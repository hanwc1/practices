import SwiftUI

/// 탐사 일지: 오늘 돌아보기, 최근 7일, 내일 메인 미션 고르기
struct LogView: View {
    @Environment(GameStore.self) private var store

    var body: some View {
        let cal = Calendar.current
        let today = store.today
        let tomorrow = cal.date(byAdding: .day, value: 1, to: today) ?? today

        NavigationStack {
            ZStack {
                SpaceBackground()
                ScrollView {
                    VStack(spacing: 16) {
                        todayCard(today)
                        WeekChart(today: today)
                        tomorrowCard(tomorrow)
                    }
                    .padding(16)
                }
            }
            .navigationTitle("탐사 일지")
            .toolbarBackground(.hidden, for: .navigationBar)
        }
    }

    private func todayCard(_ today: Date) -> some View {
        let done = store.completedCount(on: today)
        let total = store.missionsShown(on: today).count
        let planets = store.planets(on: today)

        return VStack(alignment: .leading, spacing: 12) {
            Text("오늘의 탐사")
                .font(.headline)
                .foregroundStyle(.white)
            HStack(spacing: 10) {
                StatTile(title: "완료한 미션", value: "\(done) / \(total)")
                StatTile(title: "얻은 경험치", value: "\(store.xpEarned(on: today))")
                StatTile(title: "연속 탐사", value: "\(store.displayStreak)일")
            }
            if planets.isEmpty {
                Text(done == 0 ? "아직 오늘 끝낸 미션이 없어요. 하나만 해도 연속 탐사가 이어져요." : "연료가 \(Rules.fuelGoal - store.game.fuel)칸 더 차면 새 행성을 발견해요.")
                    .font(.subheadline)
                    .foregroundStyle(Theme.muted)
            } else {
                HStack(spacing: 10) {
                    ForEach(planets) { planet in
                        PlanetView(planet: planet, size: 44)
                    }
                    Text("오늘 발견한 행성 \(planets.count)개")
                        .font(.subheadline)
                        .foregroundStyle(Theme.muted)
                }
            }
            Text("최고 기록: \(store.game.bestStreak)일 연속")
                .font(.caption)
                .foregroundStyle(Theme.muted)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(16)
        .spaceCard()
    }

    private func tomorrowCard(_ tomorrow: Date) -> some View {
        let candidates = store.missions.filter { $0.occurs(on: tomorrow) }

        return VStack(alignment: .leading, spacing: 10) {
            Text("내일 메인 미션 고르기")
                .font(.headline)
                .foregroundStyle(.white)
            Text("미리 골라 두면 내일 아침 바로 시작할 수 있어요. 메인 미션은 경험치 +\(Rules.mainBonus)에 캡슐도 잘 나와요.")
                .font(.subheadline)
                .foregroundStyle(Theme.muted)
            if candidates.isEmpty {
                Text("내일 예정된 미션이 없어요. 오늘 화면에서 미션을 추가할 때 날짜를 내일로 하거나 반복을 설정해 보세요.")
                    .font(.subheadline)
                    .foregroundStyle(Theme.muted)
            } else {
                ForEach(candidates) { mission in
                    let chosen = store.isMain(mission, on: tomorrow)
                    Button {
                        store.setMain(mission.id, on: tomorrow)
                    } label: {
                        HStack {
                            Image(systemName: chosen ? "star.fill" : "star")
                                .foregroundStyle(chosen ? Theme.gold : Theme.muted)
                            Text(mission.title)
                                .foregroundStyle(.white)
                            Spacer()
                        }
                        .padding(12)
                        .spaceCard(
                            stroke: chosen ? Theme.gold.opacity(0.6) : Theme.cardStroke,
                            fill: chosen ? Theme.gold.opacity(0.1) : Theme.card
                        )
                    }
                    .buttonStyle(.plain)
                }
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(16)
        .spaceCard()
    }
}

struct StatTile: View {
    let title: String
    let value: String

    var body: some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(value)
                .font(.title3.bold().monospacedDigit())
                .foregroundStyle(.white)
                .lineLimit(1)
                .minimumScaleFactor(0.7)
            Text(title)
                .font(.caption)
                .foregroundStyle(Theme.muted)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(10)
        .spaceCard()
    }
}

/// 최근 7일 완료 수 막대
struct WeekChart: View {
    @Environment(GameStore.self) private var store
    let today: Date

    var body: some View {
        let cal = Calendar.current
        let days: [Date] = (0..<7).reversed().compactMap { cal.date(byAdding: .day, value: -$0, to: today) }
        let counts = days.map { store.completedCount(on: $0) }
        let maxCount = max(counts.max() ?? 0, 1)

        VStack(alignment: .leading, spacing: 12) {
            Text("최근 7일")
                .font(.headline)
                .foregroundStyle(.white)
            HStack(alignment: .bottom, spacing: 8) {
                ForEach(Array(days.enumerated()), id: \.offset) { index, day in
                    VStack(spacing: 4) {
                        Text("\(counts[index])")
                            .font(.caption2.monospacedDigit())
                            .foregroundStyle(Theme.muted)
                        RoundedRectangle(cornerRadius: 4)
                            .fill(index == days.count - 1 ? Theme.accent : Theme.accent.opacity(0.45))
                            .frame(height: max(4, CGFloat(counts[index]) / CGFloat(maxCount) * 90))
                        Text(day.formatted(.dateTime.weekday(.narrow)))
                            .font(.caption2)
                            .foregroundStyle(index == days.count - 1 ? .white : Theme.muted)
                    }
                    .frame(maxWidth: .infinity)
                }
            }
            .frame(height: 130, alignment: .bottom)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(16)
        .spaceCard()
    }
}
