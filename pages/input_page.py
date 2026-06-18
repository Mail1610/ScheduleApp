import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from scheduler import Scheduler
import config_manager
from collections import defaultdict

_P  = "#00ff26"   # 主要文字（原版亮綠）
_P2 = "#69f0ae"   # 次要提示文字
_PD = "#005500"   # 暗綠（非重要標籤）
_BG = "#0d150d"   # 卡片背景（極淡）
_BH = "#001a00"   # 欄位標題背景
_BD = "#1e5a1e"   # 邊框
_BI = "#060c06"   # 輸入框背景

_DATE_STYLE = dict(
    background=_BG, foreground=_P,
    fieldbackground=_BG, selectbackground="#003d1a",
    selectforeground=_P, headersbackground=_BH,
    headersforeground=_P, normalbackground=_BG,
    normalforeground=_P2, weekendbackground=_BG,
    weekendforeground="#00c853", othermonthforeground=_PD,
    othermonthbackground=_BG, othermonthweforeground=_PD,
    othermonthwebackground=_BG, bordercolor=_BD,
    disableddaybackground=_BG, disableddayforeground="#1b4a25",
)

COL_XS = [150, 430, 710, 990]
COL_TITLES = ["內勤人員", "外勤人員", "限制條件", "指定不排班"]

RESTRICTION_SLOTS = {
    "整天不排":       {"mo", "so", "ao1", "ao2", "mi", "ni1", "ni2", "ai"},
    "外勤不排":       {"mo", "so", "ao1", "ao2"},
    "內勤不排":       {"mi", "ni1", "ni2", "ai"},
    "上午外勤不排":   {"mo"},
    "第七節後外勤不排": {"so", "ao1", "ao2"},
    "下午外勤不排":   {"ao1", "ao2"},
}
RESTRICTION_TYPES = list(RESTRICTION_SLOTS.keys())


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

        # ── 頂部標題區 ──────────────────────────────────
        self._ids.append(c.create_rectangle(
            0, 0, 1150, 55, fill="#060e06", outline=""))
        self._ids.append(c.create_text(
            575, 28, text="糾察隊排班系統",
            font=("微軟正黑體", 22, "bold"), fill=_P))

        # ── 控制列（日期 / 天數 / 半天）──────────────────
        self._ids.append(c.create_rectangle(
            20, 60, 1130, 112, fill="#060e06", outline=_BD, width=1))
        self._ids.append(c.create_text(
            340, 86, text="起始日期：",
            font=("微軟正黑體", 10), fill=_P2))
        self.start = DateEntry(c, width=12, **_DATE_STYLE)
        self._wins.append(c.create_window(420, 86, window=self.start))

        self._ids.append(c.create_text(
            510, 86, text="天數：",
            font=("微軟正黑體", 10), fill=_P2))
        self.days = tk.Entry(c, width=6, bg=_BI, fg=_P,
                             insertbackground=_P,
                             relief="flat", highlightthickness=1,
                             highlightbackground=_BD, highlightcolor=_P)
        self.days.insert(0, "5")
        self._wins.append(c.create_window(562, 86, window=self.days))

        self._ids.append(c.create_text(
            618, 86, text="半天：",
            font=("微軟正黑體", 10), fill=_P2))
        self.half_day_vars = [tk.BooleanVar() for _ in range(5)]
        for i, var in enumerate(self.half_day_vars):
            cb = tk.Checkbutton(
                c, text=f"第{i + 1}天", variable=var,
                font=("微軟正黑體", 9),
                bg=_BG, fg=_P,
                selectcolor="#003d1a",
                activebackground=_BG, activeforeground=_P
            )
            self._wins.append(c.create_window(682 + i * 80, 86, window=cb))

        self._ids.append(c.create_text(
            1048, 86, text="第八節：",
            font=("微軟正黑體", 10), fill=_P2))
        self.ao_count = tk.IntVar(value=2)
        for j, (label, val) in enumerate([("1人", 1), ("2人", 2)]):
            rb = tk.Radiobutton(c, text=label, variable=self.ao_count, value=val,
                                font=("微軟正黑體", 9),
                                bg=_BG, fg=_P,
                                selectcolor="#003d1a",
                                activebackground=_BG, activeforeground=_P)
            self._wins.append(c.create_window(1085 + j * 38, 86, window=rb))

        # ── 欄位切換按鈕 ─────────────────────────────────
        for i, (cx, title) in enumerate(zip(COL_XS, COL_TITLES)):
            btn = tk.Button(c, text=f"▸  {title}",
                            font=("微軟正黑體", 13, "bold"),
                            bg=_BH, fg=_PD,
                            activebackground=_P, activeforeground="black",
                            relief="flat", bd=0, width=14,
                            command=lambda i=i: self._toggle_col(i))
            self._header_btns.append(btn)
            self._wins.append(c.create_window(cx, 128, window=btn))

        self._setup_col0()
        self._setup_col1()
        self._setup_col2()
        self._setup_col3()

        # ── 底部按鈕區 ───────────────────────────────────
        self._ids.append(c.create_rectangle(
            20, 695, 1130, 748, fill="#060e06", outline=_BD, width=1))
        save_btn = tk.Button(c, text="儲存人員", width=12, command=self.save)
        self._style_btn(save_btn)
        self._wins.append(c.create_window(490, 720, window=save_btn))

        run_btn = tk.Button(c, text="▶  產生排班表", width=15, command=self.run)
        self._style_btn(run_btn)
        self._wins.append(c.create_window(650, 720, window=run_btn))

        self._ids.append(c.create_text(
            575, 752,
            text="修改人員名單後請按「儲存人員」；排班天數最多 5 天",
            font=("微軟正黑體", 9), fill=_PD))

        for col_ids in self._col_content:
            for wid in col_ids:
                c.itemconfigure(wid, state="hidden")

        self.load()
        self.refresh_combobox()

    def _setup_col0(self):
        c, cx, col = self.canvas, COL_XS[0], 0
        self._col_content[col].append(c.create_rectangle(
            cx - 120, 148, cx + 120, 690, fill=_BG, outline=_BD, width=1))
        self._col_content[col].append(c.create_text(
            cx, 164, text="一行一個名字",
            font=("微軟正黑體", 9), fill=_PD))
        self.indoor = tk.Text(c, height=7, width=18, font=("微軟正黑體", 14),
                              bg=_BI, fg=_P, insertbackground=_P,
                              relief="flat", highlightthickness=1,
                              highlightbackground=_BD, highlightcolor=_P)
        self._col_content[col].append(c.create_window(cx, 258, window=self.indoor))

    def _setup_col1(self):
        c, cx, col = self.canvas, COL_XS[1], 1
        self._col_content[col].append(c.create_rectangle(
            cx - 120, 148, cx + 120, 690, fill=_BG, outline=_BD, width=1))
        self._col_content[col].append(c.create_text(
            cx, 164, text="一行一個名字",
            font=("微軟正黑體", 9), fill=_PD))
        self.outdoor = tk.Text(c, height=7, width=18, font=("微軟正黑體", 14),
                               bg=_BI, fg=_P, insertbackground=_P,
                               relief="flat", highlightthickness=1,
                               highlightbackground=_BD, highlightcolor=_P)
        self._col_content[col].append(c.create_window(cx, 258, window=self.outdoor))

    def _setup_col2(self):
        c, cx, col = self.canvas, COL_XS[2], 2
        self._col_content[col].append(c.create_rectangle(
            cx - 120, 148, cx + 120, 690, fill=_BG, outline=_BD, width=1))

        for label, y_label, attr, y_box in [
            ("◆ 不能升旗人員",     165, "no_flag",              210),
            ("◆ 早上不能外勤",     280, "no_morning_outdoor",   325),
            ("◆ 不能降旗人員",     395, "no_flag_down",         440),
            ("◆ 不能站第八節外勤", 510, "no_afternoon_outdoor", 555),
        ]:
            self._col_content[col].append(c.create_text(
                cx, y_label, text=label,
                font=("微軟正黑體", 10, "bold"), fill=_P))
            box = tk.Text(c, height=2, width=14, font=("微軟正黑體", 14),
                          bg=_BI, fg=_P, insertbackground=_P,
                          relief="flat", highlightthickness=1,
                          highlightbackground=_BD, highlightcolor=_P)
            setattr(self, attr, box)
            self._col_content[col].append(c.create_window(cx, y_box, window=box))

    def _setup_col3(self):
        c, cx, col = self.canvas, COL_XS[3], 3
        self._col_content[col].append(c.create_rectangle(
            cx - 120, 148, cx + 120, 690, fill=_BG, outline=_BD, width=1))

        self._col_content[col].append(c.create_text(
            cx - 80, 162, text="選擇人員：",
            font=("微軟正黑體", 9), fill=_P2, anchor="w"))
        style = ttk.Style()
        style.configure("Green.TCombobox",
                         fieldbackground=_BI, background=_BH,
                         foreground=_P, selectbackground="#003d1a",
                         selectforeground=_P)
        self.avoid_person = ttk.Combobox(c, width=20, state="readonly", style="Green.TCombobox")
        self._col_content[col].append(c.create_window(cx, 182, window=self.avoid_person))

        self._col_content[col].append(c.create_text(
            cx - 80, 210, text="選擇日期：",
            font=("微軟正黑體", 9), fill=_P2, anchor="w"))
        self.avoid_date = DateEntry(c, width=12, **_DATE_STYLE)
        self._col_content[col].append(c.create_window(cx, 228, window=self.avoid_date))

        self._col_content[col].append(c.create_text(
            cx - 80, 252, text="限制類型：",
            font=("微軟正黑體", 9), fill=_P2, anchor="w"))
        self.avoid_type = ttk.Combobox(c, width=20, state="readonly",
                                        values=RESTRICTION_TYPES, style="Green.TCombobox")
        self.avoid_type.current(0)
        self._col_content[col].append(c.create_window(cx, 270, window=self.avoid_type))

        add_btn = tk.Button(c, text="新增", width=6, command=self.add_avoid)
        self._style_btn(add_btn)
        self._col_content[col].append(c.create_window(cx - 75, 300, window=add_btn))

        del_btn = tk.Button(c, text="刪除", width=6, command=self.remove_avoid)
        self._style_btn(del_btn)
        self._col_content[col].append(c.create_window(cx, 300, window=del_btn))

        upd_btn = tk.Button(c, text="更新名單", width=8, command=self.refresh_combobox)
        self._style_btn(upd_btn)
        self._col_content[col].append(c.create_window(cx + 85, 300, window=upd_btn))

        self.avoid_listbox = tk.Listbox(c, height=7, width=28,
                                        font=("微軟正黑體", 12),
                                        bg="black", fg="#00ff26")
        self._col_content[col].append(c.create_window(cx, 415, window=self.avoid_listbox))

    def _style_btn(self, btn):
        btn.config(font=("微軟正黑體", 9, "bold"), bg=_BH, fg=_P,
                   activebackground=_P, activeforeground="black",
                   relief="flat", bd=0, padx=10, pady=4)
        btn.bind("<Enter>", lambda e: btn.config(bg=_P, fg="black"))
        btn.bind("<Leave>", lambda e: btn.config(bg=_BH, fg=_P))

    def _toggle_col(self, col_idx):
        title = COL_TITLES[col_idx]
        btn = self._header_btns[col_idx]

        if self._open_col == col_idx:
            for wid in self._col_content[col_idx]:
                self.canvas.itemconfigure(wid, state="hidden")
            btn.config(text=f"▸  {title}", bg=_BH, fg=_PD)
            self._open_col = None
        else:
            if self._open_col is not None:
                prev_title = COL_TITLES[self._open_col]
                for wid in self._col_content[self._open_col]:
                    self.canvas.itemconfigure(wid, state="hidden")
                self._header_btns[self._open_col].config(
                    text=f"▸  {prev_title}", bg=_BH, fg=_PD)
            for wid in self._col_content[col_idx]:
                self.canvas.itemconfigure(wid, state="normal")
            btn.config(text=f"▼  {title}", bg=_P, fg="black")
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
        avoid_entries = []
        for i in range(self.avoid_listbox.size()):
            parts = [p.strip() for p in self.avoid_listbox.get(i).split("|")]
            if len(parts) == 3:
                avoid_entries.append({"name": parts[0], "date": parts[1], "type": parts[2]})
        config_manager.save(
            self.get(self.indoor), self.get(self.outdoor),
            self.get(self.no_flag), self.get(self.no_morning_outdoor),
            avoid_entries,
            self.get(self.no_flag_down), self.get(self.no_afternoon_outdoor)
        )
        self.refresh_combobox()
        messagebox.showinfo("OK", "已儲存")

    def load(self):
        c = config_manager.load()
        self.indoor.insert("1.0", "\n".join(c["indoor"]))
        self.outdoor.insert("1.0", "\n".join(c["outdoor"]))
        self.no_flag.insert("1.0", "\n".join(c.get("no_flag", [])))
        self.no_morning_outdoor.insert("1.0", "\n".join(c.get("no_morning_outdoor", [])))
        self.no_flag_down.insert("1.0", "\n".join(c.get("no_flag_down", [])))
        self.no_afternoon_outdoor.insert("1.0", "\n".join(c.get("no_afternoon_outdoor", [])))
        for entry in c.get("avoid", []):
            self.avoid_listbox.insert(tk.END, f"{entry['name']} | {entry['date']} | {entry['type']}")

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
        rtype = self.avoid_type.get()
        if not name:
            messagebox.showerror("錯誤", "請先選擇人員")
            return
        text = f"{name} | {date.month:02d}/{date.day:02d} | {rtype}"
        if text in self.avoid_listbox.get(0, tk.END):
            messagebox.showwarning("提醒", "這筆限制已經存在")
            return
        self.avoid_listbox.insert(tk.END, text)

    def remove_avoid(self):
        selected = self.avoid_listbox.curselection()
        if not selected:
            messagebox.showwarning("提醒", "請先選擇要刪除的不排班項目")
            return
        self.avoid_listbox.delete(selected[0])

    def parse_avoid(self):
        m = defaultdict(lambda: defaultdict(set))
        for i in range(self.avoid_listbox.size()):
            parts = [p.strip() for p in self.avoid_listbox.get(i).split("|")]
            if len(parts) == 3:
                name, date, rtype = parts
                m[name][date] |= RESTRICTION_SLOTS.get(rtype, set())
        return {k: dict(v) for k, v in m.items()}

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
        ao_count = self.ao_count.get()
        sch = Scheduler(indoor, outdoor, self.parse_avoid(),
                        self.get(self.no_flag), self.get(self.no_morning_outdoor),
                        half_days,
                        self.get(self.no_flag_down), self.get(self.no_afternoon_outdoor),
                        ao_count=ao_count)
        data = sch.generate(self.start.get_date(), days)
        data["ao_count"] = ao_count
        self.app.show_schedule_page(data)
