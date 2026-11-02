import SwiftUI

// MARK: - 튀어 오르는 숫자

struct FloatItem: Identifiable {
    let id = UUID()
    let text: String
    let color: Color
    let big: Bool
    let xOffset: CGFloat
}

struct FloatingLabel: View {
    let item: FloatItem
    @State private var phase = 0

    var body: some View {
        Text(item.text)
            .font(.system(size: item.big ? 22 : 17, weight: .heavy, design: .rounded))
            .foregroundStyle(item.color)
            .shadow(color: item.color.opacity(0.8), radius: 8)
            .scaleEffect(phase == 0 ? 0.5 : 1)
            .offset(x: item.xOffset, y: phase == 2 ? -90 : (phase == 1 ? -16 : 0))
            .opacity(phase == 2 ? 0 : 1)
            .task {
                withAnimation(.spring(response: 0.25, dampingFraction: 0.5)) { phase = 1 }
                try? await Task.sleep(for: .milliseconds(450))
                withAnimation(.easeIn(duration: 0.9)) { phase = 2 }
            }
    }
}

// MARK: - 워프 부스트 효과

struct WarpFlash: View {
    @State private var phase = 0

    var body: some View {
        ZStack {
            Theme.gold.opacity(phase == 1 ? 0.18 : 0)
            Canvas { context, size in
                let center = CGPoint(x: size.width / 2, y: size.height / 2)
                let inner = min(size.width, size.height) * 0.22
                let outer = hypot(size.width, size.height)
                for i in 0..<64 {
                    let angle = CGFloat(i) / 64 * 2 * .pi
                    var line = Path()
                    line.move(to: CGPoint(x: center.x + cos(angle) * inner, y: center.y + sin(angle) * inner))
                    line.addLine(to: CGPoint(x: center.x + cos(angle) * outer, y: center.y + sin(angle) * outer))
                    context.stroke(line, with: .color(.white.opacity(0.5)), lineWidth: 1.2)
                }
            }
            .scaleEffect(phase == 0 ? 0.7 : (phase == 1 ? 1.1 : 1.5))
            .opacity(phase == 1 ? 1 : 0)
        }
        .ignoresSafeArea()
        .allowsHitTesting(false)
        .task {
            withAnimation(.easeOut(duration: 0.15)) { phase = 1 }
            try? await Task.sleep(for: .milliseconds(170))
            withAnimation(.easeIn(duration: 0.45)) { phase = 2 }
        }
    }
}

/// 화면 흔들기
struct ShakeEffect: GeometryEffect {
    var amount: CGFloat = 6
    var shakesPerUnit: CGFloat = 3
    var animatableData: CGFloat

    func effectValue(size: CGSize) -> ProjectionTransform {
        ProjectionTransform(CGAffineTransform(translationX: amount * sin(animatableData * .pi * shakesPerUnit), y: 0))
    }
}

// MARK: - 폭죽

struct ConfettiBurst: View {
    struct Particle {
        let vx: CGFloat
        let vy: CGFloat
        let size: CGFloat
        let spin: Double
        let color: Color
    }

    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var start = Date()
    @State private var particles: [Particle]
    private let lifetime = 2.2

    init(colors: [Color], count: Int) {
        let palette = colors.isEmpty ? [Color.white] : colors
        let made = (0..<count).map { i -> Particle in
            let angle = CGFloat.random(in: 0..<(2 * .pi))
            let speed = CGFloat.random(in: 180...420)
            return Particle(
                vx: cos(angle) * speed,
                vy: sin(angle) * speed - 180,
                size: CGFloat.random(in: 4...8),
                spin: Double.random(in: -8...8),
                color: palette[i % palette.count]
            )
        }
        _particles = State(initialValue: made)
    }

    var body: some View {
        TimelineView(.animation(paused: reduceMotion)) { timeline in
            Canvas { context, size in
                let t: Double = timeline.date.timeIntervalSince(start)
                guard !reduceMotion, t < lifetime else { return }
                let tc = CGFloat(t)
                let origin = CGPoint(x: size.width / 2, y: size.height * 0.4)
                for p in particles {
                    let x: CGFloat = origin.x + p.vx * tc
                    let y: CGFloat = origin.y + p.vy * tc + 300 * tc * tc
                    var c = context
                    c.opacity = max(0, 1 - t / lifetime)
                    c.translateBy(x: x, y: y)
                    c.rotate(by: .radians(p.spin * t))
                    c.fill(
                        Path(CGRect(x: -p.size / 2, y: -p.size / 4, width: p.size, height: p.size / 2)),
                        with: .color(p.color)
                    )
                }
            }
        }
        .ignoresSafeArea()
        .allowsHitTesting(false)
    }
}
