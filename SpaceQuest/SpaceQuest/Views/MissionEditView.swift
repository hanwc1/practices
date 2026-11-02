import SwiftUI

/// 미션 추가·수정 화면
struct MissionEditView: View {
    @Environment(GameStore.self) private var store
    @Environment(\.dismiss) private var dismiss

    private let original: Mission?
    @State private var draft: Mission
    @State private var reminderTime: Date
    @State private var makeMain = false
    @State private var confirmDelete = false

    init(mission: Mission?) {
        original = mission
        let m = mission ?? Mission(title: "")
        _draft = State(initialValue: m)
        let time = Calendar.current.date(bySettingHour: m.reminderHour, minute: m.reminderMinute, second: 0, of: Date()) ?? Date()
        _reminderTime = State(initialValue: time)
    }

    private var trimmedTitle: String {
        draft.title.trimmingCharacters(in: .whitespacesAndNewlines)
    }

    private var mainLocked: Bool {
        store.mainIsLocked(on: store.today)
    }

    private var canSave: Bool {
        !trimmedTitle.isEmpty && !(draft.repeatKind == .weekly && draft.weekdays.isEmpty)
    }

    var body: some View {
        NavigationStack {
            Form {
                Section {
                    TextField("미션 이름 (예: 영어 단어 10개)", text: $draft.title)
                    Picker("난이도", selection: $draft.difficulty) {
                        ForEach(Difficulty.allCases) { d in
                            Text(d.label).tag(d)
                        }
                    }
                    .pickerStyle(.segmented)
                } footer: {
                    Text("경험치: 쉬움 +10 · 보통 +20 · 어려움 +40")
                }

                Section("반복") {
                    Picker("반복", selection: $draft.repeatKind) {
                        ForEach(RepeatKind.allCases) { kind in
                            Text(kind.label).tag(kind)
                        }
                    }
                    if draft.repeatKind == .weekly {
                        WeekdayPicker(selection: $draft.weekdays)
                    }
                    DatePicker(
                        draft.repeatKind == .none ? "날짜" : "시작일",
                        selection: $draft.startDate,
                        displayedComponents: .date
                    )
                }

                Section("알림") {
                    Toggle("알림 받기", isOn: $draft.reminderEnabled)
                    if draft.reminderEnabled {
                        DatePicker("시간", selection: $reminderTime, displayedComponents: .hourAndMinute)
                    }
                }

                Section {
                    Toggle("오늘의 메인 미션", isOn: $makeMain)
                        .disabled(mainLocked)
                } footer: {
                    Text(mainLocked
                         ? "오늘은 메인 미션을 이미 끝내서 바꿀 수 없어요."
                         : "하루에 하나만 고를 수 있어요. 경험치 +\(Rules.mainBonus) 보너스, 캡슐이 나올 확률도 올라가요.")
                }

                if original != nil {
                    Section {
                        Button("미션 삭제", role: .destructive) {
                            confirmDelete = true
                        }
                    }
                }
            }
            .scrollContentBackground(.hidden)
            .background(SpaceBackground())
            .navigationTitle(original == nil ? "새 미션" : "미션 수정")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("취소") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("저장") { save() }
                        .disabled(!canSave)
                }
            }
            .confirmationDialog("이 미션을 삭제할까요?", isPresented: $confirmDelete, titleVisibility: .visible) {
                Button("삭제", role: .destructive) {
                    store.delete(draft.id)
                    dismiss()
                }
            }
            .onChange(of: draft.repeatKind) { _, kind in
                if kind == .weekly && draft.weekdays.isEmpty {
                    draft.weekdays = [Calendar.current.component(.weekday, from: draft.startDate)]
                }
            }
            .onAppear {
                makeMain = store.isMain(draft, on: store.today)
            }
        }
    }

    private func save() {
        var m = draft
        m.title = trimmedTitle
        let comps = Calendar.current.dateComponents([.hour, .minute], from: reminderTime)
        m.reminderHour = comps.hour ?? 9
        m.reminderMinute = comps.minute ?? 0
        m.weekdays = m.weekdays.sorted()
        store.upsert(m, makeMain: makeMain)
        dismiss()
    }
}

struct WeekdayPicker: View {
    @Binding var selection: [Int]
    private let names = ["일", "월", "화", "수", "목", "금", "토"]

    var body: some View {
        HStack(spacing: 6) {
            ForEach(1...7, id: \.self) { day in
                let isOn = selection.contains(day)
                Button {
                    if isOn {
                        selection.removeAll { $0 == day }
                    } else {
                        selection.append(day)
                    }
                } label: {
                    Text(names[day - 1])
                        .font(.subheadline.weight(.semibold))
                        .frame(maxWidth: .infinity, minHeight: 34)
                        .background(
                            RoundedRectangle(cornerRadius: 8)
                                .fill(isOn ? Theme.accent : Color.white.opacity(0.08))
                        )
                        .foregroundStyle(isOn ? Theme.ink : Color.white)
                }
                .buttonStyle(.borderless)
            }
        }
        .padding(.vertical, 2)
    }
}
