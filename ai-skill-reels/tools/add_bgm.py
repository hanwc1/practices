# 편마다 다른 로파이 BGM을 만들어 영상에 입힘 → <이름>_bgm.mp4 (원본 무음 영상은 그대로 둠)
import json, os, subprocess, sys, tempfile
import soundfile as sf
from music import generate, SR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPISODES = {  # 폴더: (bpm, 코드 진행, 조옮김, 시드)
    "ep01_superpowers":       (88, "ii-V-I-vi", 0, 1),
    "ep02_caveman":           (82, "vi-IV-I-V", -3, 2),
    "ep03_ui_ux_pro_max":     (80, "iv-iii-ii-I", 2, 3),
    "ep04_mattpocock_skills": (84, "minor-jazz", -2, 4),
    "ep05_agent_skills":      (86, "ii-V-I-vi", 5, 5),
}

def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", path], capture_output=True, text=True)
    return float(json.loads(out.stdout)["format"]["duration"])

def main(only=None):
    for folder, (bpm, prog, key, seed) in EPISODES.items():
        if only and folder not in only: continue
        d = os.path.join(ROOT, folder); src = next(f for f in sorted(os.listdir(d)) if f.endswith(".mp4") and not f.endswith("_bgm.mp4"))
        video = os.path.join(d, src); out = video[:-4] + "_bgm.mp4"
        with tempfile.TemporaryDirectory() as tmp:
            wav = os.path.join(tmp, "bgm.wav"); sf.write(wav, generate(duration(video), bpm, prog, key, seed), SR)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", "-movflags", "+faststart", out], check=True)
        print("ok", out)

if __name__ == "__main__":
    main(sys.argv[1:] or None)
