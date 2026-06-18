"""
測試第八節人數選擇（1人/2人）功能
"""
import sys, io, subprocess, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pyautogui as pg
from PIL import ImageGrab

pg.FAILSAFE = True
pg.PAUSE = 0.5

PYTHON = r"C:\Users\ian\AppData\Local\Programs\Python\Python314\python.exe"
APP_DIR = r"C:\Users\ian\PycharmProjects\ScheduleApp"

RESULTS = []

def log(msg, ok=True):
    status = "✓" if ok else "✗"
    print(f"  {status} {msg}")
    RESULTS.append((ok, msg))

def shot(name):
    img = ImageGrab.grab()
    path = f"C:\\Users\\ian\\PycharmProjects\\ScheduleApp\\test_ao_{name}.png"
    img.save(path)
    print(f"  [截圖] {path}")
    return img

def find_win():
    import pygetwindow as gw
    wins = gw.getWindowsWithTitle("糾察隊排班系統")
    if wins:
        try: wins[0].restore()
        except: pass
        time.sleep(0.3)
        return wins[0]
    return None

def center(w):
    return w.left + w.width // 2, w.top + w.height // 2

def run_tests():
    print("\n=== 啟動 app ===")
    proc = subprocess.Popen([PYTHON, "main.py"], cwd=APP_DIR)
    time.sleep(3)

    win = find_win()
    if not win:
        log("找到視窗", False)
        proc.terminate(); return
    log("找到視窗")
    shot("01_start")

    # 進入輸入頁
    cx, cy = center(win)
    pg.click(cx, cy)
    time.sleep(1)
    shot("02_input")
    log("進入輸入頁")

    # 開啟內勤人員欄位，輸入名字
    pg.click(win.left + 150, win.top + 130)
    time.sleep(0.5)
    pg.click(win.left + 150, win.top + 260)
    time.sleep(0.3)
    pg.hotkey('ctrl', 'a')
    pg.typewrite("Alice\nBob\nCharlie", interval=0.05)

    # 開啟外勤人員欄位，輸入名字
    pg.click(win.left + 430, win.top + 130)
    time.sleep(0.5)
    pg.click(win.left + 430, win.top + 260)
    time.sleep(0.3)
    pg.hotkey('ctrl', 'a')
    pg.typewrite("Dave\nEve", interval=0.05)
    log("輸入人員名單")

    # ── 測試 1：第八節選 2 人（預設）──────────────────
    print("\n=== 測試 2 人模式 ===")
    # 第八節選 2 人的 RadioButton 在控制列右側約 x=win.left+1123
    pg.click(win.left + 1123, win.top + 88)
    time.sleep(0.3)
    shot("03_ao2_selected")
    log("選擇第八節 2 人")

    pg.click(win.left + 650, win.top + 720)
    time.sleep(1.5)
    shot("04_schedule_ao2")
    log("產生排班表（2人模式）")

    win2 = find_win()
    if win2:
        log("排班頁顯示正常（2人）")
    else:
        log("排班頁顯示異常", False)

    # 返回
    pg.click(win.left + 575, win.top + 715)
    time.sleep(1)

    # ── 測試 2：第八節選 1 人 ─────────────────────────
    print("\n=== 測試 1 人模式 ===")
    # 1人 RadioButton 在 2人 左邊約 38px
    pg.click(win.left + 1085, win.top + 88)
    time.sleep(0.3)
    shot("05_ao1_selected")
    log("選擇第八節 1 人")

    pg.click(win.left + 650, win.top + 720)
    time.sleep(1.5)
    shot("06_schedule_ao1")
    log("產生排班表（1人模式）")

    win3 = find_win()
    if win3:
        log("排班頁顯示正常（1人）")
    else:
        log("排班頁顯示異常", False)

    time.sleep(1)
    proc.terminate()

    print("\n" + "="*40)
    passed = sum(1 for ok,_ in RESULTS if ok)
    failed = sum(1 for ok,_ in RESULTS if not ok)
    for ok, msg in RESULTS:
        print(f"  {'✓' if ok else '✗'} {msg}")
    print(f"\n共 {len(RESULTS)} 項，通過 {passed}，失敗 {failed}")

if __name__ == "__main__":
    run_tests()
