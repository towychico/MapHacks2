import os
import pandas as pd
import pandastable
from _multiprocessing import send
from pandas.io.formats.printing import justify
from twilio.rest import Client
import tkinter as tk
from tkinter import ttk
import sv_ttk
from datetime import datetime, timedelta,date
import csv
from PIL import ImageTk, Image
import threading

TWILIO_ACCOUNT =os.environ.get('TWILIO_ACCOUNT')
TWILIO_AUTH_TOKEN =os.environ.get('TWILIO_AUTH_TOKEN')
NUMBER_1 = os.environ.get('NUMBER_1')
NUMBER_2 = os.environ.get('NUMBER_2')


def fill_csv(start_date_arg,days_arg,hours_arg,name_arg,dose_arg,unit_arg,time_arg):
    time_vals =time_arg.split('/')
    time_vals = [int(x) for x in time_vals]
    start_string = start_date_arg
    days_n = days_arg
    hours_of_repetition = hours_arg
    med_name = name_arg
    dose_raw = dose_arg
    units = unit_arg
    dose = ''.join([dose_raw, units])
    print(dose)
    temp = start_string.split('/')
    temp.reverse()
    temp = [int(x) for x in temp]
    start = datetime(temp[0], temp[1], temp[2], time_vals[0], time_vals[1], time_vals[2])
    repetions_per_day = 24 / hours_of_repetition
    total_ocurrences = repetions_per_day * days_n
    temp = start
    days_list = []
    times_list = []
    days_list.append(str(temp.date()))
    times_list.append(str(temp.time()))
    print(temp)
    for i in range(0, int(total_ocurrences)):
        temp += timedelta(hours=hours_of_repetition)
        new_date = temp
        print(new_date.date())
        days_list.append(str(new_date.date()))
        times_list.append(str(new_date.time()))
    end = date(2023, 5, 4)
    new_date = new_date.date()
    meds_list = [med_name for med in range(0, len(days_list))]
    dose_list = [dose for x in range(0, len(days_list))]
    with open('data.csv', 'a', encoding='UTF8', newline='') as f:

        writer = csv.writer(f)
        for i in range(0, len(days_list)):
            row = [meds_list[i], days_list[i], times_list[i], dose_list[i]]
            writer.writerow(row)
        f.close()




def Make_call(number, dose_arg, med_name_arg):
    dose = dose_arg
    med_name = med_name_arg


    account_sid = TWILIO_ACCOUNT
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        twiml=f"<Response><Say>Hello,I am calling you to remind you to take your medications as prescribed by your doctor. It's important that you take your medication on time every day to maintain its effectiveness and to help you stay healthy. Please remember to take {20} of {med_name} right now, I repeat take  {20} of {med_name} right now .Don't hesitate to ask for help if you need it. It's important to take care of yourself, and taking your medication on time is a crucial part of that..</Say></Response>",
        to=number,
        from_=NUMBER_1
    )
    print("Call sended")


def check_database():

    while True:
        data = pd.read_csv('data.csv')
        for i in range(0,len(data)):
            raw_time = data.loc[i,'Time']
            raw_date = data.loc[i,"Date"]
            time_list = raw_time.split(':')
            date_list = raw_date.split('-')
            time_list = [int(i) for i in time_list]
            date_list = [int(i) for i in date_list]
            now = datetime.now().replace(microsecond=0)

            if now.time().minute == time_list[1] and now.time().hour == time_list[0]:
                Make_call(NUMBER_2,data.loc[i,"Dose"],data.loc[i,"Name"])




def get_data():
    global current_unit, pt
    start_date_raw = start_date_input.get()
    med_name_raw = med_name_input.get()
    hours_input_raw = int(hours_input.get())

    days_numbers_raw = int(days_input.get())
    quantity = quantity_input.get()
    time_input_raw = time_input.get()
    fill_csv(start_date_raw, days_numbers_raw, hours_input_raw, med_name_raw, quantity, current_unit,
             time_input_raw)
    pt.importCSV('data.csv')
    pt.redraw()


def radio_used():
    global current_unit
    if int(radio_state.get()) == 1:
        current_unit = 'Mg'
    elif int(radio_state.get()) == 2:
        current_unit = 'g'
    elif int(radio_state.get()) == 3:
        current_unit = 'Ml'
    print(current_unit)


def draw_ui():
    global current_unit, radio_state, med_name_input, quantity_input, time_input, start_date_input, days_input, hours_input, pt
    window = tk.Tk()
    current_unit = ''
    #
    sv_ttk.set_theme("dark")
    logo_frame = ttk.Frame(window, width=200, height=200)
    # logo_frame.config(bg='blue')
    logo_frame.grid(row=1, column=1)
    img = ImageTk.PhotoImage(Image.open("logo.png"))
    image_container = tk.Label(logo_frame, image=img)
    image_container.pack()
    units_frame = ttk.Frame(window, width=200, height=300)
    # units_frame.config(bg='red')
    units_frame.grid(row=2, column=1)
    # Variable to hold on to which radio button value is checked.
    radio_state = tk.IntVar()
    mg_button = ttk.Radiobutton(units_frame, text="Mg", value=1, variable=radio_state, command=radio_used, padding=15)
    g_button = ttk.Radiobutton(units_frame, text=" g", value=2, variable=radio_state, command=radio_used, padding=15)
    ml_button = ttk.Radiobutton(units_frame, text=" Ml", value=3, variable=radio_state, command=radio_used, padding=15)
    mg_button.grid(row=1, column=1)
    g_button.grid(row=2, column=1)
    ml_button.grid(row=3, column=1)
    send_button = ttk.Button(units_frame, text="Send", command=get_data)
    send_button.grid(row=4, column=1)
    intput_frame = ttk.Frame(window, width=450, height=200)
    intput_frame.grid(row=1, column=2)
    med_name_label = ttk.Label(intput_frame, text="Medicine Name")
    med_name_label.grid(row=1, column=0, columnspan=2)
    med_name_input = ttk.Entry(intput_frame, width=15)
    med_name_input.grid(row=2, column=0, columnspan=2, padx=5)
    quantity_label = ttk.Label(intput_frame, text="Quantity")
    quantity_label.grid(row=1, column=2, columnspan=1, pady=20, padx=20)
    quantity_input = ttk.Entry(intput_frame, width=10)
    quantity_input.grid(row=2, column=2, columnspan=1, padx=50)
    time_label = ttk.Label(intput_frame, text="Time\n(hh/mm/ss)")
    time_label.grid(row=1, column=3, columnspan=1, pady=20, padx=20)
    time_input = ttk.Entry(intput_frame, width=10)
    time_input.grid(row=2, column=3, columnspan=1, padx=50)
    start_date_label = ttk.Label(intput_frame, text="Start Date\n(dd/mm/yyyy)")
    start_date_label.grid(row=3, column=1, columnspan=1, pady=20, padx=20)
    days_label = ttk.Label(intput_frame, text="days")
    days_label.grid(row=3, column=2, columnspan=1, pady=20, padx=20)
    hours_label = ttk.Label(intput_frame, text="Hours")
    hours_label.grid(row=3, column=3, columnspan=1, pady=20, padx=20)
    start_date_input = ttk.Entry(intput_frame)
    start_date_input.grid(row=4, column=1, columnspan=1, padx=5)
    days_input = ttk.Entry(intput_frame)
    days_input.grid(row=4, column=2, columnspan=1, padx=5)
    hours_input = ttk.Entry(intput_frame)
    hours_input.grid(row=4, column=3, columnspan=1, padx=5)
    data_frame = ttk.Frame(window, width=450, height=300)
    # data_frame.config(bg='pink')
    data_frame.grid(row=2, column=2)
    pt = pandastable.Table(data_frame)
    pt.importCSV('data.csv')
    pt.show()
    window.minsize(width=650, height=500)
    window.mainloop()




t1 = threading.Thread(target=draw_ui)
t2 = threading.Thread(target=check_database)
t1.start()
t2.start()