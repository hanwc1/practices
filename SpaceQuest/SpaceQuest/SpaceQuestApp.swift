import SwiftUI
import UserNotifications

@main
struct SpaceQuestApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) private var appDelegate
    @State private var store = GameStore.shared
    @Environment(\.scenePhase) private var scenePhase

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(store)
                .preferredColorScheme(.dark)
        }
        .onChange(of: scenePhase) { _, phase in
            if phase == .active {
                store.refreshDay()
            }
        }
    }
}

struct ContentView: View {
    @Environment(GameStore.self) private var store

    var body: some View {
        let newPlanets = store.planets(on: store.today).count

        ZStack {
            TabView {
                HomeView()
                    .tabItem { Label("오늘", systemImage: "sparkles") }
                DexView()
                    .tabItem { Label("도감", systemImage: "globe.asia.australia.fill") }
                    .badge(newPlanets)
                LogView()
                    .tabItem { Label("탐사 일지", systemImage: "book.closed.fill") }
                SettingsView()
                    .tabItem { Label("설정", systemImage: "gearshape.fill") }
            }
            .tint(Theme.accent)

            if let item = store.celebrations.first {
                CelebrationOverlay(item: item)
                    .id(item.id)
                    .transition(.opacity)
                    .zIndex(10)
            }
        }
        .animation(.easeInOut(duration: 0.25), value: store.celebrations.first?.id)
        .task {
            await store.requestNotificationsIfNeeded()
        }
    }
}

/// 알림에서 [완료] [10분 뒤]를 눌렀을 때 처리
final class AppDelegate: NSObject, UIApplicationDelegate, UNUserNotificationCenterDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]? = nil
    ) -> Bool {
        UNUserNotificationCenter.current().delegate = self
        Task { @MainActor in
            NotificationManager.shared.registerCategories()
        }
        return true
    }

    // 앱을 쓰는 중에도 알림 배너를 보여 줘요
    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification,
        withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void
    ) {
        completionHandler([.banner, .sound, .list])
    }

    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse,
        withCompletionHandler completionHandler: @escaping () -> Void
    ) {
        let content = response.notification.request.content
        let missionID = content.userInfo["missionID"] as? String
        let action = response.actionIdentifier
        let title = content.title
        let body = content.body

        Task { @MainActor in
            if let missionID, let id = UUID(uuidString: missionID) {
                let store = GameStore.shared
                store.refreshDay()
                if action == NotificationManager.actionDone {
                    store.complete(id, withFeedback: false)
                } else if action == NotificationManager.actionSnooze {
                    NotificationManager.shared.snooze(missionID: missionID, title: title, body: body)
                }
            }
            completionHandler()
        }
    }
}
