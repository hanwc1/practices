import SwiftUI

/// 행성 그림. 같은 행성은 항상 똑같이 그려져요.
struct PlanetView: View {
    let planet: Planet
    var size: CGFloat = 64

    var body: some View {
        Canvas { context, canvasSize in
            draw(in: &context, size: canvasSize.width)
        }
        .frame(width: size, height: size)
        .accessibilityLabel("\(planet.rarity.label) \(planet.type) \(planet.name)")
    }

    private func draw(in context: inout GraphicsContext, size s: CGFloat) {
        var rng = SeededRandom(seed: planet.seed)
        let cx = s / 2
        let cy = s / 2
        let r = s * (planet.ring ? 0.26 : 0.36)
        let sphereRect = CGRect(x: cx - r, y: cy - r, width: r * 2, height: r * 2)
        let sphere = Path(ellipseIn: sphereRect)

        let base = Color(hue: planet.hue, saturation: 0.55, brightness: planet.rarity == .legend ? 0.88 : 0.72)
        let bandHue = planet.hue2
        let ringColor = Color(hue: planet.hue2, saturation: 0.45, brightness: 1.0).opacity(0.85)

        func ringPath(back: Bool) -> Path {
            var p = Path()
            p.addRelativeArc(
                center: .zero, radius: 1,
                startAngle: .degrees(back ? 180 : 0), delta: .degrees(180)
            )
            let transform = CGAffineTransform(translationX: cx, y: cy)
                .rotated(by: -0.35)
                .scaledBy(x: r * 1.75, y: r * 0.45)
            return p.applying(transform)
        }

        // 고리 뒤쪽 절반
        if planet.ring {
            context.stroke(ringPath(back: true), with: .color(ringColor), lineWidth: r * 0.16)
        }

        // 행성 본체 (영웅·전설은 빛남)
        context.drawLayer { layer in
            switch planet.rarity {
            case .legend:
                layer.addFilter(.shadow(color: Color(red: 1, green: 0.82, blue: 0.4).opacity(0.95), radius: s * 0.12))
            case .epic:
                layer.addFilter(.shadow(color: Color(red: 0.77, green: 0.55, blue: 1).opacity(0.8), radius: s * 0.08))
            default:
                break
            }
            layer.fill(sphere, with: .color(base))
        }

        // 줄무늬, 크레이터, 입체 그림자
        context.drawLayer { layer in
            layer.clip(to: sphere)
            for _ in 0..<planet.bands {
                let y: CGFloat = cy - r + CGFloat(rng.unit()) * 2 * r
                let h: CGFloat = r * (0.08 + CGFloat(rng.unit()) * 0.22)
                let opacity: Double = 0.22 + rng.unit() * 0.3
                layer.fill(
                    Path(CGRect(x: cx - r, y: y, width: r * 2, height: h)),
                    with: .color(Color(hue: bandHue, saturation: 0.6, brightness: 0.95).opacity(opacity))
                )
            }
            if planet.rarity == .common {
                for _ in 0..<4 {
                    let x: CGFloat = cx - r + CGFloat(rng.unit()) * 2 * r
                    let y: CGFloat = cy - r + CGFloat(rng.unit()) * 2 * r
                    let cr: CGFloat = r * (0.08 + CGFloat(rng.unit()) * 0.14)
                    layer.fill(
                        Path(ellipseIn: CGRect(x: x - cr, y: y - cr, width: cr * 2, height: cr * 2)),
                        with: .color(.black.opacity(0.18))
                    )
                }
            }
            let shade = Gradient(stops: [
                .init(color: .white.opacity(0.45), location: 0),
                .init(color: .white.opacity(0), location: 0.35),
                .init(color: .black.opacity(0.65), location: 1)
            ])
            layer.fill(
                sphere,
                with: .radialGradient(
                    shade,
                    center: CGPoint(x: cx - r * 0.45, y: cy - r * 0.45),
                    startRadius: r * 0.05,
                    endRadius: r * 1.7
                )
            )
        }

        // 고리 앞쪽 절반
        if planet.ring {
            context.stroke(ringPath(back: false), with: .color(ringColor), lineWidth: r * 0.16)
        }

        // 전설 행성 반짝임
        if planet.rarity == .legend {
            for spot in [CGPoint(x: 0.2, y: 0.22), CGPoint(x: 0.82, y: 0.3), CGPoint(x: 0.75, y: 0.82)] {
                let x = spot.x * s
                let y = spot.y * s
                let k = s * 0.035
                var star = Path()
                star.move(to: CGPoint(x: x, y: y - k * 2))
                star.addLine(to: CGPoint(x: x + k * 0.5, y: y))
                star.addLine(to: CGPoint(x: x, y: y + k * 2))
                star.addLine(to: CGPoint(x: x - k * 0.5, y: y))
                star.closeSubpath()
                star.move(to: CGPoint(x: x - k * 2, y: y))
                star.addLine(to: CGPoint(x: x, y: y + k * 0.5))
                star.addLine(to: CGPoint(x: x + k * 2, y: y))
                star.addLine(to: CGPoint(x: x, y: y - k * 0.5))
                star.closeSubpath()
                context.fill(star, with: .color(Color(red: 1, green: 0.96, blue: 0.84)))
            }
        }
    }
}
