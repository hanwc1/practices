import Foundation
import UserNotifications

/// 미션 알림, 아침 브리핑, 탐사 일지 알림을 관리합니다.
@MainActor
final class NotificationManager {
    static let shared = NotificationManager()

    static let categoryID = "MISSION"
    static let actionDone = "DONE"
    static let actionSnooze = "SNOOZE"

    private let center = UNUserNotificationCenter.current()
    private var generation = 0

    /// 알림의 [완료] [10분 뒤] 버튼 등록
    func registerCategories() {
        let done = UNNotificationAction(identifier: Self.actionDone, title: "완료", options: [])
        let snooze = UNNotificationAction(identifier: Self.actionSnooze, title: "10분 뒤", options: [])
        let category = UNNotificationCategory(identifier: Self.categoryID, actions: [done, snooze], intentIdentifiers: [], options: [])
        center.setNotificationCategories([category])
    }

    func requestAuthorization() async -> Bool {
        do {
            return try await center.requestAuthorization(options: [.alert, .sound, .badge])
        } catch {
            return false
        }
    }

    /// 앞으로 7일 동안의 미션 알림을 다시 잡습니다.
    /// 이미 끝낸 미션은 알리지 않도록, 반복 알림 대신 날짜별 알림을 만들어요.
    func reschedule(store: GameStore) {
        let requests = buildRequests(missions: store.missions, settings: store.settings, mainByDay: store.game.mainMission)
        generation += 1
        let myGeneration = generation
        Task {
            let pending = await center.pendingNotificationRequests()
            guard myGeneration == generation else { return }
            let old = pending.map { $0.identifier }.filter { $0.hasPrefix("rem-") || $0.hasPrefix("brief-") }
            center.removePendingNotificationRequests(withIdentifiers: old)
            for request in requests {
                guard myGeneration == generation else { return }
                try? await center.add(request)
            }
        }
    }

    func snooze(missionID: String, title: String, body: String) {
        let content = UNMutableNotificationContent()
        content.title = title
        content.body = body
        content.sound = .default
        content.categoryIdentifier = Self.categoryID
        content.userInfo = ["missionID": missionID]
        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 10 * 60, repeats: false)
        center.add(UNNotificationRequest(identifier: "snooze-\(missionID)", content: content, trigger: trigger))
    }

    func cancelSnooze(missionID: String) {
        center.removePendingNotificationRequests(withIdentifiers: ["snooze-\(missionID)"])
    }

    private func buildRequests(missions: [Mission], settings: AppSettings, mainByDay: [String: UUID]) -> [UNNotificationRequest] {
        let cal = Calendar.current
        let now = Date()
        let todayStart = cal.startOfDay(for: now)
        var items: [(Date, UNNotificationRequest)] = []

        for offset in 0..<7 {
            guard let day = cal.date(byAdding: .day, value: offset, to: todayStart) else { continue }
            let key = DayKey.of(day)
            for m in missions where m.reminderEnabled {
                guard m.occurs(on: day), !m.isDone(on: day) else { continue }
                guard let fire = cal.date(bySettingHour: m.reminderHour, minute: m.reminderMinute, second: 0, of: day),
                      fire > now else { continue }

                let content = UNMutableNotificationContent()
                content.title = mainByDay[key] == m.id ? "★ 메인 미션 시간이에요" : "미션 시간이에요"
                content.body = m.title
                content.sound = .default
                content.categoryIdentifier = Self.categoryID
                content.userInfo = ["missionID": m.id.uuidString]

                let comps = cal.dateComponents([.year, .month, .day, .hour, .minute], from: fire)
                let trigger = UNCalendarNotificationTrigger(dateMatching: comps, repeats: false)
                let request = UNNotificationRequest(identifier: "rem-\(m.id.uuidString)-\(key)", content: content, trigger: trigger)
                items.append((fire, request))
            }
        }

        // iOS 는 앱 하나에 알림을 64개까지만 예약할 수 있어서 가까운 것부터 채워요.
        items.sort { $0.0 < $1.0 }
        var result = items.prefix(56).map { $0.1 }

        if settings.morningOn {
            result.append(dailyRequest(
                id: "brief-morning", hour: settings.morningHour, minute: settings.morningMinute,
                title: "좋은 아침이에요, 함장님", body: "오늘의 미션을 확인하고 연료를 채워 볼까요?"
            ))
        }
        if settings.eveningOn {
            result.append(dailyRequest(
                id: "brief-evening", hour: settings.eveningHour, minute: settings.eveningMinute,
                title: "탐사 일지", body: "오늘 탐사를 돌아보고 내일 메인 미션을 골라 보세요."
            ))
        }
        return result
    }

    private func dailyRequest(id: String, hour: Int, minute: Int, title: String, body: String) -> UNNotificationRequest {
        let content = UNMutableNotificationContent()
        content.title = title
        content.body = body
        content.sound = .default
        var comps = DateComponents()
        comps.hour = hour
        comps.minute = minute
        let trigger = UNCalendarNotificationTrigger(dateMatching: comps, repeats: true)
        return UNNotificationRequest(identifier: id, content: content, trigger: trigger)
    }
}
