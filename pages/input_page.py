import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from scheduler import Scheduler
import config_manager
from collections import defaultdict


class InputPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="排班系統", font=("微軟正黑體", 20, "bold")).pack(pady=10)

        top_frame = tk.Frame(self)
        top_frame.pack(pady=5)

        tk.Label(top_frame, text="起始日期：", font=("微軟正黑體", 10)).grid(row=0, column=0, padx=5)

        self.start = DateEntry(
            top_frame,
            width=12
        )
        self.start.grid(row=0, column=1, padx=5)

        tk.Label(top_frame, text="天數：", font=("微軟正黑體", 10)).grid(row=0, column=2, padx=5)
        self.days = tk.Entry(top_frame, width=6)
        self.days.insert(0, "5")
        self.days.grid(row=0, column=3, padx=5)

        main_frame = tk.Frame(self)
        main_frame.pack(pady=10)

        # 內勤
        frame1 = tk.Frame(main_frame)
        frame1.grid(row=0, column=0, padx=12)

        tk.Label(frame1, text="【內勤人員】", font=("微軟正黑體", 11, "bold")).pack(anchor="w")
        tk.Label(frame1, text="一行一個名字", font=("微軟正黑體", 9), fg="gray").pack(anchor="w")

        self.indoor = tk.Text(frame1, height=6, width=28, font=("微軟正黑體", 10))
        self.indoor.pack()

        # 外勤
        frame2 = tk.Frame(main_frame)
        frame2.grid(row=0, column=1, padx=12)

        tk.Label(frame2, text="【外勤人員】", font=("微軟正黑體", 11, "bold")).pack(anchor="w")
        tk.Label(frame2, text="一行一個名字", font=("微軟正黑體", 9), fg="gray").pack(anchor="w")

        self.outdoor = tk.Text(frame2, height=6, width=28, font=("微軟正黑體", 10))
        self.outdoor.pack()

        # 指定不排班
        frame3 = tk.Frame(main_frame)
        frame3.grid(row=0, column=2, padx=12)

        tk.Label(frame3, text="【指定不排班】", font=("微軟正黑體", 11, "bold")).pack(anchor="w")

        tk.Label(frame3, text="選擇人員：", font=("微軟正黑體", 9)).pack(anchor="w")
        self.avoid_person = ttk.Combobox(frame3, width=20, state="readonly")
        self.avoid_person.pack(anchor="w", pady=2)

        tk.Label(frame3, text="選擇日期：", font=("微軟正黑體", 9)).pack(anchor="w")
        self.avoid_date = DateEntry(
            frame3,
            width=8
        )
        self.avoid_date.pack(anchor="w", pady=2)

        avoid_button_frame = tk.Frame(frame3)
        avoid_button_frame.pack(anchor="w", pady=5)

        tk.Button(
            avoid_button_frame,
            text="新增",
            width=6,
            command=self.add_avoid
        ).grid(row=0, column=0, padx=3)

        tk.Button(
            avoid_button_frame,
            text="刪除",
            width=6,
            command=self.remove_avoid
        ).grid(row=0, column=1, padx=3)

        tk.Button(
            avoid_button_frame,
            text="更新名單",
            width=8,
            command=self.refresh_combobox
        ).grid(row=0, column=2, padx=3)

        self.avoid_listbox = tk.Listbox(
            frame3,
            height=6,
            width=30,
            font=("微軟正黑體", 10)
        )
        self.avoid_listbox.pack()

        button_frame = tk.Frame(self)
        button_frame.pack(pady=12)

        tk.Button(
            button_frame,
            text="儲存",
            width=10,
            command=self.save
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            button_frame,
            text="產生",
            width=10,
            command=self.run
        ).grid(row=0, column=1, padx=8)

        tk.Label(
            self,
            text="※ 修改人員名單後，請先按「儲存」或「更新名單」；排班天數最多 5 天。",
            font=("微軟正黑體", 9),
            fg="red"
        ).pack(pady=5)

        self.load()
        self.refresh_combobox()

    def get(self, box):
        return [
            x.strip()
            for x in box.get("1.0", "end").splitlines()
            if x.strip()
        ]

    def save(self):
        config_manager.save(
            self.get(self.indoor),
            self.get(self.outdoor)
        )
        self.refresh_combobox()
        messagebox.showinfo("OK", "已儲存")

    def load(self):
        c = config_manager.load()
        self.indoor.insert("1.0", "\n".join(c["indoor"]))
        self.outdoor.insert("1.0", "\n".join(c["outdoor"]))

    def refresh_combobox(self):
        people = self.get(self.indoor) + self.get(self.outdoor)
        self.avoid_person["values"] = people

        if people:
            self.avoid_person.current(0)

    def add_avoid(self):
        name = self.avoid_person.get()
        date = self.avoid_date.get_date()

        if not name:
            messagebox.showerror("錯誤", "請先選擇人員")
            return

        text = f"{name},{date.month:02d}/{date.day:02d}"

        existing = self.avoid_listbox.get(0, tk.END)
        if text in existing:
            messagebox.showwarning("提醒", "這筆不排班已經存在")
            return

        self.avoid_listbox.insert(tk.END, text)

    def remove_avoid(self):
        selected = self.avoid_listbox.curselection()

        if not selected:
            messagebox.showwarning("提醒", "請先選擇要刪除的不排班項目")
            return

        self.avoid_listbox.delete(selected[0])

    def parse_avoid(self):
        m = defaultdict(set)

        for i in range(self.avoid_listbox.size()):
            line = self.avoid_listbox.get(i)

            if "," in line:
                n, d = line.split(",", 1)
                m[n.strip()].add(d.strip())

        return m

    def run(self):
        indoor = self.get(self.indoor)
        outdoor = self.get(self.outdoor)

        if not indoor:
            messagebox.showerror("錯誤", "請輸入內勤人員")
            return

        if not outdoor:
            messagebox.showerror("錯誤", "請輸入外勤人員")
            return

        try:
            days = int(self.days.get())
        except ValueError:
            messagebox.showerror("錯誤", "天數請輸入數字")
            return

        if days < 1:
            messagebox.showerror("錯誤", "天數至少 1 天")
            return

        if days > 5:
            messagebox.showerror("錯誤", "最多 5 天")
            return

        sch = Scheduler(indoor, outdoor, self.parse_avoid())
        data = sch.generate(self.start.get_date(), days)

        self.app.show_schedule_page(data)