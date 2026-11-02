#if DEBUG
import Foundation

/// 자동 화면 캡처용 예시 데이터. 실행 인자에 `-demo` 가 있을 때만 켜지고,
/// 개발용(Debug) 빌드에만 들어가요. 평소 실행에는 아무 영향이 없어요.
enum DemoMode {
    static var arguments: [String] { ProcessInfo.processInfo.arguments }

    static var isOn: Bool { arguments.contains("-demo") }

    static func value(after flag: String) -> String? {
        guard let i = arguments.firstIndex(of: flag), i + 1 < arguments.count else { return nil }
        return arguments[i + 1]
    }
}

extension GameStore {
    func loadDemoData() {
        let cal = Calendar.current
        let now = Date()
        let todayKey = DayKey.of(now)
        let yesterday = cal.date(byAdding: .day, value: -1, to: now) ?? now

        var stretch = Mission(title: "아침 스트레칭 5분", difficulty: .easy, repeatKind: .daily)
        stretch.startDate = cal.date(byAdding: .day, value: -20, to: now) ?? now
        stretch.reminderEnabled = true
        stretch.reminderHour = 7
        stretch.completions[todayKey] = 10

        let report = Mission(title: "분기 보고서 초안 쓰기", difficulty: .hard)

        var words = Mission(title: "영어 단어 10개", repeatKind: .weekly)
        words.weekdays = Array(1...7)
        words.startDate = stretch.startDate
        words.reminderEnabled = true
        words.reminderHour = 20

        let gym = Mission(title: "헬스장 가기")

        var water = Mission(title: "물 2L 마시기", difficulty: .easy, repeatKind: .daily)
        water.startDate = stretch.startDate
        water.completions[todayKey] = 12

        var overdue = Mission(title: "택배 반품 보내기", difficulty: .easy)
        overdue.startDate = yesterday

        missions = [stretch, report, words, gym, water, overdue]

        var g = GameState()
        g.level = 4
        g.xp = 150
        g.totalXP = 750
        g.fuel = 2
        g.capsules = 1
        g.emergencyFuel = 1
        g.streak = 12
        g.bestStreak = 15
        g.lastActiveDay = todayKey
        g.lastCompletionAt = now.addingTimeInterval(-8 * 60)
        g.comboCount = 2
        g.mainMission[todayKey] = report.id
        g.skins = ["기본", "오로라"]
        g.parts = 15
        var seed = 11
        for rarity in [Rarity.common, .rare, .common, .epic, .rare, .legend, .common] {
            var p = PlanetGenerator.make(forced: rarity)
            p.seed = seed
            seed += 7
            p.discoveredAt = cal.date(byAdding: .day, value: -seed / 7, to: now) ?? now
            g.planets.append(p)
        }
        game = g
        settings.askedNotifications = true

        switch DemoMode.value(after: "-celebrate") {
        case "planet":
            var p = PlanetGenerator.make(forced: .epic)
            p.seed = 4242
            p.name = "케플러-27b"
            celebrations.append(CelebrationItem(kind: .planet(p)))
        case "capsule":
            celebrations.append(CelebrationItem(kind: .capsule(CapsuleReward(
                rarity: .legend, title: "전설 행성 좌표",
                detail: "다음에 발견하는 행성은 전설 등급이에요.", icon: "star.circle.fill"
            ))))
        case "level":
            celebrations.append(CelebrationItem(kind: .levelUp(level: 6, newRank: "중위")))
        default:
            break
        }
    }
}
#endif
