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
                x, y, x, y + length,
                fill="#003b00",
                width=drop["line_width"] + 7,
                tags="rain"
            )
            self.canvas.create_line(
                x, y, x, y + length,
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


class ScheduleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("糾察隊排班系統")
        self.root.geometry("1150x760")
        self.root.configure(bg="black")

        self.bg_canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.rain_background = RainBackground(self.bg_canvas, 1150, 760)

        self._setup_start_page()
        self.input_page = InputPage(self.bg_canvas, self)
        self.schedule_page = SchedulePage(self.bg_canvas, self)

    def _setup_start_page(self):
        c = self.bg_canvas
        # 隱形全螢幕點擊區（stipple 讓它不遮住雨）
        self._start_overlay = c.create_rectangle(
            0, 0, 1150, 760,
            fill="black", stipple="gray12", outline="",
            tags="start_page"
        )
        self._start_title = c.create_text(
            575, 320, text="糾察隊系統",
            font=("微軟正黑體", 58, "bold"),
            fill="#00ff26", tags="start_page"
        )
        c.create_text(
            575, 430, text="點擊任意位置進入系統",
            font=("微軟正黑體", 20),
            fill="#8cff8c", tags="start_page"
        )
        c.tag_bind("start_page", "<Button-1>", lambda e: self.show_input_page())
        c.tag_bind(self._start_title, "<Enter>",
                   lambda e: c.itemconfigure(self._start_title,
                                             font=("微軟正黑體", 66, "bold")))
        c.tag_bind(self._start_title, "<Leave>",
                   lambda e: c.itemconfigure(self._start_title,
                                             font=("微軟正黑體", 58, "bold")))

    def show_start_page(self):
        self.bg_canvas.itemconfigure("start_page", state="normal")
        self.input_page.hide()
        self.schedule_page.hide()

    def show_input_page(self):
        self.bg_canvas.itemconfigure("start_page", state="hidden")
        self.input_page.show()
        self.schedule_page.hide()

    def show_schedule_page(self, data):
        self.bg_canvas.itemconfigure("start_page", state="hidden")
        self.input_page.hide()
        self.schedule_page.show(data)

    def run(self):
        self.show_start_page()
        self.root.mainloop()


if __name__ == "__main__":
    app = ScheduleApp()
    app.run()
