import tkinter as tk


class SchedulePage:
    def __init__(self, canvas, app):
        self.canvas = canvas
        self.app = app
        self._table_canvas = None
        self._table_win = None

        back_btn = tk.Button(canvas, text="返回",
                             font=("微軟正黑體", 12, "bold"),
                             bg="#101010", fg="#00ff26",
                             activebackground="#00ff26", activeforeground="black",
                             relief="raised", bd=2,
                             command=self.app.show_input_page)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#00ff26", fg="black"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#101010", fg="#00ff26"))
        self._back_win = canvas.create_window(575, 710, window=back_btn)
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
            width=820,
            height=520,
            bg="white",
            highlightthickness=0
        )
        self._table_canvas = table_canvas
        self._table_win = self.canvas.create_window(
            575, 390, window=table_canvas
        )

        table_canvas.create_text(
            410, 30,
            text="光復高中糾察隊",
            font=("微軟正黑體", 13, "bold")
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
            table_canvas.create_text(
                x + 300, y - 14,
                text=title,
                font=("微軟正黑體", 11, "bold")
            )

            left_w, col_w, row_h, header_h = 105, 78, 28, 28
            total_w = left_w + col_w * 5
            total_h = header_h + row_h * len(left_labels)

            table_canvas.create_rectangle(
                x, y, x + total_w, y + total_h,
                outline="black", width=2
            )

            table_canvas.create_rectangle(
                x, y, x + left_w, y + header_h,
                fill="#bfbfbf", outline="black"
            )
            table_canvas.create_line(
                x, y, x + left_w, y + header_h, fill="black"
            )

            for i in range(5):
                cx = x + left_w + col_w * i
                table_canvas.create_rectangle(
                    cx, y, cx + col_w, y + header_h,
                    fill="#bfbfbf", outline="black"
                )
                text = ["一", "二", "三", "四", "五"][i] if weekday_header else date_text(i)
                table_canvas.create_text(
                    cx + col_w / 2, y + header_h / 2,
                    text=text, font=("微軟正黑體", 11, "bold")
                )

            for r, label in enumerate(left_labels):
                ry = y + header_h + row_h * r
                table_canvas.create_rectangle(
                    x, ry, x + left_w, ry + row_h,
                    fill="#bfbfbf", outline="black"
                )
                table_canvas.create_text(
                    x + left_w / 2, ry + row_h / 2,
                    text=label, font=("微軟正黑體", 10, "bold")
                )
                for i in range(5):
                    cx = x + left_w + col_w * i
                    table_canvas.create_rectangle(
                        cx, ry, cx + col_w, ry + row_h,
                        fill="white", outline="black"
                    )
                    if i >= len(dates):
                        table_canvas.create_line(
                            cx, ry, cx + col_w, ry + row_h, fill="black"
                        )
                        continue
                    table_canvas.create_text(
                        cx + col_w / 2, ry + row_h / 2,
                        text=value(row_keys[r], i),
                        font=("微軟正黑體", 11)
                    )

        table_x = 130
        draw_table("上午外勤", table_x, 70, ["登　雲　樓　1"], ["mo"])
        draw_table("第七節外勤", table_x, 150, ["登　雲　樓"], ["so"])
        draw_table("下午外勤", table_x, 230,
                   ["登　雲　樓　1", "登　雲　樓　2"], ["ao1", "ao2"],
                   weekday_header=True)
        draw_table("早上、中午、下午內勤簽到表", table_x, 350,
                   ["發　資　料", "寫　白　板", "升　旗", "降　旗"],
                   ["ni1", "ni2", "mi", "ai"])
