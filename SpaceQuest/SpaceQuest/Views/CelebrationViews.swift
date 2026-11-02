import SwiftUI

/// 레벨업, 행성 발견, 캡슐 열기, 귀환 보너스를 화면 가운데 크게 보여 줍니다.
struct CelebrationOverlay: View {
    @Environment(GameStore.self) private var store
    let item: CelebrationItem

    var body: some View {
        ZStack {
            Color.black.opacity(0.72)
                .ignoresSafeArea()
            switch item.kind {
            case .levelUp(let level, let newRank):
                LevelUpCard(level: level, newRank: newRank, onDone: done)
            case .planet(let planet):
                PlanetFoundCard(planet: planet, onDone: done)
            case .capsule(let reward):
                CapsuleCard(reward: reward, onDone: done)
            case .returnBonus(let days):
                ReturnCard(days: days, onDone: done)
            }
        }
    }

    private func done() {
        store.dismissCelebration()
    }
}

/// 축하 카드 공통 틀
struct CelebrationCard<Content: View>: View {
    let color: Color
    let kicker: String
    @ViewBuilder let content: Content
    @State private var appeared = false

    var body: some View {
        VStack(spacing: 10) {
            Text(kicker)
                .font(.caption.weight(.semibold))
                .tracking(3)
                .foregroundStyle(color)
            content
        }
        .multilineTextAlignment(.center)
        .foregroundStyle(.white)
        .padding(22)
        .frame(maxWidth: 340)
        .background(
            RoundedRectangle(cornerRadius: 24)
                .fill(LinearGradient(colors: [Theme.cardTop, Theme.cardBottom], startPoint: .top, endPoint: .bottom))
        )
        .overlay(RoundedRectangle(cornerRadius: 24).stroke(color.opacity(0.7), lineWidth: 1))
        .shadow(color: color.opacity(0.5), radius: 30)
        .padding(24)
        .scaleEffect(appeared ? 1 : 0.8)
        .opacity(appeared ? 1 : 0)
        .onAppear {
            withAnimation(.spring(response: 0.4, dampingFraction: 0.65)) {
                appeared = true
            }
        }
    }
}

struct GoButton: View {
    let title: String
    let color: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.headline)
                .foregroundStyle(Theme.ink)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 13)
                .background(RoundedRectangle(cornerRadius: 14).fill(color))
        }
        .buttonStyle(.plain)
        .padding(.top, 6)
    }
}

struct LevelUpCard: View {
    @Environment(GameStore.self) private var store
    let level: Int
    let newRank: String?
    let onDone: () -> Void

    private let color = Color(red: 0.66, green: 0.55, blue: 1.0)

    var body: some View {
        ZStack {
            ConfettiBurst(colors: [color, Theme.accent, .white], count: 70)
            CelebrationCard(color: color, kicker: "LEVEL UP") {
                Text("Lv.\(level)")
                    .font(.system(size: 52, weight: .heavy, design: .rounded))
                    .shadow(color: color, radius: 18)
                Text(newRank.map { "계급 승급! \($0)" } ?? "레벨이 올랐어요")
                    .font(.title3.bold())
                Text("보상: 보급 캡슐 1개")
                    .font(.subheadline)
                    .foregroundStyle(Theme.muted)
                GoButton(title: "계속 탐사", color: color, action: onDone)
            }
        }
        .task {
            Feedback.shared.play(.level, enabled: store.settings.soundOn)
            Feedback.shared.success(enabled: store.settings.hapticsOn)
        }
    }
}

struct PlanetFoundCard: View {
    @Environment(GameStore.self) private var store
    let planet: Planet
    let onDone: () -> Void

    var body: some View {
        let color = planet.rarity.color
        let count: Int
        switch planet.rarity {
        case .legend: count = 180
        case .epic: count = 120
        default: count = 80
        }

        return ZStack {
            ConfettiBurst(colors: [color, .white, Theme.accent], count: count)
            CelebrationCard(color: color, kicker: "NEW PLANET") {
                Text("새 행성을 발견했어요!")
                    .font(.title3.bold())
                PlanetView(planet: planet, size: 170)
                RarityChip(text: "\(planet.rarity.label) · \(planet.type)", color: color)
                Text(planet.name)
                    .font(.title2.bold())
                Text(planet.rarity.flavor)
                    .font(.subheadline)
                    .foregroundStyle(Theme.muted)
                GoButton(title: "도감에 등록", color: color, action: onDone)
            }
        }
        .task {
            Feedback.shared.play(.planet, enabled: store.settings.soundOn)
            Feedback.shared.success(enabled: store.settings.hapticsOn)
        }
    }
}

struct CapsuleCard: View {
    @Environment(GameStore.self) private var store
    let reward: CapsuleReward
    let onDone: () -> Void

    @State private var opened = false
    @State private var wobble = false

    var body: some View {
        let color = opened ? reward.rarity.color : Theme.accent
        let bigReward = reward.rarity == .epic || reward.rarity == .legend

        return ZStack {
            if opened && bigReward {
                ConfettiBurst(colors: [color, .white], count: reward.rarity == .legend ? 160 : 90)
            }
            CelebrationCard(color: color, kicker: "SUPPLY CAPSULE") {
                if opened {
                    ZStack {
                        Circle()
                            .fill(RadialGradient(colors: [color, color.opacity(0)], center: .center, startRadius: 0, endRadius: 70))
                            .frame(width: 140, height: 140)
                        Image(systemName: reward.icon)
                            .font(.system(size: 46, weight: .bold))
                            .foregroundStyle(.white)
                            .shadow(color: color, radius: 12)
                    }
                    .transition(.scale(scale: 0.2).combined(with: .opacity))
                    RarityChip(text: reward.rarity.label, color: color)
                    Text(reward.title)
                        .font(.title3.bold())
                    Text(reward.detail)
                        .font(.subheadline)
                        .foregroundStyle(Theme.muted)
                    GoButton(title: "받기", color: color, action: onDone)
                } else {
                    Text("보급 캡슐 여는 중…")
                        .font(.title3.bold())
                    ZStack {
                        Capsule()
                            .fill(LinearGradient(
                                colors: [Color(red: 0.56, green: 0.65, blue: 0.85), Color(red: 0.93, green: 0.96, blue: 1), Color(red: 0.62, green: 0.70, blue: 0.89)],
                                startPoint: .leading, endPoint: .trailing
                            ))
                        Rectangle()
                            .fill(Color(red: 0.30, green: 0.37, blue: 0.61))
                            .frame(height: 10)
                    }
                    .frame(width: 84, height: 116)
                    .clipShape(Capsule())
                    .rotationEffect(.degrees(wobble ? 8 : -8))
                    .animation(.linear(duration: 0.08).repeatForever(autoreverses: true), value: wobble)
                    .padding(.vertical, 12)
                    Text("무엇이 들어 있을까요?")
                        .font(.subheadline)
                        .foregroundStyle(Theme.muted)
                }
            }
        }
        .task {
            wobble = true
            Feedback.shared.play(.shake, enabled: store.settings.soundOn)
            Feedback.shared.impact(.light, enabled: store.settings.hapticsOn)
            try? await Task.sleep(for: .milliseconds(1100))
            withAnimation(.spring(response: 0.45, dampingFraction: 0.55)) {
                opened = true
            }
            Feedback.shared.play(.reveal(reward.rarity), enabled: store.settings.soundOn)
            Feedback.shared.impact(reward.rarity == .common ? .medium : .heavy, enabled: store.settings.hapticsOn)
            if bigReward {
                Feedback.shared.success(enabled: store.settings.hapticsOn)
            }
        }
    }
}

struct ReturnCard: View {
    @Environment(GameStore.self) private var store
    let days: Int
    let onDone: () -> Void

    var body: some View {
        CelebrationCard(color: Theme.accent, kicker: "WELCOME BACK") {
            Text("🛸")
                .font(.system(size: 52))
            Text("귀환을 환영합니다, 함장님!")
                .font(.title3.bold())
            Text("\(days)일 만이에요. 다시 출발할 수 있게 보급 캡슐 1개를 드렸어요.")
                .font(.subheadline)
                .foregroundStyle(Theme.muted)
            GoButton(title: "다시 출발", color: Theme.accent, action: onDone)
        }
        .task {
            Feedback.shared.play(.reveal(.rare), enabled: store.settings.soundOn)
            Feedback.shared.success(enabled: store.settings.hapticsOn)
        }
    }
}
