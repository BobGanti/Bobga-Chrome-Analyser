import tkinter as tk
from querybydate import QuerybyDate
from querybymonth import QuerybyMonth
from querybyrange import QuerybyRange
from startingframe import StartFrame

LARGE_FONT = ('Verdana', 12)


# app set-up
class SurfingHistory(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        tk.Tk.wm_title(self, 'Chrome Browsing History')
        tk.Tk.iconbitmap(self,)

        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for class_name in (StartFrame, QuerybyDate, QuerybyMonth, QuerybyRange):

            frame = class_name(container, self)

            self.frames[class_name] = frame

            frame.grid(row=0, column=0, sticky='nsew')

            self.show_frame(StartFrame)

    def show_frame(self, controller):  # display frames
        frame = self.frames[controller]
        frame.tkraise()


app = SurfingHistory()
app.geometry('1920x740')

app.mainloop()
