import os
import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
import operator
import datetime
from utility import Month

LARGE_FONT = ('Verdana', 20)
NORMAL_FONT = ('Verdana', 14)


class QuerybyMonth(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ttk.Label(self).pack()
        ttk.Label(self).pack()
        ttk.Label(self).pack()

        ttk.Label(self, text='Web Surfing History', font=LARGE_FONT).pack()
        ttk.Label(self).pack()

        frame1 = Frame(self)
        frame1.pack()

        self.mm = StringVar(frame1)
        self.mm.set('select month')
        self.options_mm = ttk.OptionMenu(frame1, self.mm, 'select month', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
        self.options_mm.pack(side='left', fill=X, padx=20)

        self.yl = [2019, 2018, 2017, 2016, 2017, 2016, 2015, 2014, 2013, 1012, 1011, 1010]
        self.yy = StringVar(frame1)
        self.yy.set('select year')
        self.options_yy = ttk.OptionMenu(frame1, self.yy, 'select year', 2019, 2018, 2017, 2016, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010)
        self.options_yy.pack(side='left', fill=X, padx=20)

        frame2 = Frame(self)
        frame2.pack()

        self.btn_surf = Button(frame2, text="Analyse Chrome", width=20, command=lambda: self.get_history())
        self.btn_surf.pack(side='left', fill=X, padx=10, pady=20)

        self.btn_quit = Button(frame2, text="Quit", width=20, command=lambda: quitting())
        self.btn_quit.pack(side='left', fill=X, padx=10, pady=20)

        self.lbl_disp = Label(self, text='', font=NORMAL_FONT)
        self.lbl_disp.pack(fill=X, pady=10)

        info_board_frame = Frame(self)
        info_board_frame.pack(fill=BOTH, padx=10, expand=1)

        self.yscrollbar = Scrollbar(info_board_frame)
        self.yscrollbar.pack(side=RIGHT, fill=Y)

        self.lbox = Listbox(info_board_frame)
        self.lbox.pack(fill='both', expand=1)

        self.lbox.config(yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.config(command=self.lbox.yview)

        def quitting():
            sys.exit()

    def get_history(self):
        data_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default')
        database = os.path.join(data_path, 'history')

        month = self.mm.get()
        m_val = Month().month_value(month)
        year = self.yy.get()
        if month == 'select month' or year == 'select year':
            showerror('Error Fields', 'Choose fields')
        else:
            query_mmyy = f'{m_val}-{year}'

            url_dict = {}
            try:
                conn = sqlite3.connect(database)
                cursor = conn.cursor()
                query_wdatetime = 'SELECT u.url, v.visit_time FROM urls u JOIN visits v ON u.id = v.url;'
                cursor.execute(query_wdatetime)

                rows = cursor.fetchall()
                for row in rows:
                    url, timestamp = row[0], row[1]
                    formatted_timestamp = str(datetime.datetime(1601, 1, 1) +datetime.timedelta(microseconds=timestamp)
                    ).split('.')[0]

                    extracted_date, extracted_time = formatted_timestamp.split(' ')[0], formatted_timestamp.split(' ')[1]
                    extracted_date_split = extracted_date.split('-')
                    dd, mm, yy = extracted_date_split[2], extracted_date_split[1], extracted_date_split[0]
                    formatted_mmyy = f'{mm}-{yy}'

                    if query_mmyy == formatted_mmyy:
                        url_dict.update({url: extracted_date})

                data_set = sorted(url_dict.items(), key=operator.itemgetter(1))
                self.lbl_disp['fg'] = 'blue'
                self.lbl_disp['text'] = f'Month: {month}-{year} || Records: {len(data_set)}'
                if len(data_set) > 0:
                    for data in data_set:
                        self.lbox.insert(END, f'Date: {data[1]}     {data[0]}')
                else:
                    self.lbox.insert(END, '')
                    showwarning('Empty', f'There is no record {query_mmyy}')
            except Exception as e:
                if str(e) == 'database is locked':
                    showerror('ERROR', f'{e}. \nClose all opened Chrome')
                else:
                    showerror('ERROR', e)