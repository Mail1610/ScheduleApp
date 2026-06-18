import tkinter as tk

_C = {
    "bg":        "#ffffff",
    "header":    "#e0e0e0",
    "header_fg": "#000000",
    "cell":      "#ffffff",
    "cell_alt":  "#f5f5f5",
    "cell_fg":   "#000000",
    "border":    "#888888",
    "title":     "#000000",
    "btn_bg":    "#e0e0e0",
    "btn_fg":    "#000000",
    "btn_hover": "#cccccc",
}


class SchedulePage:
    def __init__(self, canvas, app):
        self.canvas = canvas
        self.app = app
        self._table_canvas = None
        self._table_win = None

        back_btn = tk.Button(canvas, text="← 返回設定",
                             font=("微軟正黑體", 11, "bold"),
                             bg=_C["btn_bg"], fg=_C["btn_fg"],
                             activebackground=_C["btn_hover"], activeforeground="black",
                             relief="flat", bd=0, padx=18, pady=6,
                             command=self.app.show_input_page)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg=_C["btn_hover"], fg="black"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg=_C["btn_bg"], fg=_C["btn_fg"]))
        self._back_win = canvas.create_window(575, 715, window=back_btn)
        canvas.itemconfigure(self._back_win, state="hidden")

    def show(self, data):
        self._clear_table()
        self._render(data)
        self.canvas.itemconfigure(self._back_win, state="normal")

    def hide(self):
        self._clear_table()
        self.canvas.itemconfigure(self._back_win, state="hidden")

    def _clear_table(self):
        if self._table_canvas is not None:
            self._table_canvas.destroy()
            self._table_canvas = None
            self._table_win = None

    def _render(self, data):
        table_canvas = tk.Canvas(
            self.canvas,
            width=830,
            height=550,
            bg=_C["bg"],
            highlightthickness=1,
            highlightbackground=_C["border"]
        )
        self._table_canvas = table_canvas
        self._table_win = self.canvas.create_window(575, 375, window=table_canvas)

        table_canvas.create_text(
            415, 28,
            text="光復高中糾察隊排班表",
            font=("微軟正黑體", 15, "bold"),
            fill=_C["title"]
        )

        dates = data["dates"]

        def date_text(i):
            if i < len(dates):
                d = dates[i]
                return f"{d.month}/{d.day}"
            return ""

        def value(row_key, i):
            if row_key and i < len(data[row_key]):
                return data[row_key][i]
            return ""

        def draw_table(title, x, y, left_labels, row_keys, weekday_header=False):
            left_w, col_w, row_h, header_h = 108, 80, 30, 30
            total_w = left_w + col_w * 5
            total_h = header_h + row_h * len(left_labels)

            table_canvas.create_text(
                x + total_w / 2, y - 13,
                text=title,
                font=("微軟正黑體", 10, "bold"),
                fill=_C["header_fg"]
            )

            table_canvas.create_rectangle(
                x, y, x + total_w, y + total_h,
                outline=_C["border"], width=1
            )

            # 左上角標題格（斜線）
            table_canvas.create_rectangle(
                x, y, x + left_w, y + header_h,
                fill=_C["header"], outline=_C["border"]
            )
            table_canvas.create_line(
                x, y, x + left_w, y + header_h, fill=_C["border"]
            )

            # 日期/星期 header 格
            for i in range(5):
                cx = x + left_w + col_w * i
                table_canvas.create_rectangle(
                    cx, y, cx + col_w, y + header_h,
                    fill=_C["header"], outline=_C["border"]
                )
                text = ["一", "二", "三", "四", "五"][i] if weekday_header else date_text(i)
                table_canvas.create_text(
                    cx + col_w / 2, y + header_h / 2,
                    text=text, font=("微軟正黑體", 11, "bold"),
                    fill=_C["header_fg"]
                )

            # 列
            for r, label in enumerate(left_labels):
                ry = y + header_h + row_h * r
                table_canvas.create_rectangle(
                    x, ry, x + left_w, ry + row_h,
                    fill=_C["header"], outline=_C["border"]
                )
                table_canvas.create_text(
                    x + left_w / 2, ry + row_h / 2,
                    text=label, font=("微軟正黑體", 10, "bold"),
                    fill=_C["header_fg"]
                )
                for i in range(5):
                    cx = x + left_w + col_w * i
                    cell_fill = _C["cell"] if r % 2 == 0 else _C["cell_alt"]
                    table_canvas.create_rectangle(
                        cx, ry, cx + col_w, ry + row_h,
                        fill=cell_fill, outline=_C["border"]
                    )
                    if i >= len(dates):
                        table_canvas.create_line(
                            cx, ry, cx + col_w, ry + row_h, fill=_C["border"]
                        )
                        continue
                    v = value(row_keys[r], i)
                    table_canvas.create_text(
                        cx + col_w / 2, ry + row_h / 2,
                        text=v,
                        font=("微軟正黑體", 11),
                        fill=_C["cell_fg"]
                    )

        tx = 53
        ao_count = data.get("ao_count", 2)
        draw_table("上午外勤", tx, 62, ["登　雲　樓　1"], ["mo"])
        draw_table("第七節外勤", tx, 152, ["登　雲　樓"], ["so"])
        if ao_count >= 2:
            draw_table("下午外勤", tx, 242,
                       ["登　雲　樓　1", "登　雲　樓　2"], ["ao1", "ao2"],
                       weekday_header=True)
        else:
            draw_table("下午外勤", tx, 242,
                       ["登　雲　樓　1"], ["ao1"],
                       weekday_header=True)
        draw_table("早上、中午、下午內勤簽到表", tx, 372,
                   ["發　資　料", "寫　白　板", "升　旗", "降　旗"],
                   ["ni1", "ni2", "mi", "ai"])
