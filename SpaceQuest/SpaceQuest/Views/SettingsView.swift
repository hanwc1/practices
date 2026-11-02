import SwiftUI
import UIKit
import UserNotifications

struct SettingsView: View {
    @Environment(GameStore.self) private var store
    @Environment(\.scenePhase) private var scenePhase
    @State private var authStatus: UNAuthorizationStatus = .notDetermined
    @State private var confirmReset = false

    var body: some View {
        NavigationStack {
            Form {
                Section("손맛") {
                    Toggle("효과음", isOn: binding(\.soundOn))
                    Toggle("진동", isOn: binding(\.hapticsOn))
                }

                Section {
                    notificationStatusRow
                    Toggle("아침 브리핑", isOn: binding(\.morningOn))
                    if store.settings.morningOn {
                        DatePicker("시간", selection: timeBinding(hour: \.morningHour, minute: \.morningMinute), displayedComponents: .hourAndMinute)
                    }
                    Toggle("탐사 일지 알림 (밤)", isOn: binding(\.eveningOn))
                    if store.settings.eveningOn {
                        DatePicker("시간", selection: timeBinding(hour: \.eveningHour, minute: \.eveningMinute), displayedComponents: .hourAndMinute)
                    }
                } header: {
                    Text("알림")
                } footer: {
                    Text("미션별 알림 시간은 미션을 추가하거나 수정할 때 정해요. 알림에서 바로 [완료]나 [10분 뒤]를 누를 수 있어요.")
                }

                Section("로켓 스킨") {
                    Picker("스킨", selection: binding(\.skin)) {
                        ForEach(store.game.skins, id: \.self) { name in
                            Text(name).tag(name)
                        }
                    }
                    Text("보급 캡슐에서 새 스킨이 나와요. 모은 스킨 \(store.game.skins.count) / \(Skins.all.count)")
                        .font(.footnote)
                        .foregroundStyle(Theme.muted)
                }

                Section("내 기록") {
                    LabeledContent("계급", value: "\(Rules.rank(for: store.game.level)) · Lv.\(store.game.level)")
                    LabeledContent("누적 경험치", value: "\(store.game.totalXP)")
                    LabeledContent("발견한 행성", value: "\(store.game.planets.count)개")
                    LabeledContent("우주 부품", value: "\(store.game.parts)개")
                    LabeledContent("최고 연속 탐사", value: "\(store.game.bestStreak)일")
                }

                Section {
                    probabilityRow("워프 부스트", "\(percent(Rules.critChance)) (3배는 그중 \(percent(Rules.crit3Share)))")
                    probabilityRow("콤보", "\(Int(Rules.comboWindow / 60))분 안에 연달아 · 최대 ×\(Rules.multText(Rules.comboMultipliers.last ?? 1))")
                    probabilityRow("보급 캡슐", "일반 \(percent(Rules.capsuleChance)) · 메인 \(percent(Rules.capsuleChanceMain)) · 하루 \(Rules.capsuleDailyLimit)개까지")
                    probabilityRow("캡슐 등급", weightsText(Rules.capsuleWeights))
                    probabilityRow("행성 등급", weightsText(Rules.planetWeights))
                } header: {
                    Text("확률 안내")
                }

                Section {
                    Button("모든 기록 지우기", role: .destructive) {
                        confirmReset = true
                    }
                } footer: {
                    Text("미션, 경험치, 도감이 모두 지워지고 되돌릴 수 없어요.")
                }
            }
            .scrollContentBackground(.hidden)
            .background(SpaceBackground())
            .navigationTitle("설정")
            .confirmationDialog("모든 기록을 지울까요?", isPresented: $confirmReset, titleVisibility: .visible) {
                Button("모두 지우기", role: .destructive) {
                    store.resetAll()
                }
            }
            .task { await refreshAuthStatus() }
            .onChange(of: scenePhase) { _, phase in
                if phase == .active {
                    Task { await refreshAuthStatus() }
                }
            }
        }
    }

    @ViewBuilder
    private var notificationStatusRow: some View {
        switch authStatus {
        case .denied:
            VStack(alignment: .leading, spacing: 6) {
                Text("알림이 꺼져 있어요")
                    .foregroundStyle(Theme.combo)
                Button("iPhone 설정에서 알림 켜기") {
                    if let url = URL(string: UIApplication.openSettingsURLString) {
                        UIApplication.shared.open(url)
                    }
                }
            }
        case .notDetermined:
            Button("알림 허용하기") {
                Task {
                    _ = await NotificationManager.shared.requestAuthorization()
                    await refreshAuthStatus()
                    NotificationManager.shared.reschedule(store: store)
                }
            }
        default:
            Label("알림 켜짐", systemImage: "bell.badge.fill")
                .foregroundStyle(Theme.accent)
        }
    }

    private func refreshAuthStatus() async {
        let settings = await UNUserNotificationCenter.current().notificationSettings()
        authStatus = settings.authorizationStatus
    }

    private func binding<T>(_ keyPath: WritableKeyPath<AppSettings, T>) -> Binding<T> {
        Binding(
            get: { store.settings[keyPath: keyPath] },
            set: { newValue in
                var s = store.settings
                s[keyPath: keyPath] = newValue
                store.updateSettings(s)
            }
        )
    }

    private func timeBinding(hour: WritableKeyPath<AppSettings, Int>, minute: WritableKeyPath<AppSettings, Int>) -> Binding<Date> {
        Binding(
            get: {
                Calendar.current.date(
                    bySettingHour: store.settings[keyPath: hour],
                    minute: store.settings[keyPath: minute],
                    second: 0,
                    of: Date()
                ) ?? Date()
            },
            set: { newValue in
                let comps = Calendar.current.dateComponents([.hour, .minute], from: newValue)
                var s = store.settings
                s[keyPath: hour] = comps.hour ?? 0
                s[keyPath: minute] = comps.minute ?? 0
                store.updateSettings(s)
            }
        )
    }

    private func probabilityRow(_ title: String, _ value: String) -> some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(title)
            Text(value)
                .font(.footnote)
                .foregroundStyle(Theme.muted)
        }
    }

    private func percent(_ value: Double) -> String {
        String(format: "%.0f%%", value * 100)
    }

    private func weightsText(_ table: [(Rarity, Double)]) -> String {
        let total = table.reduce(0) { $0 + $1.1 }
        return table.map { "\($0.0.label) " + String(format: "%.0f%%", $0.1 / total * 100) }.joined(separator: " · ")
    }
}
