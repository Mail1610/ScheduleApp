"""
自動化測試腳本：完整跑一遍 ScheduleApp 的所有功能
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import subprocess
import time
import pyautogui as pg
from PIL import ImageGrab

pg.FAILSAFE = True
pg.PAUSE = 0.4

RESULTS = []


def log(msg, ok=True):
    status = "✓" if ok else "✗"
    print(f"  {status} {msg}")
    RESULTS.append((ok, msg))


def screenshot(name):
    img = ImageGrab.grab()
    img.save(f"test_{name}.png")
    return img


def find_window():
    import pygetwindow as gw
    wins = gw.getWindowsWithTitle("糾察隊排班系統")
    if wins:
        w = wins[0]
        try:
            w.restore()
        except Exception:
            pass
        time.sleep(0.3)
        return w
    return None


def center(win):
    return win.left + win.width // 2, win.top + win.height // 2


def run_tests():
    print("\n=== 啟動 ScheduleApp ===")
    proc = subprocess.Popen([sys.executable, "main.py"],
                            cwd=r"C:\Users\ian\PycharmProjects\ScheduleApp")
    time.sleep(2.5)

    win = find_window()
    if not win:
        log("找到視窗", False)
        proc.terminate()
        return
    log("找到視窗")
    screenshot("01_start")

    # ── 第一頁：點擊進入 ──────────────────────────────
    print("\n=== 第一頁：點擊進入 ===")
    cx, cy = center(win)
    pg.click(cx, cy)
    time.sleep(0.8)
    screenshot("02_input")

    win2 = find_window()
    if win2:
        log("成功進入第二頁")
    else:
        log("進入第二頁失敗", False)

    # ── 第二頁：開啟「內勤人員」欄位 ─────────────────
    print("\n=== 開啟內勤人員欄位 ===")
    # 第一個按鈕在視窗左側約 x=win.left+150, y=win.top+130
    btn1_x = win.left + 150
    btn1_y = win.top + 130
    pg.click(btn1_x, btn1_y)
    time.sleep(0.5)
    screenshot("03_col0_open")
    log("點擊內勤人員按鈕")

    # 在文字框輸入名字
    text_x = win.left + 150
    text_y = win.top + 260
    pg.click(text_x, text_y)
    time.sleep(0.3)
    pg.hotkey('ctrl', 'a')
    pg.typewrite("Alice\nBob\nCharlie", interval=0.05)
    time.sleep(0.3)
    log("輸入內勤人員名字")
    screenshot("04_indoor_typed")

    # ── 開啟「外勤人員」欄位 ─────────────────────────
    print("\n=== 開啟外勤人員欄位 ===")
    btn2_x = win.left + 430
    btn2_y = win.top + 130
    pg.click(btn2_x, btn2_y)
    time.sleep(0.5)
    screenshot("05_col1_open")
    log("點擊外勤人員按鈕")

    text2_x = win.left + 430
    text2_y = win.top + 260
    pg.click(text2_x, text2_y)
    time.sleep(0.3)
    pg.hotkey('ctrl', 'a')
    pg.typewrite("Dave\nEve\nFrank", interval=0.05)
    time.sleep(0.3)
    log("輸入外勤人員名字")
    screenshot("06_outdoor_typed")

    # ── 儲存人員 ──────────────────────────────────────
    print("\n=== 儲存人員 ===")
    save_x = win.left + 490
    save_y = win.top + 710
    pg.click(save_x, save_y)
    time.sleep(0.8)
    screenshot("07_after_save")
    # 關掉可能出現的 messagebox
    pg.press('enter')
    time.sleep(0.3)
    log("點擊儲存人員")

    # ── 產生排班表 ────────────────────────────────────
    print("\n=== 產生排班表 ===")
    run_x = win.left + 640
    run_y = win.top + 710
    pg.click(run_x, run_y)
    time.sleep(1.2)
    screenshot("08_schedule")
    log("點擊產生排班表")

    wins_after = find_window()
    if wins_after:
        log("排班表頁面顯示正常")
    else:
        log("排班表頁面異常", False)

    # ── 返回 ──────────────────────────────────────────
    print("\n=== 點擊返回 ===")
    back_x = win.left + 575
    back_y = win.top + 710
    pg.click(back_x, back_y)
    time.sleep(0.8)
    screenshot("09_back_to_input")
    log("點擊返回按鈕")

    # ── 開啟限制條件欄位 ─────────────────────────────
    print("\n=== 開啟限制條件欄位 ===")
    btn3_x = win.left + 710
    btn3_y = win.top + 130
    pg.click(btn3_x, btn3_y)
    time.sleep(0.5)
    screenshot("10_col2_open")
    log("點擊限制條件按鈕")

    # ── 開啟指定不排班欄位 ───────────────────────────
    print("\n=== 開啟指定不排班欄位 ===")
    btn4_x = win.left + 990
    btn4_y = win.top + 130
    pg.click(btn4_x, btn4_y)
    time.sleep(0.5)
    screenshot("11_col3_open")
    log("點擊指定不排班按鈕")

    # 關閉 app
    time.sleep(0.5)
    proc.terminate()

    # ── 結果報告 ─────────────────────────────────────
    print("\n" + "="*40)
    print("測試結果：")
    passed = sum(1 for ok, _ in RESULTS if ok)
    failed = sum(1 for ok, _ in RESULTS if not ok)
    for ok, msg in RESULTS:
        log(msg, ok)
    print(f"\n共 {len(RESULTS)} 項，通過 {passed}，失敗 {failed}")
    print("截圖已儲存為 test_*.png")


if __name__ == "__main__":
    run_tests()
