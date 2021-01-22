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


class QuerybyRange(tk.Frame):

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

        label1 = Label(frame1, text='Start Date', font=NORMAL_FONT)
        label1.pack()

        self.dd = StringVar(frame1)
        self.dd.set('select day')
        self.options = ttk.OptionMenu(frame1, self.dd, 'select day', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                      16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
        self.options.pack(side='left', fill=X, padx=20)

        self.mm = StringVar(frame1)
        self.mm.set('select month')
        self.options_mm = ttk.OptionMenu(frame1, self.mm, 'select month', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
        self.options_mm.pack(side='left', fill=X, padx=20)

        self.yy = StringVar(frame1)
        self.yy.set('select year')
        self.options_yy = ttk.OptionMenu(frame1, self.yy, 'select year', 2019, 2018, 2017, 2016, 2017, 2016, 2015,
                                          2014, 2013, 2012, 2011, 2010)
        self.options_yy.pack(side='left', fill=X, padx=20)

        ttk.Label(self).pack()
        frame2 = Frame(self)
        frame2.pack()

        label2 = Label(frame2, text='End Date', font=NORMAL_FONT)
        label2.pack()

        self.ddE = StringVar(frame2)
        self.ddE.set('select day')
        self.options_ddE = ttk.OptionMenu(frame2, self.ddE, 'select day', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                      16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
        self.options_ddE.pack(side='left', fill=X, padx=20)

        self.mmE = StringVar(frame2)
        self.mmE.set('select month')
        self.options_mmE = ttk.OptionMenu(frame2, self.mmE, 'select month', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
        self.options_mmE.pack(side='left', fill=X, padx=20)

        self.yyE = StringVar(frame2)
        self.yyE.set('select year')
        self.options_yyE = ttk.OptionMenu(frame2, self.yyE, 'select year', 2019, 2018, 2017, 2016, 2017, 2016, 2015,
                                         2014, 2013, 2012, 2011, 2010)
        self.options_yyE.pack(side='left', fill=X, padx=20)

        frame3 = Frame(self)
        frame3.pack()

        self.btn_surf = Button(frame3, text="Analyse Chrome", width=20, command=lambda: self.get_history())
        self.btn_surf.pack(side='left', fill=X, padx=10, pady=20)

        self.btn_quit = Button(frame3, text="Quit", width=20, command=lambda: quitting())
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

        day = self.dd.get()
        month = self.mm.get()
        m_val = Month().month_value(month)
        year = self.yy.get()
        if self.verified_inputs(day, month, year):
            start_date = f'{year}-{m_val}-{day}'
            form_start_date = f'{day}-{m_val}-{year}'

        dayE = self.ddE.get()
        monthE = self.mmE.get()
        m_valE = Month().month_value(monthE)
        yearE = self.yyE.get()
        if self.verified_inputs(dayE, monthE, yearE):
            end_date = f'{yearE}-{m_valE}-{dayE}'
            form_end_date = f'{dayE}-{m_valE}-{yearE}'

        isvalid_range = self.validate_range(start_date, end_date)

        if isvalid_range:
            date_range = []
            start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            step = datetime.timedelta(days=1)

            while start >= end:
                r_date = start.date()
                date_range.append(r_date)
                start -= step

            url_dict = {}
            try:
                conn = sqlite3.connect(database)
                cursor = conn.cursor()
                query_wdatetime = 'SELECT u.url, v.visit_time FROM urls u JOIN visits v ON u.id = v.url;'
                cursor.execute(query_wdatetime)

                rows = cursor.fetchall()
                for row in rows:
                    url, timestamp = row[0], row[1]
                    formatted_timestamp = str(datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestamp)
                                              ).split('.')[0]

                    extracted_date, extracted_time = formatted_timestamp.split(' ')[0], formatted_timestamp.split(' ')[1]

                    for query_date in date_range:
                        query_date = str(query_date)
                        if query_date == extracted_date:
                            url_dict.update({url: query_date})

                data_set = sorted(url_dict.items(), key=operator.itemgetter(1))

                self.lbl_disp['fg'] = 'blue'
                self.lbl_disp['text'] = f'from {form_end_date} to {form_start_date} || Query Records: {len(data_set)} ||' \
                    f'Total Records: {len(rows)}'

                if len(data_set) > 0:
                    for data in data_set:
                        self.lbox.insert(END, f'Date: {data[1]}     {data[0]}')
                else:
                    showwarning('Empty', f'There is no record between {form_end_date} and {form_start_date}')

            except Exception as e:
                if str(e) == 'database is locked':
                    showerror('ERROR', f'{e}. \nClose all opened Chrome')
                else:
                    showerror('ERROR', e)
        else:
            showerror('Invalid Range', '''\nStart date should be recent. End date should be previous.''')

    def verified_inputs(self, dd, mm, yy):
        if dd == 'select day' or mm == 'select month' or yy == 'select year':
            showerror('Error Fields', 'Choose fields')
            return False
        else:
            return True

    def validate_range(self, s_date, e_date):
        s_split = s_date.split('-')
        syy, smm, sdd = int(s_split[0]), int(s_split[1][1]), int(s_split[2])

        e_split = e_date.split('-')
        eyy, emm, edd = int(e_split[0]), int(e_split[1][1]), int(e_split[2])

        delta = datetime.date(syy, smm, sdd) - datetime.date(eyy, emm, edd)
        print(delta)
        try:
            val = int(delta.days)
            if val > 0:
                return True
        except:

            return False