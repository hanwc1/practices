import Foundation

/// 같은 seed 면 항상 같은 숫자를 내는 난수 생성기 (행성 모양을 매번 똑같이 그리기 위해)
struct SeededRandom: RandomNumberGenerator {
    private var state: UInt64

    init(seed: Int) {
        state = UInt64(truncatingIfNeeded: seed) &+ 0x9E37_79B9_7F4A_7C15
    }

    mutating func next() -> UInt64 {
        state &+= 0x9E37_79B9_7F4A_7C15
        var z = state
        z = (z ^ (z >> 30)) &* 0xBF58_476D_1CE4_E5B9
        z = (z ^ (z >> 27)) &* 0x94D0_49BB_1331_11EB
        return z ^ (z >> 31)
    }

    /// 0 이상 1 미만
    mutating func unit() -> Double {
        Double(next() >> 11) / 9_007_199_254_740_992.0
    }
}

enum PlanetGenerator {
    static let prefixes = ["케플러", "글리제", "트라피스트", "코로트", "와스프", "로스", "HD", "TOI"]

    static func types(for rarity: Rarity) -> [String] {
        switch rarity {
        case .common: return ["암석 행성", "사막 행성", "왜소 행성"]
        case .rare: return ["고리 행성", "얼음 거인"]
        case .epic: return ["생명체 신호 행성", "오로라 행성"]
        case .legend: return ["보석 결정 행성", "쌍성 궤도 행성"]
        }
    }

    static func make(forced: Rarity? = nil) -> Planet {
        let rarity = forced ?? Rules.roll(Rules.planetWeights)
        let hue = Double.random(in: 0..<1)
        let hue2 = (hue + 0.08 + Double.random(in: 0..<0.33)).truncatingRemainder(dividingBy: 1)

        let bands: Int
        let ring: Bool
        switch rarity {
        case .common:
            bands = Int.random(in: 0...1)
            ring = Double.random(in: 0..<1) < 0.12
        case .rare:
            bands = Int.random(in: 3...6)
            ring = Double.random(in: 0..<1) < 0.7
        case .epic, .legend:
            bands = Int.random(in: 3...6)
            ring = true
        }

        let letter = ["b", "c", "d", "e", "f"].randomElement() ?? "b"
        let name = "\(prefixes.randomElement() ?? "케플러")-\(Int.random(in: 10...899))\(letter)"

        return Planet(
            name: name,
            type: types(for: rarity).randomElement() ?? "행성",
            rarity: rarity,
            hue: hue,
            hue2: hue2,
            bands: bands,
            ring: ring,
            seed: Int.random(in: 0..<1_000_000_000),
            discoveredAt: Date()
        )
    }
}
