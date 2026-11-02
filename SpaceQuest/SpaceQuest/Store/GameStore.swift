import Foundation
import Observation

/// 앱의 모든 데이터와 게임 규칙을 처리합니다. 데이터는 폰 안의 파일 하나에 저장돼요.
@MainActor
@Observable
final class GameStore {
    static let shared = GameStore()

    var missions: [Mission] = []
    var game = GameState()
    var settings = AppSettings()
    /// 화면이 기준으로 삼는 "오늘". 앱을 다시 열 때 갱신돼요.
    var today = Date()
    /// 차례로 보여 줄 축하 화면(레벨업, 행성 발견, 캡슐 등)
    var celebrations: [CelebrationItem] = []
    /// 방금 끝낸 미션의 화면 효과
    var lastEffect: CompletionEffect?

    private let fileURL: URL

    init() {
        let dir = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
        try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
        fileURL = dir.appendingPathComponent("spacequest.json")
        load()
        #if DEBUG
        if DemoMode.isOn {
            loadDemoData()
        }
        #endif
    }

    // MARK: - 저장 / 불러오기

    private func load() {
        guard FileManager.default.fileExists(atPath: fileURL.path) else { return }
        do {
            let data = try Data(contentsOf: fileURL)
            let saved = try JSONDecoder().decode(SaveData.self, from: data)
            missions = saved.missions
            game = saved.game
            settings = saved.settings
        } catch {
            // 읽지 못한 파일은 지우지 않고 따로 보관해 둡니다.
            let backup = fileURL.deletingLastPathComponent()
                .appendingPathComponent("spacequest-unreadable-\(Int(Date().timeIntervalSince1970)).json")
            try? FileManager.default.copyItem(at: fileURL, to: backup)
        }
    }

    func save() {
        let data = SaveData(missions: missions, game: game, settings: settings)
        do {
            let encoded = try JSONEncoder().encode(data)
            try encoded.write(to: fileURL, options: .atomic)
        } catch {
            print("저장 실패: \(error)")
        }
    }

    // MARK: - 오늘

    var todayKey: String { DayKey.of(today) }

    /// 앱을 열 때마다 호출: 날짜 갱신, 귀환 보너스, 알림 다시 잡기
    func refreshDay() {
        today = Date()

        if let last = game.lastActiveDay,
           let gap = DayKey.daysBetween(last, todayKey),
           gap >= Rules.returnBonusDays,
           (game.lastReturnBonusDay ?? "") <= last {
            game.capsules += 1
            game.lastReturnBonusDay = todayKey
            enqueue(.returnBonus(days: gap))
        }

        // 오래된 기록 정리
        if let cutoff = Calendar.current.date(byAdding: .day, value: -30, to: today) {
            let cutoffKey = DayKey.of(cutoff)
            game.capsulesByDay = game.capsulesByDay.filter { $0.key >= cutoffKey }
            game.mainMission = game.mainMission.filter { $0.key >= cutoffKey }
        }

        save()
        NotificationManager.shared.reschedule(store: self)
    }

    /// 그날 목록에 보일 미션 (오늘이면 못 끝낸 지난 미션도 포함)
    func missionsShown(on day: Date) -> [Mission] {
        let cal = Calendar.current
        let dayStart = cal.startOfDay(for: day)
        let isToday = cal.isDate(day, inSameDayAs: today)
        return missions.filter { m in
            if m.occurs(on: day) { return true }
            return isToday && isOverdue(m, relativeTo: dayStart)
        }
    }

    func isOverdue(_ m: Mission, relativeTo dayStart: Date? = nil) -> Bool {
        let start = dayStart ?? Calendar.current.startOfDay(for: today)
        return m.repeatKind == .none
            && m.completions.isEmpty
            && Calendar.current.startOfDay(for: m.startDate) < start
    }

    var todayMissions: [Mission] {
        let day = today
        return missionsShown(on: day).sorted { a, b in
            let am = isMain(a, on: day), bm = isMain(b, on: day)
            if am != bm { return am }
            let ad = a.isDone(on: day), bd = b.isDone(on: day)
            if ad != bd { return !ad }
            let at = a.reminderEnabled ? a.reminderHour * 60 + a.reminderMinute : 9999
            let bt = b.reminderEnabled ? b.reminderHour * 60 + b.reminderMinute : 9999
            if at != bt { return at < bt }
            return a.createdAt < b.createdAt
        }
    }

    func isMain(_ m: Mission, on day: Date) -> Bool {
        game.mainMission[DayKey.of(day)] == m.id
    }

    var displayStreak: Int {
        guard let last = game.lastActiveDay, let gap = DayKey.daysBetween(last, todayKey) else { return 0 }
        if gap <= 1 { return game.streak }
        return (gap - 1) <= game.emergencyFuel ? game.streak : 0
    }

    // MARK: - 미션 편집

    func upsert(_ mission: Mission, makeMain: Bool) {
        if let idx = missions.firstIndex(where: { $0.id == mission.id }) {
            missions[idx] = mission
        } else {
            missions.append(mission)
        }
        let key = todayKey
        let showsToday = mission.occurs(on: today) || isOverdue(mission)
        if makeMain && showsToday {
            game.mainMission[key] = mission.id
        } else if game.mainMission[key] == mission.id {
            game.mainMission[key] = nil
        }
        save()
        NotificationManager.shared.reschedule(store: self)
    }

    func delete(_ id: UUID) {
        missions.removeAll { $0.id == id }
        game.mainMission = game.mainMission.filter { $0.value != id }
        save()
        NotificationManager.shared.cancelSnooze(missionID: id.uuidString)
        NotificationManager.shared.reschedule(store: self)
    }

    /// 그날의 메인 미션으로 지정 (이미 메인이면 해제)
    func setMain(_ id: UUID, on day: Date) {
        let key = DayKey.of(day)
        if game.mainMission[key] == id {
            game.mainMission[key] = nil
        } else {
            game.mainMission[key] = id
        }
        Feedback.shared.impact(.light, enabled: settings.hapticsOn)
        save()
        NotificationManager.shared.reschedule(store: self)
    }

    // MARK: - 미션 완료

    func toggle(_ mission: Mission) {
        if mission.isDone(on: today) {
            undo(mission.id)
        } else {
            complete(mission.id, withFeedback: true)
        }
    }

    func complete(_ id: UUID, withFeedback: Bool) {
        guard let idx = missions.firstIndex(where: { $0.id == id }) else { return }
        let mission = missions[idx]
        guard !mission.isDone(on: today) else { return }

        let now = Date()
        // 콤보: 같은 날, 정해진 시간 안에 연달아 끝내면 이어져요
        if let last = game.lastCompletionAt,
           now.timeIntervalSince(last) <= Rules.comboWindow,
           Calendar.current.isDate(last, inSameDayAs: now) {
            game.comboCount += 1
        } else {
            game.comboCount = 1
        }
        game.lastCompletionAt = now
        let comboMult = Rules.comboMultiplier(game.comboCount)

        // 워프 부스트(크리티컬)
        var crit = 1
        if Double.random(in: 0..<1) < Rules.critChance {
            crit = Double.random(in: 0..<1) < Rules.crit3Share ? 3 : 2
        }

        let main = isMain(mission, on: today)
        let base = mission.difficulty.baseXP + (main ? Rules.mainBonus : 0)
        let gained = Int((Double(base) * comboMult * Double(crit)).rounded())
        missions[idx].completions[todayKey] = gained

        updateStreakOnActivity()

        // 보급 캡슐
        let usedToday = game.capsulesByDay[todayKey] ?? 0
        var gotCapsule = false
        if usedToday < Rules.capsuleDailyLimit,
           Double.random(in: 0..<1) < (main ? Rules.capsuleChanceMain : Rules.capsuleChance) {
            game.capsules += 1
            game.capsulesByDay[todayKey] = usedToday + 1
            gotCapsule = true
        }

        addXP(gained)
        addFuel(1)

        lastEffect = CompletionEffect(
            xp: gained, crit: crit, combo: game.comboCount,
            comboMultiplier: comboMult, gotCapsule: gotCapsule
        )
        if withFeedback {
            Feedback.shared.completion(crit: crit > 1, combo: game.comboCount, capsule: gotCapsule, settings: settings)
        }

        save()
        NotificationManager.shared.cancelSnooze(missionID: id.uuidString)
        NotificationManager.shared.reschedule(store: self)
    }

    func undo(_ id: UUID) {
        guard let idx = missions.firstIndex(where: { $0.id == id }) else { return }
        let mission = missions[idx]
        let gained: Int
        if mission.repeatKind == .none {
            gained = mission.completions.values.reduce(0, +)
            missions[idx].completions = [:]
        } else {
            gained = mission.completions[todayKey] ?? 0
            missions[idx].completions[todayKey] = nil
        }
        game.xp = max(0, game.xp - gained)
        game.totalXP = max(0, game.totalXP - gained)
        game.fuel = max(0, game.fuel - 1)
        Feedback.shared.impact(.light, enabled: settings.hapticsOn)
        save()
        NotificationManager.shared.reschedule(store: self)
    }

    private func updateStreakOnActivity() {
        let key = todayKey
        if game.lastActiveDay == key { return }
        if let last = game.lastActiveDay, let gap = DayKey.daysBetween(last, key), gap >= 1 {
            let missed = gap - 1
            if missed == 0 {
                game.streak += 1
            } else if missed <= game.emergencyFuel {
                // 비상 연료가 빠진 날을 막아 줘요
                game.emergencyFuel -= missed
                game.streak += 1
            } else {
                game.streak = 1
            }
        } else {
            game.streak = 1
        }
        game.bestStreak = max(game.bestStreak, game.streak)
        game.lastActiveDay = key
    }

    private func addXP(_ amount: Int) {
        game.xp += amount
        game.totalXP += amount
        while game.xp >= Rules.xpPerLevel {
            game.xp -= Rules.xpPerLevel
            let oldRank = Rules.rank(for: game.level)
            game.level += 1
            let newRank = Rules.rank(for: game.level)
            // 레벨업 보상: 보급 캡슐 1개 (하루 제한과 별개)
            game.capsules += 1
            enqueue(.levelUp(level: game.level, newRank: newRank != oldRank ? newRank : nil))
        }
    }

    private func addFuel(_ amount: Int) {
        let before = game.fuel
        game.fuel = min(Rules.fuelGoal, game.fuel + amount)
        if before < Rules.fuelGoal && game.fuel >= Rules.fuelGoal {
            discoverPlanet()
        }
    }

    private func discoverPlanet() {
        var planet = PlanetGenerator.make(forced: game.legendNext ? .legend : nil)
        game.legendNext = false
        let key = todayKey
        planet.missions = missions.filter { $0.completions[key] != nil }.map { $0.title }
        game.planets.append(planet)
        game.fuel = 0
        enqueue(.planet(planet))
    }

    // MARK: - 보급 캡슐

    func openCapsule() {
        guard game.capsules > 0 else { return }
        game.capsules -= 1

        let rarity = Rules.roll(Rules.capsuleWeights)
        // 보상 화면을 먼저 줄 세운 뒤 효과를 적용해서, 레벨업·행성 발견 화면이 그다음에 나오게 해요.
        switch rarity {
        case .common:
            if Bool.random() {
                enqueue(.capsule(CapsuleReward(rarity: .common, title: "경험치 +30", detail: "바로 경험치가 올라요.", icon: "sparkles")))
                addXP(30)
            } else {
                game.parts += 5
                enqueue(.capsule(CapsuleReward(rarity: .common, title: "우주 부품 ×5", detail: "모아 두면 다음 업데이트의 로켓 꾸미기에서 쓸 수 있어요. (지금 \(game.parts)개)", icon: "gearshape.2.fill")))
            }
        case .rare:
            let missing = Skins.all.filter { !game.skins.contains($0.name) }
            if let skin = missing.randomElement(), Bool.random() {
                game.skins.append(skin.name)
                enqueue(.capsule(CapsuleReward(rarity: .rare, title: "로켓 스킨: \(skin.name)", detail: "설정에서 바꿔 낄 수 있어요.", icon: "paintpalette.fill")))
            } else {
                enqueue(.capsule(CapsuleReward(rarity: .rare, title: "경험치 +80", detail: "바로 경험치가 올라요.", icon: "sparkles")))
                addXP(80)
            }
        case .epic:
            if game.emergencyFuel < Rules.maxEmergencyFuel && Bool.random() {
                game.emergencyFuel += 1
                enqueue(.capsule(CapsuleReward(rarity: .epic, title: "비상 연료", detail: "하루를 놓쳐도 연속 탐사 기록을 지켜 줘요.", icon: "lifepreserver.fill")))
            } else {
                enqueue(.capsule(CapsuleReward(rarity: .epic, title: "연료 +1", detail: "다음 행성에 한 칸 더 가까워져요.", icon: "fuelpump.fill")))
                addFuel(1)
            }
        case .legend:
            game.legendNext = true
            enqueue(.capsule(CapsuleReward(rarity: .legend, title: "전설 행성 좌표", detail: "다음에 발견하는 행성은 전설 등급이에요.", icon: "star.circle.fill")))
        }
        save()
    }

    // MARK: - 축하 화면

    private func enqueue(_ c: Celebration) {
        celebrations.append(CelebrationItem(kind: c))
    }

    func dismissCelebration() {
        if !celebrations.isEmpty {
            celebrations.removeFirst()
        }
    }

    // MARK: - 통계 (탐사 일지)

    func completedCount(on day: Date) -> Int {
        let key = DayKey.of(day)
        return missions.filter { $0.completions[key] != nil }.count
    }

    func xpEarned(on day: Date) -> Int {
        let key = DayKey.of(day)
        return missions.compactMap { $0.completions[key] }.reduce(0, +)
    }

    func planets(on day: Date) -> [Planet] {
        game.planets.filter { Calendar.current.isDate($0.discoveredAt, inSameDayAs: day) }
    }

    // MARK: - 설정

    func updateSettings(_ new: AppSettings) {
        settings = new
        save()
        NotificationManager.shared.reschedule(store: self)
    }

    func requestNotificationsIfNeeded() async {
        guard !settings.askedNotifications else { return }
        settings.askedNotifications = true
        save()
        _ = await NotificationManager.shared.requestAuthorization()
        NotificationManager.shared.reschedule(store: self)
    }

    func resetAll() {
        missions = []
        game = GameState()
        celebrations = []
        lastEffect = nil
        save()
        NotificationManager.shared.reschedule(store: self)
    }
}
