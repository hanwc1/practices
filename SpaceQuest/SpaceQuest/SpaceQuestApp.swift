import Combine
import SwiftUI
import UIKit
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
    @State private var tab = ContentView.initialTab

    private static var initialTab: String {
        #if DEBUG
        return DemoMode.value(after: "-tab") ?? "home"
        #else
        return "home"
        #endif
    }

    var body: some View {
        let newPlanets = store.planets(on: store.today).count

        ZStack {
            TabView(selection: $tab) {
                HomeView()
                    .tabItem { Label("오늘", systemImage: "sparkles") }
                    .tag("home")
                DexView()
                    .tabItem { Label("도감", systemImage: "globe.asia.australia.fill") }
                    .badge(newPlanets)
                    .tag("dex")
                LogView()
                    .tabItem { Label("탐사 일지", systemImage: "book.closed.fill") }
                    .tag("log")
                SettingsView()
                    .tabItem { Label("설정", systemImage: "gearshape.fill") }
                    .tag("settings")
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
        // 앱을 켜 둔 채 자정이 지나거나 시간대가 바뀌어도 "오늘"을 맞춰요.
        .onReceive(NotificationCenter.default.publisher(for: UIApplication.significantTimeChangeNotification)) { _ in
            store.refreshDay()
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
        let dayKey = content.userInfo["day"] as? String
        let action = response.actionIdentifier
        let title = content.title
        let body = content.body

        Task { @MainActor in
            let store = GameStore.shared
            store.refreshDay()
            if let missionID, let id = UUID(uuidString: missionID),
               let mission = store.missions.first(where: { $0.id == id }),
               dayKey == nil || dayKey == store.todayKey,
               !mission.isDone(on: store.today) {
                // 오늘 알림이고 아직 안 끝낸 미션일 때만 처리해요. (어제 알림의 [완료]는 무시)
                if action == NotificationManager.actionDone {
                    store.complete(id, withFeedback: false)
                } else if action == NotificationManager.actionSnooze {
                    NotificationManager.shared.snooze(missionID: missionID, dayKey: store.todayKey, title: title, body: body)
                }
            }
            // 알림 다시 잡기가 끝난 뒤에 iOS 에 처리 완료를 알려요.
            await NotificationManager.shared.reschedule(store: store).value
            completionHandler()
        }
    }
}
