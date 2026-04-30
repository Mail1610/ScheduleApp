import tkinter as tk
from pages.input_page import InputPage
from pages.schedule_page import SchedulePage


class ScheduleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("糾察隊排班系統")
        self.root.geometry("1150x760")

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.input_page = InputPage(self.container, self)
        self.schedule_page = SchedulePage(self.container, self)

        self.input_page.place(relwidth=1, relheight=1)
        self.schedule_page.place(relwidth=1, relheight=1)

    def show_input_page(self):
        self.input_page.tkraise()

    def show_schedule_page(self, data):
        self.schedule_page.render(data)
        self.schedule_page.tkraise()

    def run(self):
        self.show_input_page()
        self.root.mainloop()


if __name__ == "__main__":
    app = ScheduleApp()
    app.run()