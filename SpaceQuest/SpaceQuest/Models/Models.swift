import Foundation

// MARK: - 날짜 키

/// 하루를 "yyyy-MM-dd" 문자열로 다룹니다. (기기 시간대 기준)
enum DayKey {
    static let formatter: DateFormatter = {
        let f = DateFormatter()
        f.calendar = Calendar(identifier: .gregorian)
        f.locale = Locale(identifier: "en_US_POSIX")
        f.timeZone = .current
        f.dateFormat = "yyyy-MM-dd"
        return f
    }()

    static func of(_ date: Date) -> String {
        formatter.string(from: date)
    }

    static func date(_ key: String) -> Date? {
        formatter.date(from: key)
    }

    /// a 에서 b 까지 며칠인지 (같은 날이면 0)
    static func daysBetween(_ a: String, _ b: String) -> Int? {
        guard let da = date(a), let db = date(b) else { return nil }
        return Calendar.current.dateComponents([.day], from: da, to: db).day
    }
}

// MARK: - 미션

enum Difficulty: String, Codable, CaseIterable, Identifiable {
    case easy, normal, hard

    var id: String { rawValue }

    var label: String {
        switch self {
        case .easy: return "쉬움"
        case .normal: return "보통"
        case .hard: return "어려움"
        }
    }

    var baseXP: Int {
        switch self {
        case .easy: return 10
        case .normal: return 20
        case .hard: return 40
        }
    }
}

enum RepeatKind: String, Codable, CaseIterable, Identifiable {
    case none, daily, weekly, monthly

    var id: String { rawValue }

    var label: String {
        switch self {
        case .none: return "반복 안 함"
        case .daily: return "매일"
        case .weekly: return "요일 선택"
        case .monthly: return "매월"
        }
    }
}

struct Mission: Identifiable, Codable, Equatable {
    var id = UUID()
    var title: String
    var difficulty: Difficulty = .normal
    var repeatKind: RepeatKind = .none
    /// Calendar 요일 번호: 1 = 일요일 … 7 = 토요일
    var weekdays: [Int] = []
    /// 반복 안 함: 그 날짜 / 반복: 시작일
    var startDate: Date = Date()
    var reminderEnabled: Bool = false
    var reminderHour: Int = 9
    var reminderMinute: Int = 0
    /// 완료한 날짜 키 → 그때 받은 경험치
    var completions: [String: Int] = [:]
    var createdAt: Date = Date()

    enum CodingKeys: String, CodingKey {
        case id, title, difficulty, repeatKind, weekdays, startDate
        case reminderEnabled, reminderHour, reminderMinute, completions, createdAt
    }
}

extension Mission {
    init(from decoder: Decoder) throws {
        let c = try decoder.container(keyedBy: CodingKeys.self)
        id = c.decode(.id, default: UUID())
        title = c.decode(.title, default: "")
        difficulty = c.decode(.difficulty, default: Difficulty.normal)
        repeatKind = c.decode(.repeatKind, default: RepeatKind.none)
        weekdays = c.decode(.weekdays, default: [Int]())
        startDate = c.decode(.startDate, default: Date())
        reminderEnabled = c.decode(.reminderEnabled, default: false)
        reminderHour = c.decode(.reminderHour, default: 9)
        reminderMinute = c.decode(.reminderMinute, default: 0)
        completions = c.decode(.completions, default: [String: Int]())
        createdAt = c.decode(.createdAt, default: Date())
    }

    /// 이 날짜에 해야 하는 미션인지
    func occurs(on day: Date) -> Bool {
        let cal = Calendar.current
        let d = cal.startOfDay(for: day)
        let s = cal.startOfDay(for: startDate)
        switch repeatKind {
        case .none:
            return d == s
        case .daily:
            return d >= s
        case .weekly:
            return d >= s && weekdays.contains(cal.component(.weekday, from: d))
        case .monthly:
            return d >= s && cal.component(.day, from: d) == cal.component(.day, from: s)
        }
    }

    /// 이 날짜 기준으로 완료했는지 (반복 안 하는 미션은 한 번만 하면 완료)
    func isDone(on day: Date) -> Bool {
        if repeatKind == .none { return !completions.isEmpty }
        return completions[DayKey.of(day)] != nil
    }

    /// 완료로 받은 경험치 (표시용)
    func xpGained(on day: Date) -> Int? {
        if repeatKind == .none { return completions.values.first }
        return completions[DayKey.of(day)]
    }

    var reminderText: String? {
        guard reminderEnabled else { return nil }
        return String(format: "%02d:%02d", reminderHour, reminderMinute)
    }

    var repeatText: String? {
        switch repeatKind {
        case .none:
            return nil
        case .daily:
            return "매일"
        case .weekly:
            let names = ["일", "월", "화", "수", "목", "금", "토"]
            let days = weekdays.sorted().compactMap { (1...7).contains($0) ? names[$0 - 1] : nil }
            return days.isEmpty ? "매주" : days.joined()
        case .monthly:
            return "매월 \(Calendar.current.component(.day, from: startDate))일"
        }
    }
}

// MARK: - 행성

enum Rarity: String, Codable, CaseIterable {
    case common, rare, epic, legend

    var label: String {
        switch self {
        case .common: return "일반"
        case .rare: return "희귀"
        case .epic: return "영웅"
        case .legend: return "전설"
        }
    }

    var flavor: String {
        switch self {
        case .common: return "오늘 하루가 만든 행성이에요."
        case .rare: return "보기 드문 행성이에요."
        case .epic: return "희미한 생명체 신호가 잡혔어요."
        case .legend: return "아주 드물게 나오는 전설의 행성이에요."
        }
    }
}

struct Planet: Identifiable, Codable, Equatable {
    var id = UUID()
    var name: String
    var type: String
    var rarity: Rarity
    /// 0...1
    var hue: Double
    var hue2: Double
    var bands: Int
    var ring: Bool
    var seed: Int
    var discoveredAt: Date
    /// 발견한 날 끝낸 미션 이름들
    var missions: [String] = []
}

// MARK: - 게임 상태

struct GameState: Codable {
    var level = 1
    var xp = 0
    var totalXP = 0
    var fuel = 0
    var capsules = 0
    var capsulesByDay: [String: Int] = [:]
    var emergencyFuel = 1
    var streak = 0
    var bestStreak = 0
    var lastActiveDay: String? = nil
    var lastReturnBonusDay: String? = nil
    var legendNext = false
    var parts = 0
    var skins: [String] = ["기본"]
    var planets: [Planet] = []
    /// 날짜 키 → 그날의 메인 미션 id
    var mainMission: [String: UUID] = [:]
    var lastCompletionAt: Date? = nil
    var comboCount = 0

    enum CodingKeys: String, CodingKey {
        case level, xp, totalXP, fuel, capsules, capsulesByDay, emergencyFuel
        case streak, bestStreak, lastActiveDay, lastReturnBonusDay, legendNext
        case parts, skins, planets, mainMission, lastCompletionAt, comboCount
    }
}

extension GameState {
    init(from decoder: Decoder) throws {
        let c = try decoder.container(keyedBy: CodingKeys.self)
        level = c.decode(.level, default: 1)
        xp = c.decode(.xp, default: 0)
        totalXP = c.decode(.totalXP, default: 0)
        fuel = c.decode(.fuel, default: 0)
        capsules = c.decode(.capsules, default: 0)
        capsulesByDay = c.decode(.capsulesByDay, default: [String: Int]())
        emergencyFuel = c.decode(.emergencyFuel, default: 1)
        streak = c.decode(.streak, default: 0)
        bestStreak = c.decode(.bestStreak, default: 0)
        lastActiveDay = c.decode(.lastActiveDay, default: String?.none)
        lastReturnBonusDay = c.decode(.lastReturnBonusDay, default: String?.none)
        legendNext = c.decode(.legendNext, default: false)
        parts = c.decode(.parts, default: 0)
        skins = c.decode(.skins, default: ["기본"])
        planets = c.decode(.planets, default: [Planet]())
        mainMission = c.decode(.mainMission, default: [String: UUID]())
        lastCompletionAt = c.decode(.lastCompletionAt, default: Date?.none)
        comboCount = c.decode(.comboCount, default: 0)
    }
}

// MARK: - 설정

struct AppSettings: Codable, Equatable {
    var soundOn = true
    var hapticsOn = true
    var morningOn = true
    var morningHour = 8
    var morningMinute = 30
    var eveningOn = true
    var eveningHour = 21
    var eveningMinute = 30
    var skin = "기본"
    var askedNotifications = false

    enum CodingKeys: String, CodingKey {
        case soundOn, hapticsOn, morningOn, morningHour, morningMinute
        case eveningOn, eveningHour, eveningMinute, skin, askedNotifications
    }
}

extension AppSettings {
    init(from decoder: Decoder) throws {
        let c = try decoder.container(keyedBy: CodingKeys.self)
        soundOn = c.decode(.soundOn, default: true)
        hapticsOn = c.decode(.hapticsOn, default: true)
        morningOn = c.decode(.morningOn, default: true)
        morningHour = c.decode(.morningHour, default: 8)
        morningMinute = c.decode(.morningMinute, default: 30)
        eveningOn = c.decode(.eveningOn, default: true)
        eveningHour = c.decode(.eveningHour, default: 21)
        eveningMinute = c.decode(.eveningMinute, default: 30)
        skin = c.decode(.skin, default: "기본")
        askedNotifications = c.decode(.askedNotifications, default: false)
    }
}

// MARK: - 저장 파일

struct SaveData: Codable {
    var missions: [Mission] = []
    var game = GameState()
    var settings = AppSettings()

    enum CodingKeys: String, CodingKey {
        case missions, game, settings
    }
}

extension SaveData {
    init(from decoder: Decoder) throws {
        let c = try decoder.container(keyedBy: CodingKeys.self)
        missions = c.decode(.missions, default: [Mission]())
        game = c.decode(.game, default: GameState())
        settings = c.decode(.settings, default: AppSettings())
    }
}

extension KeyedDecodingContainer {
    /// 값이 없거나 형식이 달라도 기본값을 써서, 앱을 업데이트해도 기존 기록을 잃지 않게 합니다.
    func decode<T: Decodable>(_ key: Key, default value: T) -> T {
        (try? decodeIfPresent(T.self, forKey: key)) ?? value
    }
}

// MARK: - 화면 이벤트

struct CapsuleReward {
    var rarity: Rarity
    var title: String
    var detail: String
    /// SF Symbols 이름
    var icon: String
}

enum Celebration {
    case levelUp(level: Int, newRank: String?)
    case planet(Planet)
    case capsule(CapsuleReward)
    case returnBonus(days: Int)
}

struct CelebrationItem: Identifiable {
    let id = UUID()
    let kind: Celebration
}

/// 미션 완료 직후 화면 효과(숫자 튀어 오르기, 워프 등)에 쓰는 정보
struct CompletionEffect: Equatable {
    let id = UUID()
    let xp: Int
    let crit: Int
    let combo: Int
    let comboMultiplier: Double
    let gotCapsule: Bool
}
