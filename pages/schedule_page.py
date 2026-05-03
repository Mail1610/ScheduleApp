import tkinter as tk


class SchedulePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="black")
        self.app = app

    def render(self, data):
        for widget in self.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(
            self,
            width=820,
            height=520,
            bg="white",
            highlightthickness=0
        )
        canvas.place(relx=0.5, rely=0.47, anchor="center")

        canvas.create_text(
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
            canvas.create_text(
                x + 300,
                y - 14,
                text=title,
                font=("微軟正黑體", 11, "bold")
            )

            left_w = 105
            col_w = 78
            row_h = 28
            header_h = 28

            total_w = left_w + col_w * 5
            total_h = header_h + row_h * len(left_labels)

            canvas.create_rectangle(
                x, y,
                x + total_w,
                y + total_h,
                outline="black",
                width=2
            )

            canvas.create_rectangle(
                x, y,
                x + left_w,
                y + header_h,
                fill="#bfbfbf",
                outline="black"
            )
            canvas.create_line(
                x, y,
                x + left_w,
                y + header_h,
                fill="black"
            )

            for i in range(5):
                cx = x + left_w + col_w * i

                canvas.create_rectangle(
                    cx, y,
                    cx + col_w,
                    y + header_h,
                    fill="#bfbfbf",
                    outline="black"
                )

                text = ["一", "二", "三", "四", "五"][i] if weekday_header else date_text(i)

                canvas.create_text(
                    cx + col_w / 2,
                    y + header_h / 2,
                    text=text,
                    font=("微軟正黑體", 11, "bold")
                )

            for r, label in enumerate(left_labels):
                ry = y + header_h + row_h * r

                canvas.create_rectangle(
                    x, ry,
                    x + left_w,
                    ry + row_h,
                    fill="#bfbfbf",
                    outline="black"
                )

                canvas.create_text(
                    x + left_w / 2,
                    ry + row_h / 2,
                    text=label,
                    font=("微軟正黑體", 10, "bold")
                )

                for i in range(5):
                    cx = x + left_w + col_w * i

                    canvas.create_rectangle(
                        cx, ry,
                        cx + col_w,
                        ry + row_h,
                        fill="white",
                        outline="black"
                    )

                    if i >= len(dates):
                        canvas.create_line(
                            cx, ry,
                            cx + col_w,
                            ry + row_h,
                            fill="black"
                        )
                        continue

                    canvas.create_text(
                        cx + col_w / 2,
                        ry + row_h / 2,
                        text=value(row_keys[r], i),
                        font=("微軟正黑體", 11)
                    )

        table_x = 130

        draw_table(
            title="上午外勤",
            x=table_x,
            y=70,
            left_labels=["登　雲　樓　1"],
            row_keys=["mo"]
        )

        draw_table(
            title="第七節外勤",
            x=table_x,
            y=150,
            left_labels=["登　雲　樓"],
            row_keys=["so"]
        )

        draw_table(
            title="下午外勤",
            x=table_x,
            y=230,
            left_labels=["登　雲　樓　1", "登　雲　樓　2"],
            row_keys=["ao1", "ao2"],
            weekday_header=True
        )

        draw_table(
            title="早上、中午、下午內勤簽到表",
            x=table_x,
            y=350,
            left_labels=[
                "發　資　料",
                "寫　白　板",
                "升　旗",
                "降　旗"
            ],
            row_keys=["ni1", "ni2", "mi", "ai"]
        )

        back_btn = tk.Button(
            self,
            text="返回",
            font=("微軟正黑體", 12, "bold"),
            command=self.app.show_input_page
        )
        back_btn.place(relx=0.5, rely=0.90, anchor="center")