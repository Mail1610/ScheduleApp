import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from scheduler import Scheduler
import config_manager
from collections import defaultdict


class InputPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="black")
        self.app = app

        self.open_box = None
        self.open_header = None
        self.open_title = None

        tk.Label(
            self,
            text="糾察隊排班系統",
            font=("微軟正黑體", 24, "bold"),
            bg="black",
            fg="#00ff26"
        ).pack(pady=(25, 10))

        top_frame = tk.LabelFrame(
            self,
            text="排班設定",
            font=("微軟正黑體", 11, "bold"),
            bg="#0b0b0b",
            fg="#00ff26",
            padx=20,
            pady=12,
            bd=2,
            relief="groove"
        )
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="起始日期：", font=("微軟正黑體", 10), bg="#0b0b0b", fg="white").grid(row=0, column=0, padx=8)
        self.start = DateEntry(top_frame, width=12)
        self.start.grid(row=0, column=1, padx=8)

        tk.Label(top_frame, text="天數：", font=("微軟正黑體", 10), bg="#0b0b0b", fg="white").grid(row=0, column=2, padx=8)
        self.days = tk.Entry(top_frame, width=6)
        self.days.insert(0, "5")
        self.days.grid(row=0, column=3, padx=8)

        main_frame = tk.Frame(self, bg="black")
        main_frame.pack(pady=15)

        for i in range(4):
            main_frame.grid_columnconfigure(i, minsize=240, weight=1)

        frame1 = self.create_box(main_frame, "內勤人員", "一行一個名字", 0)
        self.indoor = tk.Text(frame1, height=7, width=28, font=("微軟正黑體", 10), bg="#050505", fg="#00ff26", insertbackground="#00ff26")
        self.indoor.pack(padx=10, pady=(5, 10))

        frame2 = self.create_box(main_frame, "外勤人員", "一行一個名字", 1)
        self.outdoor = tk.Text(frame2, height=7, width=28, font=("微軟正黑體", 10), bg="#050505", fg="#00ff26", insertbackground="#00ff26")
        self.outdoor.pack(padx=10, pady=(5, 10))

        frame3 = self.create_box(main_frame, "升旗人員", "只有這些人會排升旗", 2)
        self.flag = tk.Text( frame3, height=7,width=22,font=("微軟正黑體", 10),bg="#050505",  fg="#00ff26",insertbackground="#00ff26" )
        self.flag.pack(padx=10, pady=(5, 10))

        frame4 = self.create_box(main_frame, "指定不排班", "新增後才會生效", 3)

        tk.Label(frame4, text="選擇人員：", font=("微軟正黑體", 9), bg="#0b0b0b", fg="white").pack(anchor="w", padx=10)
        self.avoid_person = ttk.Combobox(frame4, width=22, state="readonly")
        self.avoid_person.pack(anchor="w", padx=10, pady=3)

        tk.Label(frame4, text="選擇日期：", font=("微軟正黑體", 9), bg="#0b0b0b", fg="white").pack(anchor="w", padx=10)
        self.avoid_date = DateEntry(frame4, width=12)
        self.avoid_date.pack(anchor="w", padx=10, pady=3)

        avoid_button_frame = tk.Frame(frame4, bg="#0b0b0b")
        avoid_button_frame.pack(anchor="w", padx=10, pady=5)

        add_btn = tk.Button(avoid_button_frame, text="新增", width=6, command=self.add_avoid)
        add_btn.grid(row=0, column=0, padx=3)
        self.add_hover_button_effect(add_btn)

        delete_btn = tk.Button(avoid_button_frame, text="刪除", width=6, command=self.remove_avoid)
        delete_btn.grid(row=0, column=1, padx=3)
        self.add_hover_button_effect(delete_btn)

        update_btn = tk.Button(avoid_button_frame, text="更新名單", width=8, command=self.refresh_combobox)
        update_btn.grid(row=0, column=2, padx=3)
        self.add_hover_button_effect(update_btn)

        self.avoid_listbox = tk.Listbox(frame4, height=7, width=30, font=("微軟正黑體", 10), bg="#050505", fg="#00ff26")
        self.avoid_listbox.pack(padx=10, pady=(5, 10))

        button_frame = tk.Frame(self, bg="black")
        button_frame.pack(pady=12)

        save_btn = tk.Button(button_frame, text="儲存人員", width=12, command=self.save)
        save_btn.grid(row=0, column=0, padx=10)
        self.add_hover_button_effect(save_btn)

        run_btn = tk.Button(button_frame, text="產生排班表", width=14, command=self.run)
        run_btn.grid(row=0, column=1, padx=10)
        self.add_hover_button_effect(run_btn)

        tk.Label(
            self,
            text="※ 修改人員名單後，請按「儲存人員」或「更新名單」；排班天數最多 5 天。",
            font=("微軟正黑體", 9),
            fg="#00ff26",
            bg="black"
        ).pack(pady=5)

        self.load()
        self.refresh_combobox()

    def add_hover_button_effect(self, button):
        normal_font = ("微軟正黑體", 9)
        hover_font = ("微軟正黑體", 11, "bold")

        button.config(
            font=normal_font,
            bg="#101010",
            fg="#00ff26",
            activebackground="#00ff26",
            activeforeground="black",
            relief="raised",
            bd=2
        )

        button.bind("<Enter>", lambda e: button.config(
            font=hover_font,
            bg="#00ff26",
            fg="black",
            relief="sunken"
        ))

        button.bind("<Leave>", lambda e: button.config(
            font=normal_font,
            bg="#101010",
            fg="#00ff26",
            relief="raised"
        ))

    def create_box(self, parent, title, subtitle, column):
        outer = tk.Frame(parent, bg="black")
        outer.grid(row=0, column=column, padx=8, sticky="nsew")

        header = tk.Button(
            outer,
            text=f"【{title}】",
            font=("微軟正黑體", 11, "bold"),
            bg="#101010",
            fg="#00ff26",
            activebackground="#00ff26",
            activeforeground="black",
            width=20,
            command=lambda: self.toggle_box(header, content, title)
        )
        header.pack(anchor="center")

        content = tk.LabelFrame(
            outer,
            text="",
            bg="#0b0b0b",
            fg="#00ff26",
            padx=8,
            pady=8,
            bd=2,
            relief="groove"
        )

        tk.Label(
            content,
            text=subtitle,
            font=("微軟正黑體", 9),
            fg="#8cff8c",
            bg="#0b0b0b"
        ).pack(anchor="w", padx=10)

        content.pack_forget()

        return content

    def toggle_box(self, header, content, title):
        # 如果點的是目前已打開的區塊，就關起來
        if self.open_box == content and content.winfo_ismapped():
            content.pack_forget()
            header.config(text=f"▼【{title}】")
            self.open_box = None
            self.open_header = None
            self.open_title = None
            return

        # 先關掉上一個已打開的區塊
        if self.open_box is not None and self.open_box.winfo_ismapped():
            self.open_box.pack_forget()
            self.open_header.config(text=f"▼【{self.open_title}】")

        # 打開目前點選的區塊
        content.pack(anchor="w", pady=5)
        header.config(text=f"▲【{title}】")

        self.open_box = content
        self.open_header = header
        self.open_title = title

    def get(self, box):
        return [
            x.strip()
            for x in box.get("1.0", "end").splitlines()
            if x.strip()
        ]

    def save(self):
        config_manager.save(
            self.get(self.indoor),
            self.get(self.outdoor),
            self.get(self.flag)
        )
        self.refresh_combobox()
        messagebox.showinfo("OK", "已儲存A")

    def load(self):
        c = config_manager.load()
        self.indoor.insert("1.0", "\n".join(c["indoor"]))
        self.outdoor.insert("1.0", "\n".join(c["outdoor"]))
        self.flag.insert("1.0", "\n".join(c.get("flag", [])))

    def refresh_combobox(self):
        people = self.get(self.indoor) + self.get(self.outdoor)
        self.avoid_person["values"] = people

        if people:
            self.avoid_person.current(0)
        else:
            self.avoid_person.set("")

    def add_avoid(self):
        name = self.avoid_person.get()
        date = self.avoid_date.get_date()

        if not name:
            messagebox.showerror("錯誤", "請先選擇人員")
            return

        text = f"{name},{date.month:02d}/{date.day:02d}"

        if text in self.avoid_listbox.get(0, tk.END):
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