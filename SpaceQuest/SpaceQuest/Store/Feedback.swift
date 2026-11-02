import AVFoundation
import UIKit

/// 진동과 효과음. 효과음은 파일 없이 코드로 직접 만들어요.
@MainActor
final class Feedback {
    static let shared = Feedback()

    enum Sound {
        case done(combo: Int)
        case crit
        case drop
        case shake
        case reveal(Rarity)
        case planet
        case level

        var key: String {
            switch self {
            case .done(let combo): return "done-\(min(combo, 8))"
            case .crit: return "crit"
            case .drop: return "drop"
            case .shake: return "shake"
            case .reveal(let r): return "reveal-\(r.rawValue)"
            case .planet: return "planet"
            case .level: return "level"
            }
        }

        var notes: [Note] {
            switch self {
            case .done(let combo):
                // 콤보가 이어질수록 음이 조금씩 올라가요
                let m = 1 + 0.06 * Double(max(0, min(combo, 8) - 1))
                return [
                    Note(freq: 660 * m, start: 0, duration: 0.12, wave: .triangle, gain: 0.5),
                    Note(freq: 990 * m, start: 0.07, duration: 0.18, wave: .triangle, gain: 0.5)
                ]
            case .crit:
                return [523.0, 659, 784, 1047].enumerated().map {
                    Note(freq: $0.element, start: Double($0.offset) * 0.05, duration: 0.32, wave: .square, gain: 0.18)
                }
            case .drop:
                return [
                    Note(freq: 1200, start: 0, duration: 0.08, wave: .square, gain: 0.15),
                    Note(freq: 1600, start: 0.06, duration: 0.12, wave: .square, gain: 0.15)
                ]
            case .shake:
                return (0..<7).map {
                    Note(freq: 170 + Double($0) * 22, start: Double($0) * 0.14, duration: 0.07, wave: .square, gain: 0.15)
                }
            case .reveal(let rarity):
                let count: Int
                switch rarity {
                case .common: count = 2
                case .rare: count = 3
                case .epic: count = 4
                case .legend: count = 6
                }
                return (0..<count).map {
                    Note(freq: 523 * pow(1.26, Double($0)), start: Double($0) * 0.08, duration: 0.28, wave: .triangle, gain: 0.45)
                }
            case .planet:
                return [392.0, 523, 659, 784, 1047].enumerated().map {
                    Note(freq: $0.element, start: Double($0.offset) * 0.1, duration: 0.4, wave: .triangle, gain: 0.45)
                }
            case .level:
                return [523.0, 523, 784, 1047].enumerated().map {
                    Note(freq: $0.element, start: Double($0.offset) * 0.12, duration: 0.3, wave: .square, gain: 0.18)
                }
            }
        }
    }

    private var players: [AVAudioPlayer] = []
    private var cache: [String: Data] = [:]

    private init() {
        // 무음 모드를 따르고, 듣고 있던 음악은 멈추지 않아요.
        try? AVAudioSession.sharedInstance().setCategory(.ambient, mode: .default, options: [.mixWithOthers])
    }

    func play(_ sound: Sound, enabled: Bool) {
        guard enabled else { return }
        let key = sound.key
        let data: Data
        if let cached = cache[key] {
            data = cached
        } else {
            data = Synth.wav(sound.notes)
            cache[key] = data
        }
        guard let player = try? AVAudioPlayer(data: data) else { return }
        player.volume = 0.8
        player.play()
        players.removeAll { !$0.isPlaying }
        players.append(player)
    }

    func impact(_ style: UIImpactFeedbackGenerator.FeedbackStyle, enabled: Bool) {
        guard enabled else { return }
        UIImpactFeedbackGenerator(style: style).impactOccurred()
    }

    func success(enabled: Bool) {
        guard enabled else { return }
        UINotificationFeedbackGenerator().notificationOccurred(.success)
    }

    /// 미션 완료 손맛
    func completion(crit: Bool, combo: Int, capsule: Bool, settings: AppSettings) {
        if crit {
            impact(.heavy, enabled: settings.hapticsOn)
            play(.crit, enabled: settings.soundOn)
        } else {
            impact(.medium, enabled: settings.hapticsOn)
            play(.done(combo: combo), enabled: settings.soundOn)
        }
        if capsule {
            Task { @MainActor in
                try? await Task.sleep(for: .milliseconds(450))
                self.impact(.rigid, enabled: settings.hapticsOn)
                self.play(.drop, enabled: settings.soundOn)
            }
        }
    }
}

// MARK: - 간단한 신시사이저

enum Wave {
    case sine, triangle, square
}

struct Note {
    let freq: Double
    let start: Double
    let duration: Double
    let wave: Wave
    let gain: Double
}

enum Synth {
    static let sampleRate = 44_100

    /// 음표들을 16비트 WAV 데이터로 만듭니다.
    static func wav(_ notes: [Note]) -> Data {
        let rate = Double(sampleRate)
        let total = (notes.map { $0.start + $0.duration }.max() ?? 0.1) + 0.05
        let count = Int(total * rate)
        var buffer = [Double](repeating: 0, count: count)

        for note in notes {
            let startIndex = Int(note.start * rate)
            let length = Int(note.duration * rate)
            for i in 0..<length {
                let index = startIndex + i
                if index >= count { break }
                let t = Double(i) / rate
                let phase = 2 * Double.pi * note.freq * t
                let raw: Double
                switch note.wave {
                case .sine: raw = sin(phase)
                case .triangle: raw = (2 / Double.pi) * asin(sin(phase))
                case .square: raw = sin(phase) >= 0 ? 0.6 : -0.6
                }
                let attack = min(1, t / 0.008)
                let release = pow(max(0, 1 - t / note.duration), 2)
                buffer[index] += raw * attack * release * note.gain
            }
        }

        var data = Data()
        func put<T: FixedWidthInteger>(_ value: T) {
            var little = value.littleEndian
            withUnsafeBytes(of: &little) { data.append(contentsOf: $0) }
        }
        let dataSize = UInt32(count * 2)
        data.append(contentsOf: Array("RIFF".utf8))
        put(UInt32(36) + dataSize)
        data.append(contentsOf: Array("WAVE".utf8))
        data.append(contentsOf: Array("fmt ".utf8))
        put(UInt32(16))                 // fmt 크기
        put(UInt16(1))                  // PCM
        put(UInt16(1))                  // 모노
        put(UInt32(sampleRate))
        put(UInt32(sampleRate * 2))     // 초당 바이트
        put(UInt16(2))                  // 블록 크기
        put(UInt16(16))                 // 비트 수
        data.append(contentsOf: Array("data".utf8))
        put(dataSize)
        for value in buffer {
            let clipped = max(-1, min(1, value))
            put(Int16(clipped * 32_000))
        }
        return data
    }
}
