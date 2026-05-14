import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from scheduler import Scheduler
import config_manager
from collections import defaultdict

_DATE_STYLE = dict(
    background="black", foreground="#00ff26",
    fieldbackground="black", selectbackground="#003300",
    selectforeground="#00ff26", headersbackground="#001a00",
    headersforeground="#00ff26", normalbackground="black",
    normalforeground="#00ff26", weekendbackground="black",
    weekendforeground="#00aa00", othermonthforeground="#005500",
    othermonthbackground="black", othermonthweforeground="#005500",
    othermonthwebackground="black", bordercolor="#00ff26",
    disableddaybackground="black", disableddayforeground="#003300",
)

COL_XS = [150, 430, 710, 990]
COL_TITLES = ["內勤人員", "外勤人員", "限制條件", "指定不排班"]


class InputPage:
    def __init__(self, canvas, app):
        self.canvas = canvas
        self.app = app
        self._ids = []
        self._wins = []
        self._col_content = [[], [], [], []]
        self._header_btns = []
        self._open_col = None

        c = canvas

        self._ids.append(c.create_text(
            575, 35, text="糾察隊排班系統",
            font=("微軟正黑體", 24, "bold"), fill="#00ff26"))

        self._ids.append(c.create_text(
            575, 65, text="━━━━━━━━【 排班設定 】━━━━━━━━",
            font=("微軟正黑體", 11, "bold"), fill="#00ff26"))

        self._ids.append(c.create_text(
            360, 95, text="起始日期：",
            font=("微軟正黑體", 10), fill="white"))
        self.start = DateEntry(c, width=12, **_DATE_STYLE)
        self._wins.append(c.create_window(435, 95, window=self.start))

        self._ids.append(c.create_text(
            545, 95, text="天數：",
            font=("微軟正黑體", 10), fill="white"))
        self.days = tk.Entry(c, width=6, bg="black", fg="#00ff26",
                             insertbackground="#00ff26")
        self.days.insert(0, "5")
        self._wins.append(c.create_window(595, 95, window=self.days))

        self._ids.append(c.create_text(
            655, 95, text="半天：",
            font=("微軟正黑體", 10), fill="white"))
        self.half_day_vars = [tk.BooleanVar() for _ in range(5)]
        for i, var in enumerate(self.half_day_vars):
            cb = tk.Checkbutton(
                c, text=f"第{i + 1}天", variable=var,
                font=("微軟正黑體", 9),
                bg="black", fg="#00ff26",
                selectcolor="#003300",
                activebackground="black", activeforeground="#00ff26"
            )
            self._wins.append(c.create_window(720 + i * 85, 95, window=cb))

        for i, (cx, title) in enumerate(zip(COL_XS, COL_TITLES)):
            btn = tk.Button(c, text=f"━━【{title}】━━",
                            font=("微軟正黑體", 15, "bold"),
                            bg="black", fg="#00ff26",
                            activebackground="#00ff26", activeforeground="black",
                            relief="flat", bd=0, width=14,
                            command=lambda i=i: self._toggle_col(i))
            self._header_btns.append(btn)
            self._wins.append(c.create_window(cx, 130, window=btn))

        self._setup_col0()
        self._setup_col1()
        self._setup_col2()
        self._setup_col3()

        save_btn = tk.Button(c, text="儲存人員", width=12, command=self.save)
        self._style_btn(save_btn)
        self._wins.append(c.create_window(490, 710, window=save_btn))

        run_btn = tk.Button(c, text="產生排班表", width=14, command=self.run)
        self._style_btn(run_btn)
        self._wins.append(c.create_window(640, 710, window=run_btn))

        self._ids.append(c.create_text(
            575, 740,
            text="※ 修改人員名單後，請按「儲存人員」或「更新名單」；排班天數最多 5 天。",
            font=("微軟正黑體", 9), fill="#8cff8c"))

        for col_ids in self._col_content:
            for wid in col_ids:
                c.itemconfigure(wid, state="hidden")

        self.load()
        self.refresh_combobox()

    def _setup_col0(self):
        c, cx, col = self.canvas, COL_XS[0], 0
        self._col_content[col].append(c.create_text(
            cx, 162, text="一行一個名字",
            font=("微軟正黑體", 9), fill="#8cff8c"))
        self.indoor = tk.Text(c, height=7, width=18, font=("微軟正黑體", 14),
                              bg="black", fg="#00ff26", insertbackground="#00ff26")
        self._col_content[col].append(c.create_window(cx, 258, window=self.indoor))

    def _setup_col1(self):
        c, cx, col = self.canvas, COL_XS[1], 1
        self._col_content[col].append(c.create_text(
            cx, 162, text="一行一個名字",
            font=("微軟正黑體", 9), fill="#8cff8c"))
        self.outdoor = tk.Text(c, height=7, width=18, font=("微軟正黑體", 14),
                               bg="black", fg="#00ff26", insertbackground="#00ff26")
        self._col_content[col].append(c.create_window(cx, 258, window=self.outdoor))

    def _setup_col2(self):
        c, cx, col = self.canvas, COL_XS[2], 2
        self._col_content[col].append(c.create_text(
            cx, 162, text="【不能升旗人員】",
            font=("微軟正黑體", 9, "bold"), fill="#00ff26"))
        self.no_flag = tk.Text(c, height=4, width=18, font=("微軟正黑體", 14),
                               bg="black", fg="#00ff26", insertbackground="#00ff26")
        self._col_content[col].append(c.create_window(cx, 218, window=self.no_flag))
        self._col_content[col].append(c.create_text(
            cx, 282, text="【早上不能外勤】",
            font=("微軟正黑體", 9, "bold"), fill="#00ff26"))
        self.no_morning_outdoor = tk.Text(c, height=4, width=18,
                                          font=("微軟正黑體", 14),
                                          bg="black", fg="#00ff26",
                                          insertbackground="#00ff26")
        self._col_content[col].append(c.create_window(cx, 338, window=self.no_morning_outdoor))

    def _setup_col3(self):
        c, cx, col = self.canvas, COL_XS[3], 3
        self._col_content[col].append(c.create_text(
            cx - 80, 162, text="選擇人員：",
            font=("微軟正黑體", 9), fill="white", anchor="w"))
        style = ttk.Style()
        style.configure("Green.TCombobox",
                         fieldbackground="black", background="#001a00",
                         foreground="#00ff26", selectbackground="#003300",
                         selectforeground="#00ff26")
        self.avoid_person = ttk.Combobox(c, width=20, state="readonly", style="Green.TCombobox")
        self._col_content[col].append(c.create_window(cx, 182, window=self.avoid_person))
        self._col_content[col].append(c.create_text(
            cx - 80, 210, text="選擇日期：",
            font=("微軟正黑體", 9), fill="white", anchor="w"))
        self.avoid_date = DateEntry(c, width=12, **_DATE_STYLE)
        self._col_content[col].append(c.create_window(cx, 228, window=self.avoid_date))

        add_btn = tk.Button(c, text="新增", width=6, command=self.add_avoid)
        self._style_btn(add_btn)
        self._col_content[col].append(c.create_window(cx - 75, 258, window=add_btn))

        del_btn = tk.Button(c, text="刪除", width=6, command=self.remove_avoid)
        self._style_btn(del_btn)
        self._col_content[col].append(c.create_window(cx, 258, window=del_btn))

        upd_btn = tk.Button(c, text="更新名單", width=8, command=self.refresh_combobox)
        self._style_btn(upd_btn)
        self._col_content[col].append(c.create_window(cx + 85, 258, window=upd_btn))

        self.avoid_listbox = tk.Listbox(c, height=7, width=20,
                                        font=("微軟正黑體", 14),
                                        bg="black", fg="#00ff26")
        self._col_content[col].append(c.create_window(cx, 375, window=self.avoid_listbox))

    def _style_btn(self, btn):
        btn.config(font=("微軟正黑體", 9), bg="#101010", fg="#00ff26",
                   activebackground="#00ff26", activeforeground="black",
                   relief="raised", bd=2)
        btn.bind("<Enter>", lambda e: btn.config(
            font=("微軟正黑體", 11, "bold"), bg="#00ff26", fg="black", relief="sunken"))
        btn.bind("<Leave>", lambda e: btn.config(
            font=("微軟正黑體", 9), bg="#101010", fg="#00ff26", relief="raised"))

    def _toggle_col(self, col_idx):
        title = COL_TITLES[col_idx]
        btn = self._header_btns[col_idx]

        if self._open_col == col_idx:
            for wid in self._col_content[col_idx]:
                self.canvas.itemconfigure(wid, state="hidden")
            btn.config(text=f"━━【{title}】━━")
            self._open_col = None
        else:
            if self._open_col is not None:
                prev_title = COL_TITLES[self._open_col]
                for wid in self._col_content[self._open_col]:
                    self.canvas.itemconfigure(wid, state="hidden")
                self._header_btns[self._open_col].config(text=f"━━【{prev_title}】━━")
            for wid in self._col_content[col_idx]:
                self.canvas.itemconfigure(wid, state="normal")
            btn.config(text=f"━━【{title}】━━ ▲")
            self._open_col = col_idx

    def show(self):
        for wid in self._ids + self._wins:
            self.canvas.itemconfigure(wid, state="normal")
        for ci, col_ids in enumerate(self._col_content):
            state = "normal" if ci == self._open_col else "hidden"
            for wid in col_ids:
                self.canvas.itemconfigure(wid, state=state)

    def hide(self):
        for wid in self._ids + self._wins:
            self.canvas.itemconfigure(wid, state="hidden")
        for col_ids in self._col_content:
            for wid in col_ids:
                self.canvas.itemconfigure(wid, state="hidden")

    def get(self, box):
        return [x.strip() for x in box.get("1.0", "end").splitlines() if x.strip()]

    def save(self):
        config_manager.save(
            self.get(self.indoor), self.get(self.outdoor),
            self.get(self.no_flag), self.get(self.no_morning_outdoor)
        )
        self.refresh_combobox()
        messagebox.showinfo("OK", "已儲存")

    def load(self):
        c = config_manager.load()
        self.indoor.insert("1.0", "\n".join(c["indoor"]))
        self.outdoor.insert("1.0", "\n".join(c["outdoor"]))
        self.no_flag.insert("1.0", "\n".join(c.get("no_flag", [])))
        self.no_morning_outdoor.insert("1.0", "\n".join(c.get("no_morning_outdoor", [])))

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
        half_days = {i for i, var in enumerate(self.half_day_vars) if var.get()}
        sch = Scheduler(indoor, outdoor, self.parse_avoid(),
                        self.get(self.no_flag), self.get(self.no_morning_outdoor),
                        half_days)
        data = sch.generate(self.start.get_date(), days)
        self.app.show_schedule_page(data)
