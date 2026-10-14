#!/usr/bin/env python3
"""キューに入っている未投稿の回を、出す前に測る。

  python3 scripts/check_ready.py [queue.csv]

見るのは4つだけ。**どれも出てしまってからでは直せない**ので、push の前に必ず通す。
- 動画があるか（行はあるのにファイルが無いと、その日の投稿が失敗して枠が飛ぶ）
- 1080x1920 か
- ラウドネス -16.5 LUFS ±1.0（2026-08-24にRyusei承認。家族の回が -14.5 で出てしまった反省）
- 尺（🔴 合否にはしない。40秒超えは伸びないと実測で出ているが、短い側に正解は無い）
"""
import csv, glob, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
q = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob(os.path.join(ROOT, "drafts", "*-queue.csv")))[-1]

def ffprobe(path, *entries):
    out = subprocess.run(["ffprobe","-v","error",*entries,"-of","csv=p=0",path],
                         capture_output=True, text=True).stdout.strip()
    return out

def lufs(path):
    r = subprocess.run(["ffmpeg","-hide_banner","-nostats","-i",path,"-af","ebur128","-f","null","-"],
                       capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?\d+\.\d+) LUFS", r)
    return float(m[-1]) if m else None

bad = 0
print(f"{'回':22} {'尺':>7} {'LUFS':>7} {'寸法':>10}  判定")
for row in csv.DictReader(open(q)):
    if row.get("posted_at") or not row.get("slug") or row.get("status","").lower() in ("hold","skip"):
        continue
    d = os.path.join(ROOT, "posts", row["slug"])
    vids = sorted(glob.glob(os.path.join(d, "*.mp4")) + glob.glob(os.path.join(d, "*.mov")))
    if not vids:
        print(f"{row['slug']:22} {'':>7} {'':>7} {'':>10}  🔴 動画が無い"); bad += 1; continue
    v = vids[0]
    dur = float(ffprobe(v, "-show_entries", "format=duration") or 0)
    wh = ffprobe(v, "-select_streams", "v:0", "-show_entries", "stream=width,height").replace("\n", "")
    lu = lufs(v)
    msg = []
    if wh != "1080,1920": msg.append(f"🔴 寸法が {wh}")
    if lu is None or abs(lu + 16.5) > 1.0: msg.append(f"🔴 音量が {lu} LUFS（-16.5±1.0）")
    if dur > 40: msg.append("⚠️ 40秒超（9/22の実測では伸びていない）")
    if msg: bad += 1
    print(f"{row['slug']:22} {dur:6.1f}s {str(lu):>7} {wh:>10}  {' / '.join(msg) or '✅'}")
print("\n" + ("全部そのまま出せる" if bad == 0 else f"🔴 {bad}件。直してから push すること"))
sys.exit(1 if bad else 0)
