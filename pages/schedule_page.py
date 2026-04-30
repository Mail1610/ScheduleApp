import tkinter as tk


class SchedulePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

    def render(self, data):
        for w in self.winfo_children():
            w.destroy()

        tk.Label(self, text="排班表", font=("微軟正黑體", 20)).pack()

        table = tk.Frame(self)
        table.pack()

        for i, d in enumerate(data["dates"]):
            tk.Label(table, text=f"{d.month}/{d.day}").grid(row=0, column=i+1)

        rows = [
            ("上午外勤", "mo"),
            ("第七節", "so"),
            ("下午外勤", "ao"),
            ("早內", "mi"),
            ("中內", "ni"),
            ("晚內", "ai"),
        ]

        for r, (title, key) in enumerate(rows, start=1):
            tk.Label(table, text=title).grid(row=r, column=0)
            for c, val in enumerate(data[key]):
                tk.Label(table, text=val).grid(row=r, column=c+1)

        tk.Button(self, text="返回", command=self.app.show_input_page).pack()