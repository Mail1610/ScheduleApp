import tkinter as tk
import random
from pages.input_page import InputPage
from pages.schedule_page import SchedulePage


class RainBackground:
    def __init__(self, canvas, width=1150, height=760):
        self.canvas = canvas
        self.width = width
        self.height = height

        self.drops = []
        for _ in range(120):
            self.drops.append({
                "x": random.randint(0, width),
                "y": random.randint(-height, height),
                "length": random.randint(70, 190),
                "speed": random.randint(7, 18),
                "line_width": random.choice([2, 3])
            })

        self.animate()

    def animate(self):
        self.canvas.delete("rain")

        for drop in self.drops:
            x = drop["x"]
            y = drop["y"]
            length = drop["length"]

            self.canvas.create_line(
                x, y,
                x, y + length,
                fill="#003b00",
                width=drop["line_width"] + 7,
                tags="rain"
            )

            self.canvas.create_line(
                x, y,
                x, y + length,
                fill="#00ff26",
                width=drop["line_width"],
                tags="rain"
            )

            drop["y"] += drop["speed"]

            if drop["y"] > self.height:
                drop["y"] = random.randint(-500, -50)
                drop["x"] = random.randint(0, self.width)
                drop["length"] = random.randint(70, 190)
                drop["speed"] = random.randint(7, 18)

        self.canvas.after(30, self.animate)


class StartPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="black")
        self.app = app

        self.title = tk.Label(
            self,
            text="糾察隊系統",
            font=("微軟正黑體", 42, "bold"),
            bg="black",
            fg="#00ff26"
        )
        self.title.place(relx=0.5, rely=0.42, anchor="center")

        self.hint = tk.Label(
            self,
            text="點擊任意位置進入系統",
            font=("微軟正黑體", 14),
            bg="black",
            fg="#8cff8c"
        )
        self.hint.place(relx=0.5, rely=0.55, anchor="center")

        self.bind("<Button-1>", lambda e: self.app.show_input_page())
        self.title.bind("<Button-1>", lambda e: self.app.show_input_page())
        self.hint.bind("<Button-1>", lambda e: self.app.show_input_page())

        self.bind_hover_effect(self.title, 42, 48)

    def bind_hover_effect(self, widget, normal_size, hover_size):
        widget.bind(
            "<Enter>",
            lambda e: widget.config(
                font=("微軟正黑體", hover_size, "bold")
            )
        )
        widget.bind(
            "<Leave>",
            lambda e: widget.config(
                font=("微軟正黑體", normal_size, "bold")
            )
        )


class ScheduleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("糾察隊排班系統")
        self.root.geometry("1150x760")
        self.root.configure(bg="black")

        self.bg_canvas = tk.Canvas(
            self.root,
            bg="black",
            highlightthickness=0
        )
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.rain_background = RainBackground(self.bg_canvas, 1150, 760)

        self.container = tk.Frame(self.root, bg="black")
        self.container.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=980,
            height=620
        )

        self.start_page = StartPage(self.container, self)
        self.input_page = InputPage(self.container, self)
        self.schedule_page = SchedulePage(self.container, self)

        self.start_page.place(relwidth=1, relheight=1)
        self.input_page.place(relwidth=1, relheight=1)
        self.schedule_page.place(relwidth=1, relheight=1)

    def show_start_page(self):
        self.start_page.tkraise()

    def show_input_page(self):
        self.input_page.tkraise()

    def show_schedule_page(self, data):
        self.schedule_page.render(data)
        self.schedule_page.tkraise()

    def run(self):
        self.show_start_page()
        self.root.mainloop()


if __name__ == "__main__":
    app = ScheduleApp()
    app.run()