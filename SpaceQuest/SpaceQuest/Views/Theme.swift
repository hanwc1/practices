import SwiftUI

enum Theme {
    static let bgTop = Color(red: 0.15, green: 0.20, blue: 0.44)
    static let bgMid = Color(red: 0.05, green: 0.07, blue: 0.19)
    static let bgBottom = Color(red: 0.03, green: 0.04, blue: 0.11)
    static let ink = Color(red: 0.05, green: 0.07, blue: 0.19)
    static let accent = Color(red: 0.49, green: 0.77, blue: 1.0)
    static let gold = Color(red: 1.0, green: 0.82, blue: 0.40)
    static let combo = Color(red: 1.0, green: 0.54, blue: 0.36)
    static let muted = Color(red: 0.62, green: 0.69, blue: 0.91)
    static let card = Color.white.opacity(0.06)
    static let cardStroke = Color(red: 0.49, green: 0.71, blue: 1.0).opacity(0.18)
    static let xpColors = [Color(red: 0.31, green: 0.82, blue: 1.0), Color(red: 0.66, green: 0.55, blue: 1.0)]
    static let cardTop = Color(red: 0.10, green: 0.13, blue: 0.31)
    static let cardBottom = Color(red: 0.05, green: 0.07, blue: 0.20)
}

extension Rarity {
    var color: Color {
        switch self {
        case .common: return Color(red: 0.62, green: 0.70, blue: 0.85)
        case .rare: return Color(red: 0.37, green: 0.82, blue: 1.0)
        case .epic: return Color(red: 0.77, green: 0.55, blue: 1.0)
        case .legend: return Color(red: 1.0, green: 0.82, blue: 0.40)
        }
    }
}

struct RocketSkin: Identifiable {
    let name: String
    let colors: [Color]
    var id: String { name }
}

enum Skins {
    static let all: [RocketSkin] = [
        RocketSkin(name: "기본", colors: [Color(red: 1.0, green: 0.70, blue: 0.28), Color(red: 1.0, green: 0.82, blue: 0.40)]),
        RocketSkin(name: "오로라", colors: [Color(red: 0.30, green: 0.95, blue: 0.70), Color(red: 0.40, green: 0.70, blue: 1.0), Color(red: 0.75, green: 0.50, blue: 1.0)]),
        RocketSkin(name: "성운", colors: [Color(red: 1.0, green: 0.45, blue: 0.75), Color(red: 0.60, green: 0.40, blue: 1.0)]),
        RocketSkin(name: "얼음", colors: [Color(red: 0.60, green: 0.95, blue: 1.0), Color.white]),
        RocketSkin(name: "황금", colors: [Color(red: 1.0, green: 0.84, blue: 0.30), Color(red: 1.0, green: 0.96, blue: 0.75)])
    ]

    static func named(_ name: String) -> RocketSkin {
        all.first { $0.name == name } ?? all[0]
    }
}

// MARK: - 공용 부품

/// 우주 배경 (반짝이는 별 포함)
struct SpaceBackground: View {
    var body: some View {
        ZStack {
            RadialGradient(
                colors: [Theme.bgTop, Theme.bgMid, Theme.bgBottom],
                center: UnitPoint(x: 0.85, y: 0),
                startRadius: 0,
                endRadius: 750
            )
            StarField()
        }
        .ignoresSafeArea()
    }
}

struct StarField: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        TimelineView(.animation(minimumInterval: 1.0 / 12.0, paused: reduceMotion)) { timeline in
            Canvas { context, size in
                let t = timeline.date.timeIntervalSinceReferenceDate
                var rng = SeededRandom(seed: 9)
                for _ in 0..<70 {
                    let x: CGFloat = CGFloat(rng.unit()) * size.width
                    let y: CGFloat = CGFloat(rng.unit()) * size.height
                    let r: CGFloat = 0.4 + CGFloat(rng.unit()) * 1.1
                    let p: Double = rng.unit() * 6
                    let s: Double = 0.5 + rng.unit() * 1.5
                    let wave: Double = 0.5 + 0.5 * sin(p + t * s)
                    let alpha: Double = reduceMotion ? 0.6 : 0.35 + 0.45 * wave
                    let rect = CGRect(x: x - r, y: y - r, width: r * 2, height: r * 2)
                    context.fill(Path(ellipseIn: rect), with: .color(.white.opacity(alpha)))
                }
            }
        }
        .allowsHitTesting(false)
    }
}

struct ProgressBar: View {
    let value: Double
    let colors: [Color]
    var height: CGFloat = 8

    var body: some View {
        GeometryReader { geo in
            ZStack(alignment: .leading) {
                Capsule().fill(Color.white.opacity(0.1))
                Capsule()
                    .fill(LinearGradient(colors: colors, startPoint: .leading, endPoint: .trailing))
                    .frame(width: max(0, min(1, value)) * geo.size.width)
            }
        }
        .frame(height: height)
        .animation(.spring(response: 0.45, dampingFraction: 0.7), value: value)
    }
}

struct RarityChip: View {
    let text: String
    let color: Color

    var body: some View {
        Text(text)
            .font(.caption.weight(.bold))
            .padding(.horizontal, 10)
            .padding(.vertical, 3)
            .background(Capsule().fill(color))
            .foregroundStyle(Theme.ink)
    }
}

/// 반투명 카드 배경
struct CardBackground: ViewModifier {
    var stroke: Color = Theme.cardStroke
    var fill: Color = Theme.card

    func body(content: Content) -> some View {
        content
            .background(RoundedRectangle(cornerRadius: 16).fill(fill))
            .overlay(RoundedRectangle(cornerRadius: 16).stroke(stroke, lineWidth: 1))
    }
}

extension View {
    func spaceCard(stroke: Color = Theme.cardStroke, fill: Color = Theme.card) -> some View {
        modifier(CardBackground(stroke: stroke, fill: fill))
    }
}
