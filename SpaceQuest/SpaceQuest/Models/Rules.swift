import Foundation

/// 게임 수치를 한곳에 모아 둡니다. 여기 숫자만 바꾸면 앱 전체에 반영돼요.
enum Rules {
    /// 행성 하나를 발견하는 데 필요한 연료(완료한 미션 수)
    static let fuelGoal = 5
    /// 레벨 하나에 필요한 경험치
    static let xpPerLevel = 200
    /// 메인 미션 보너스 경험치
    static let mainBonus = 30

    /// 워프 부스트(크리티컬) 확률과, 그중 3배가 나올 비율
    static let critChance = 0.10
    static let crit3Share = 0.30

    /// 이 시간 안에 연달아 끝내면 콤보
    static let comboWindow: TimeInterval = 45 * 60
    static let comboMultipliers: [Double] = [1, 1, 1.2, 1.5, 2]

    /// 보급 캡슐
    static let capsuleChance = 0.15
    static let capsuleChanceMain = 0.40
    static let capsuleDailyLimit = 3
    static let capsuleWeights: [(Rarity, Double)] = [(.common, 60), (.rare, 28), (.epic, 10), (.legend, 2)]

    /// 행성 등급 확률
    static let planetWeights: [(Rarity, Double)] = [(.common, 60), (.rare, 25), (.epic, 12), (.legend, 3)]

    static let maxEmergencyFuel = 2
    /// 며칠 쉬고 돌아오면 귀환 보너스를 줄지
    static let returnBonusDays = 3
    static let dexSize = 48

    static let ranks: [(Int, String)] = [
        (1, "훈련생"), (3, "소위"), (6, "중위"), (10, "대위"), (15, "함장"), (20, "제독")
    ]

    static func rank(for level: Int) -> String {
        ranks.last(where: { level >= $0.0 })?.1 ?? "훈련생"
    }

    static func comboMultiplier(_ combo: Int) -> Double {
        let i = min(max(combo, 0), comboMultipliers.count - 1)
        return comboMultipliers[i]
    }

    /// 1.0 → "1", 1.5 → "1.5"
    static func multText(_ value: Double) -> String {
        value == value.rounded() ? String(Int(value)) : String(format: "%.1f", value)
    }

    static func roll(_ table: [(Rarity, Double)]) -> Rarity {
        let total = table.reduce(0) { $0 + $1.1 }
        var r = Double.random(in: 0..<total)
        for (rarity, weight) in table {
            r -= weight
            if r < 0 { return rarity }
        }
        return table.first?.0 ?? .common
    }
}
