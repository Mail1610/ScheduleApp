import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
import pandas as pd
from datetime import timedelta
import holidays
from collections import defaultdict
import random

tw_holidays = holidays.Taiwan()

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("勤務自動排班系統")
        self.root.geometry("700x600")

        tk.Label(root, text="勤務自動排班系統", font=("Microsoft JhengHei", 18, "bold")).pack(pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="起始日期").grid(row=0, column=0, padx=10, pady=5)
        self.start_date = DateEntry(frame, date_pattern="yyyy-mm-dd")
        self.start_date.grid(row=0, column=1)

        tk.Label(frame, text="結束日期").grid(row=1, column=0, padx=10, pady=5)
        self.end_date = DateEntry(frame, date_pattern="yyyy-mm-dd")
        self.end_date.grid(row=1, column=1)

        tk.Label(root, text="內勤人員名單，每行一位").pack()
        self.indoor_text = tk.Text(root, height=6, width=50)
        self.indoor_text.pack(pady=5)

        tk.Label(root, text="外勤人員名單，每行一位").pack()
        self.outdoor_text = tk.Text(root, height=6, width=50)
        self.outdoor_text.pack(pady=5)

        self.skip_weekend = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="六日不排班", variable=self.skip_weekend).pack()

        tk.Button(root, text="產生排班表", command=self.generate_schedule, height=2, width=20).pack(pady=20)

    def get_names(self, text_box):
        names = text_box.get("1.0", tk.END).strip().split("\n")
        return [name.strip() for name in names if name.strip()]

    def choose_person(self, people, count_map, weekly_map, week_key):
        candidates = sorted(
            people,
            key=lambda p: (weekly_map[week_key][p], count_map[p], random.random())
        )
        return candidates[0]

    def generate_schedule(self):
        indoor_people = self.get_names(self.indoor_text)
        outdoor_people = self.get_names(self.outdoor_text)

        if not indoor_people or not outdoor_people:
            messagebox.showerror("錯誤", "請輸入內勤與外勤人員名單")
            return

        start = self.start_date.get_date()
        end = self.end_date.get_date()

        if start > end:
            messagebox.showerror("錯誤", "起始日期不可晚於結束日期")
            return

        indoor_count = defaultdict(int)
        outdoor_count = defaultdict(int)
        indoor_weekly = defaultdict(lambda: defaultdict(int))
        outdoor_weekly = defaultdict(lambda: defaultdict(int))

        rows = []
        current = start

        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            weekday = current.strftime("%A")
            week_key = current.strftime("%Y-W%U")

            is_holiday = current in tw_holidays
            is_weekend = current.weekday() >= 5

            if is_holiday:
                rows.append({
                    "日期": date_str,
                    "星期": weekday,
                    "內勤": "國定假日不排",
                    "外勤": "國定假日不排",
                    "備註": tw_holidays.get(current)
                })

            elif self.skip_weekend.get() and is_weekend:
                rows.append({
                    "日期": date_str,
                    "星期": weekday,
                    "內勤": "假日不排",
                    "外勤": "假日不排",
                    "備註": "週末"
                })

            else:
                indoor_person = self.choose_person(
                    indoor_people,
                    indoor_count,
                    indoor_weekly,
                    week_key
                )

                outdoor_person = self.choose_person(
                    outdoor_people,
                    outdoor_count,
                    outdoor_weekly,
                    week_key
                )

                indoor_count[indoor_person] += 1
                outdoor_count[outdoor_person] += 1
                indoor_weekly[week_key][indoor_person] += 1
                outdoor_weekly[week_key][outdoor_person] += 1

                rows.append({
                    "日期": date_str,
                    "星期": weekday,
                    "內勤": indoor_person,
                    "外勤": outdoor_person,
                    "備註": ""
                })

            current += timedelta(days=1)

        df = pd.DataFrame(rows)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel 檔案", "*.xlsx")]
        )

        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("完成", "排班表已成功產生")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()