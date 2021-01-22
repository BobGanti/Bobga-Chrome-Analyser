import os
import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from querybydate import QuerybyDate
from querybymonth import QuerybyMonth
from querybyrange import QuerybyRange
from tkinter.messagebox import *
import operator
import datetime

LARGE_FONT = ('Verdana', 20)
NORMAL_FONT = ('Verdana', 14)


class StartFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ttk.Label(self).pack()
        ttk.Label(self).pack()
        ttk.Label(self).pack()

        ttk.Label(self, text='Web Surfing History', font=LARGE_FONT).pack()
        ttk.Label(self).pack()

        label = Label(self)
        label.pack()

        frame = Frame(self)
        frame.pack()
        self.btn_bydate = Button(frame, text="Day Analysis", width=20, command=lambda: self.by_date())
        self.btn_bydate.pack(side='left', fill=X, padx=10, pady=20)

        self.btn_bymonth = Button(frame, text="Month's Analysis", width=20, command=lambda: self.by_month())
        self.btn_bymonth.pack(side='left', fill=X, padx=10, pady=20)

        self.btn_byrange = Button(frame, text="Day range Analysis", width=20, command=lambda: self.by_range())
        self.btn_byrange.pack(side='left', fill=X, padx=10, pady=20)

        self.btn_quit = Button(frame, text="Quit", width=20, command=lambda: quitting())
        self.btn_quit.pack(side='left', fill=X, padx=10, pady=20)

        def quitting():
            sys.exit()

    def by_date(self):
        self.controller.show_frame(QuerybyDate)

    def by_month(self):
        self.controller.show_frame(QuerybyMonth)

    def by_range(self):
        self.controller.show_frame(QuerybyRange)
