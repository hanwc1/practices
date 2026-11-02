import SwiftUI

/// "오늘" 화면: 계급·경험치, 연료, 콤보·캡슐, 오늘의 미션
struct HomeView: View {
    @Environment(GameStore.self) private var store
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    @State private var showingNew = false
    @State private var editing: Mission?
    @State private var floats: [FloatItem] = []
    @State private var shakes: CGFloat = 0
    @State private var warpID = 0
    @State private var showWarp = false

    var body: some View {
        NavigationStack {
            ZStack {
                SpaceBackground()

                VStack(spacing: 12) {
                    HeaderCard()
                    RouteCard()
                    StatusRow()
                    missionList
                }
                .padding(.horizontal, 16)
                .padding(.top, 4)
                .modifier(ShakeEffect(animatableData: shakes))

                if showWarp {
                    WarpFlash().id(warpID)
                }

                ZStack {
                    ForEach(floats) { item in
                        FloatingLabel(item: item)
                    }
                }
                .allowsHitTesting(false)
            }
            .navigationTitle("오늘의 탐사")
            .navigationBarTitleDisplayMode(.inline)
            .toolbarBackground(.hidden, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        showingNew = true
                    } label: {
                        Image(systemName: "plus.circle.fill")
                            .font(.title2)
                            .foregroundStyle(Theme.accent)
                    }
                    .accessibilityLabel("새 미션 추가")
                }
            }
            .sheet(isPresented: $showingNew) {
                MissionEditView(mission: nil)
            }
            .sheet(item: $editing) { mission in
                MissionEditView(mission: mission)
            }
            .onChange(of: store.lastEffect) { _, effect in
                if let effect {
                    play(effect)
                }
            }
        }
    }

    // MARK: 미션 목록

    private var missionList: some View {
        let missions = store.todayMissions
        let day = store.today
        return List {
            HStack {
                Text("오늘의 미션")
                Spacer()
                Text(missions.isEmpty ? "" : "탭해서 완료 · 밀어서 수정")
            }
            .font(.caption)
            .foregroundStyle(Theme.muted)
            .listRowBackground(Color.clear)
            .listRowSeparator(.hidden)
            .listRowInsets(EdgeInsets(top: 0, leading: 2, bottom: 2, trailing: 2))

            if missions.isEmpty {
                EmptyMissionsView { showingNew = true }
                    .listRowBackground(Color.clear)
                    .listRowSeparator(.hidden)
            }

            ForEach(missions) { mission in
                Button {
                    withAnimation(.spring(response: 0.35, dampingFraction: 0.8)) {
                        store.toggle(mission)
                    }
                } label: {
                    MissionRow(
                        mission: mission,
                        isMain: store.isMain(mission, on: day),
                        isDone: mission.isDone(on: day),
                        isOverdue: store.isOverdue(mission),
                        xpGained: mission.xpGained(on: day)
                    )
                }
                .buttonStyle(.plain)
                .listRowBackground(Color.clear)
                .listRowSeparator(.hidden)
                .listRowInsets(EdgeInsets(top: 3, leading: 0, bottom: 3, trailing: 0))
                .swipeActions(edge: .trailing) {
                    Button(role: .destructive) {
                        store.delete(mission.id)
                    } label: {
                        Label("삭제", systemImage: "trash")
                    }
                    Button {
                        editing = mission
                    } label: {
                        Label("수정", systemImage: "pencil")
                    }
                    .tint(.blue)
                }
                .swipeActions(edge: .leading) {
                    Button {
                        store.setMain(mission.id, on: day)
                    } label: {
                        Label("메인", systemImage: "star.fill")
                    }
                    .tint(.orange)
                }
                .contextMenu {
                    Button {
                        editing = mission
                    } label: {
                        Label("수정", systemImage: "pencil")
                    }
                    Button {
                        store.setMain(mission.id, on: day)
                    } label: {
                        Label(store.isMain(mission, on: day) ? "메인 미션 해제" : "오늘의 메인 미션으로", systemImage: "star")
                    }
                    Button(role: .destructive) {
                        store.delete(mission.id)
                    } label: {
                        Label("삭제", systemImage: "trash")
                    }
                }
            }
        }
        .listStyle(.plain)
        .scrollContentBackground(.hidden)
    }

    // MARK: 효과

    private func play(_ effect: CompletionEffect) {
        let text: String
        if effect.crit > 1 {
            text = "워프 부스트 ×\(effect.crit)  +\(effect.xp) XP"
        } else if effect.comboMultiplier > 1 {
            text = "+\(effect.xp) XP  콤보 ×\(Rules.multText(effect.comboMultiplier))"
        } else {
            text = "+\(effect.xp) XP"
        }
        addFloat(FloatItem(
            text: text,
            color: effect.crit > 1 ? Theme.gold : Theme.accent,
            big: effect.crit > 1,
            xOffset: CGFloat.random(in: -30...30)
        ))

        if effect.crit > 1 && !reduceMotion {
            withAnimation(.linear(duration: 0.35)) { shakes += 1 }
            warpID += 1
            showWarp = true
            Task {
                try? await Task.sleep(for: .milliseconds(700))
                showWarp = false
            }
        }

        if effect.gotCapsule {
            Task {
                try? await Task.sleep(for: .milliseconds(450))
                addFloat(FloatItem(text: "📦 보급 캡슐 획득!", color: Color(red: 0.76, green: 0.94, blue: 1), big: false, xOffset: 0))
            }
        }
    }

    private func addFloat(_ item: FloatItem) {
        floats.append(item)
        Task {
            try? await Task.sleep(for: .milliseconds(1600))
            floats.removeAll { $0.id == item.id }
        }
    }
}

// MARK: - 계급·경험치

struct HeaderCard: View {
    @Environment(GameStore.self) private var store

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack(alignment: .bottom) {
                VStack(alignment: .leading, spacing: 0) {
                    Text(Rules.rank(for: store.game.level))
                        .font(.caption)
                        .foregroundStyle(Theme.muted)
                    Text("Lv.\(store.game.level)")
                        .font(.system(size: 28, weight: .bold, design: .rounded))
                        .contentTransition(.numericText())
                }
                Spacer()
                VStack(alignment: .trailing, spacing: 2) {
                    Text("🔥 \(store.displayStreak)일 연속 탐사")
                        .font(.subheadline.weight(.semibold))
                        .foregroundStyle(Theme.gold)
                    Text("비상 연료 \(store.game.emergencyFuel)개")
                        .font(.caption)
                        .foregroundStyle(Theme.muted)
                }
            }
            VStack(spacing: 4) {
                HStack {
                    Text("경험치")
                    Spacer()
                    Text("\(store.game.xp) / \(Rules.xpPerLevel)")
                        .monospacedDigit()
                        .contentTransition(.numericText())
                }
                .font(.caption)
                .foregroundStyle(Theme.muted)
                ProgressBar(value: Double(store.game.xp) / Double(Rules.xpPerLevel), colors: Theme.xpColors)
            }
        }
        .animation(.spring(response: 0.4, dampingFraction: 0.8), value: store.game.xp)
    }
}

// MARK: - 연료·로켓

struct RouteCard: View {
    @Environment(GameStore.self) private var store

    var body: some View {
        let fuel = store.game.fuel
        let goal = Rules.fuelGoal
        let skin = Skins.named(store.settings.skin)

        VStack(spacing: 8) {
            HStack {
                Label("연료 \(fuel) / \(goal)", systemImage: "fuelpump.fill")
                Spacer()
                Text(fuel >= goal ? "도착!" : "미확인 행성까지 \(goal - fuel)칸")
            }
            .font(.caption)
            .foregroundStyle(Theme.muted)

            GeometryReader { geo in
                let w = geo.size.width
                ZStack {
                    Path { p in
                        p.move(to: CGPoint(x: 18, y: 18))
                        p.addLine(to: CGPoint(x: w - 18, y: 18))
                    }
                    .stroke(Color.white.opacity(0.3), style: StrokeStyle(lineWidth: 2, dash: [5, 5]))

                    Text("🌍").font(.system(size: 24)).position(x: 14, y: 18)
                    Text("❔").font(.system(size: 22)).position(x: w - 14, y: 18)
                    Text("🚀")
                        .font(.system(size: 22))
                        .rotationEffect(.degrees(45))
                        .shadow(color: skin.colors.first ?? Theme.gold, radius: 8)
                        .position(x: 18 + (w - 36) * CGFloat(fuel) / CGFloat(goal), y: 18)
                }
            }
            .frame(height: 36)
            .animation(.spring(response: 0.6, dampingFraction: 0.6), value: fuel)

            HStack(spacing: 4) {
                ForEach(0..<goal, id: \.self) { i in
                    Capsule()
                        .fill(i < fuel
                              ? AnyShapeStyle(LinearGradient(colors: skin.colors, startPoint: .leading, endPoint: .trailing))
                              : AnyShapeStyle(Color.white.opacity(0.12)))
                        .frame(height: 7)
                        .shadow(color: i < fuel ? (skin.colors.first ?? Theme.gold).opacity(0.6) : .clear, radius: 4)
                }
            }
            .animation(.spring(response: 0.4, dampingFraction: 0.6), value: fuel)
        }
        .padding(12)
        .spaceCard(stroke: Theme.accent.opacity(0.25), fill: Theme.accent.opacity(0.08))
    }
}

// MARK: - 콤보·캡슐

struct StatusRow: View {
    @Environment(GameStore.self) private var store

    var body: some View {
        HStack(spacing: 8) {
            if let last = store.game.lastCompletionAt, store.game.comboCount >= 2 {
                ComboBadge(combo: store.game.comboCount, last: last)
            }
            if store.game.capsules > 0 {
                Button {
                    store.openCapsule()
                } label: {
                    HStack(spacing: 6) {
                        Text("📦")
                        Text("캡슐 \(store.game.capsules)개 열기")
                            .font(.subheadline.weight(.semibold))
                    }
                    .foregroundStyle(Theme.ink)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 9)
                    .background(
                        RoundedRectangle(cornerRadius: 12)
                            .fill(LinearGradient(colors: [Color(red: 0.76, green: 0.94, blue: 1), Theme.accent], startPoint: .topLeading, endPoint: .bottomTrailing))
                    )
                    .shadow(color: Theme.accent.opacity(0.6), radius: 10)
                }
                .buttonStyle(.plain)
                .transition(.scale.combined(with: .opacity))
            }
        }
        .animation(.spring(response: 0.4, dampingFraction: 0.6), value: store.game.capsules)
    }
}

struct ComboBadge: View {
    let combo: Int
    let last: Date

    var body: some View {
        TimelineView(.periodic(from: .now, by: 1)) { timeline in
            let remaining = Rules.comboWindow - timeline.date.timeIntervalSince(last)
            if remaining > 0 {
                VStack(alignment: .leading, spacing: 4) {
                    Text("🔥 \(combo)콤보 · XP ×\(Rules.multText(Rules.comboMultiplier(combo)))")
                        .font(.caption.weight(.bold))
                        .foregroundStyle(Theme.combo)
                    ProgressBar(value: remaining / Rules.comboWindow, colors: [Theme.combo, Theme.gold], height: 3)
                    Text("\(Int(remaining / 60) + 1)분 안에 하나 더!")
                        .font(.caption2)
                        .foregroundStyle(Theme.muted)
                }
                .padding(.horizontal, 10)
                .padding(.vertical, 6)
                .frame(maxWidth: .infinity, alignment: .leading)
                .spaceCard(stroke: Theme.combo.opacity(0.4), fill: Theme.combo.opacity(0.12))
            }
        }
    }
}

// MARK: - 미션 한 줄

struct MissionRow: View {
    let mission: Mission
    let isMain: Bool
    let isDone: Bool
    let isOverdue: Bool
    let xpGained: Int?

    var body: some View {
        HStack(spacing: 12) {
            ZStack {
                RoundedRectangle(cornerRadius: 6)
                    .fill(isDone ? Theme.accent : Color.clear)
                RoundedRectangle(cornerRadius: 6)
                    .stroke(isDone ? Theme.accent : Theme.muted.opacity(0.8), lineWidth: 2)
                if isDone {
                    Image(systemName: "checkmark")
                        .font(.caption.weight(.heavy))
                        .foregroundStyle(Theme.ink)
                }
            }
            .frame(width: 22, height: 22)

            VStack(alignment: .leading, spacing: 2) {
                Text((isMain ? "★ " : "") + mission.title)
                    .font(.body)
                    .foregroundStyle(.white)
                    .strikethrough(isDone)
                    .opacity(isDone ? 0.5 : 1)
                    .lineLimit(2)
                HStack(spacing: 6) {
                    Text(mission.difficulty.label)
                    if let repeatText = mission.repeatText {
                        Text("🔁 \(repeatText)")
                    }
                    if let time = mission.reminderText {
                        Text("⏰ \(time)")
                    }
                    if isOverdue {
                        Text("지난 미션").foregroundStyle(Theme.combo)
                    }
                }
                .font(.caption2)
                .foregroundStyle(Theme.muted)
            }

            Spacer(minLength: 4)

            Text(rewardText)
                .font(.caption.weight(.semibold).monospacedDigit())
                .foregroundStyle(isMain ? Theme.gold : Theme.accent)
        }
        .padding(.vertical, 10)
        .padding(.horizontal, 12)
        .spaceCard(
            stroke: isMain ? Theme.gold.opacity(0.6) : Theme.cardStroke,
            fill: isMain ? Theme.gold.opacity(0.08) : Theme.card
        )
        .contentShape(Rectangle())
        .accessibilityElement(children: .combine)
        .accessibilityAddTraits(isDone ? [.isSelected] : [])
    }

    private var rewardText: String {
        if isDone { return "+\(xpGained ?? 0) XP" }
        let base = mission.difficulty.baseXP
        return isMain ? "메인 +\(base + Rules.mainBonus)" : "+\(base)"
    }
}

struct EmptyMissionsView: View {
    let onAdd: () -> Void

    var body: some View {
        VStack(spacing: 10) {
            Text("🛰️").font(.system(size: 44))
            Text("첫 미션을 추가해 보세요")
                .font(.headline)
                .foregroundStyle(.white)
            Text("미션 하나를 끝낼 때마다 연료가 한 칸씩 차고,\n다섯 칸이 차면 새 행성을 발견해요.")
                .font(.subheadline)
                .foregroundStyle(Theme.muted)
                .multilineTextAlignment(.center)
            Button(action: onAdd) {
                Text("미션 추가")
                    .font(.headline)
                    .foregroundStyle(Theme.ink)
                    .padding(.horizontal, 22)
                    .padding(.vertical, 10)
                    .background(Capsule().fill(Theme.accent))
            }
            .buttonStyle(.plain)
            .padding(.top, 4)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 28)
    }
}
