import SwiftUI

/// 행성 도감
struct DexView: View {
    @Environment(GameStore.self) private var store
    @State private var selected: Planet?

    private let columns = Array(repeating: GridItem(.flexible(), spacing: 10), count: 3)

    var body: some View {
        let planets = Array(store.game.planets.reversed())
        let legendCount = planets.filter { $0.rarity == .legend }.count
        let shown = max(12, ((planets.count + 3 + 2) / 3) * 3)

        NavigationStack {
            ZStack {
                SpaceBackground()
                ScrollView {
                    VStack(alignment: .leading, spacing: 14) {
                        Text("발견 \(planets.count) / \(Rules.dexSize) · 전설 \(legendCount)")
                            .font(.subheadline)
                            .foregroundStyle(Theme.muted)
                        LazyVGrid(columns: columns, spacing: 10) {
                            ForEach(planets) { planet in
                                Button {
                                    selected = planet
                                } label: {
                                    DexCell(planet: planet, isNew: Calendar.current.isDate(planet.discoveredAt, inSameDayAs: store.today))
                                }
                                .buttonStyle(.plain)
                            }
                            ForEach(0..<(shown - planets.count), id: \.self) { _ in
                                Text("?")
                                    .font(.title)
                                    .foregroundStyle(Theme.muted.opacity(0.5))
                                    .frame(maxWidth: .infinity, minHeight: 116)
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 14)
                                            .stroke(Theme.muted.opacity(0.3), style: StrokeStyle(lineWidth: 1, dash: [4, 4]))
                                    )
                            }
                        }
                    }
                    .padding(16)
                }
            }
            .navigationTitle("행성 도감")
            .toolbarBackground(.hidden, for: .navigationBar)
            .sheet(item: $selected) { planet in
                PlanetDetailView(planet: planet)
            }
        }
    }
}

struct DexCell: View {
    let planet: Planet
    let isNew: Bool

    var body: some View {
        VStack(spacing: 2) {
            PlanetView(planet: planet, size: 64)
            Text(planet.name)
                .font(.caption2.weight(.semibold))
                .foregroundStyle(.white)
                .lineLimit(1)
                .minimumScaleFactor(0.8)
            Text("\(planet.rarity.label) · \(planet.type)")
                .font(.system(size: 10))
                .foregroundStyle(planet.rarity.color)
                .lineLimit(2)
                .multilineTextAlignment(.center)
        }
        .padding(.vertical, 8)
        .padding(.horizontal, 4)
        .frame(maxWidth: .infinity, minHeight: 116)
        .spaceCard(stroke: planet.rarity.color.opacity(0.6))
        .overlay(alignment: .topTrailing) {
            if isNew {
                Text("NEW")
                    .font(.system(size: 9, weight: .bold))
                    .foregroundStyle(.white)
                    .padding(.horizontal, 4)
                    .background(Capsule().fill(Color(red: 1, green: 0.42, blue: 0.5)))
                    .padding(5)
            }
        }
    }
}

struct PlanetDetailView: View {
    let planet: Planet
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            ZStack {
                SpaceBackground()
                ScrollView {
                    VStack(spacing: 12) {
                        PlanetView(planet: planet, size: 220)
                            .padding(.top, 12)
                        RarityChip(text: "\(planet.rarity.label) · \(planet.type)", color: planet.rarity.color)
                        Text(planet.name)
                            .font(.title.bold())
                            .foregroundStyle(.white)
                        Text(planet.rarity.flavor)
                            .font(.subheadline)
                            .foregroundStyle(Theme.muted)
                        Text("발견한 날: \(planet.discoveredAt.formatted(date: .long, time: .omitted))")
                            .font(.subheadline)
                            .foregroundStyle(Theme.muted)

                        if !planet.missions.isEmpty {
                            VStack(alignment: .leading, spacing: 6) {
                                Text("그날 끝낸 미션")
                                    .font(.headline)
                                    .foregroundStyle(.white)
                                ForEach(planet.missions, id: \.self) { title in
                                    Label(title, systemImage: "checkmark.circle.fill")
                                        .font(.subheadline)
                                        .foregroundStyle(Theme.muted)
                                }
                            }
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .padding(14)
                            .spaceCard()
                        }
                    }
                    .padding(16)
                }
            }
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("닫기") { dismiss() }
                }
            }
        }
    }
}
