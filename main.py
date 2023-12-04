from tkinter import messagebox
from threading import Thread
import customtkinter as ctk
import tkinter as tk
import time
from PIL import ImageTk, Image
import mouse
import pystray
from pystray import MenuItem as item
from datetime import datetime
import json
import os
from pydub import AudioSegment
# import required module
import playsound
from playsound import playsound

beep_count = int(1)
alarms = []
alarms_active = []
alarms_widgets = []
box_widgets = []
initialized = False



def AlarmApp():
    current_time = datetime.now()
    current_time = current_time.strftime("%I:%M %p")



    root = tk.Tk()
    root.title("Alarm")
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    # Store the initial mouse coordinates when the left button is pressed
    # alarms = [{"hour", "minute", "am/pm", "Every Day/Never", "Alarm Name", "ID", "0/1"}]
    #              2       32      am=0 pm=1    0/1                 name     1,2,3,4   0/1


    background_color = '#%02x%02x%02x' % (18, 18, 18)
    green_color = '#%02x%02x%02x' % (47,208,88)
    beep_count=0
    root.geometry("400x600")
    root.resizable(False,False)
    root.geometry("+{}+{}".format(576,110)) #spawn in middle

    start_x = 0
    start_y = 0

    def get_audio_duration(file_path):
        audio = AudioSegment.from_file(file_path)
        duration_in_seconds = len(audio) / 1000.0  # Convert milliseconds to seconds
        return duration_in_seconds


    def alarm_ring():
        global beep_count
        while True:
            current_time = datetime.now()
            current_time = current_time.strftime("%I:%M %p")
            prev_time = current_time
            print(current_time)
            for index, alarm_status in enumerate(alarms_active):
                if (alarm_status == "On" and int(current_time[:2])==int(alarms[index][0]) and int(current_time[3:5])==int(alarms[index][1])and((int(alarms[index][2]) == 1 and current_time[6:]=="AM" )or (int(alarms[index][2]) == 2 and current_time[6:]=="PM" ))):
                    sound_file_path = os.path.join(os.getcwd(), 'ring.wav')
                    duration = get_audio_duration(sound_file_path)
                    print("duration:",duration)
                    playsound(sound_file_path)
                    time.sleep(60-duration)
            time.sleep(0.5)



    def on_button_press(event):
        global start_x, start_y
        # Record the initial mouse coordinates
        # add_alarm() #_------remove
        start_x = event.x_root - root.winfo_x()
        start_y = event.y_root - root.winfo_y()
    def on_mouse_drag(event):
        global start_x, start_y
        # Calculate the new window coordinates based on the mouse motion
        x = event.x_root - start_x
        y = event.y_root - start_y
        print(x,y)
        # Move the window to the new coordinates
        root.geometry("+{}+{}".format(x, y))

        # Bind the mouse events



    root.bind("<ButtonPress-1>", on_button_press)
    root.bind("<B1-Motion>", on_mouse_drag)



    def create_alarm(hour, minute, period, repetition, alarm_name, new_id):
        box_frame = ctk.CTkFrame(frame, width=360, height=116, corner_radius=0, fg_color="black")
        box_frame.pack_propagate(False)  # keep it from changing size cuz of text

        line_label = tk.Label(box_frame, height=1, width=360, text="━━━━━━━━━━━━━━━━━━"
                                                                   "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                              bg="black",
                              relief="solid", fg="gray")
        line_label.pack(side="bottom")

        box_frame.pack(anchor="center", pady=5)  # Adjust the padx and pady values as needed

        if (period == 1):
            period = "AM"
        if (period == 2):
            period = "PM"

        if (minute < 10):
            minute = "0" + str(minute)

        time_text = f"{hour}:{minute}"

        label_time = ctk.CTkLabel(box_frame, text_color='#444348', text=f"{time_text}", font=("Helvetica", 40))
        label_time.pack(side="left", anchor="w")

        label_period = ctk.CTkLabel(box_frame, text_color='#444348', text=f"{period}", font=("Helvetica", 20))
        label_period.pack(side="left", anchor="w", pady=(14, 0))

        label_name = ctk.CTkLabel(box_frame, text_color='#444348', text=f"{alarm_name}", font=("Helvetica", 15))
        label_name.place(relx=0.025, rely=0.6)

        delete_button = ctk.CTkButton(box_frame, text="─", width=0, height=0, fg_color="black",
                                      text_color="Red", font=("Helvetica", 30),
                                      hover_color=background_color)
        delete_button.configure(command=lambda: delete_alarm(new_id))

        alarms_widgets.append([label_time, label_period, label_name, delete_button])
        box_widgets.append(box_frame)

        def alarm_enable_manage(switch_id, switch_state):
            print("SwitchId:", switch_id)
            print(alarms)
            print(alarms_active)


            switch_status = (f"{'On' if switch_state.get() == 1 else 'Off'}")
            counter_id = 0
            for i in alarms:
                if (i[5] == switch_id):
                    break
                counter_id += 1
            print("Counter:",counter_id)

            alarms_active[counter_id] = switch_status
            # wali 3
            print(alarms_active)

        switch_state_var = tk.IntVar()
        print(switch_state_var)

        alarm_enable_switch = ctk.CTkSwitch(master=box_frame, text="",
                                            command=lambda: alarm_enable_manage(new_id, switch_state_var),
                                            variable=switch_state_var, onvalue=1, offvalue=0,
                                            fg_color="#444348", progress_color=green_color, button_color="white",
                                            button_hover_color="#D0d1d3", bg_color="black", switch_width=90,
                                            switch_height=40,
                                            font=("Arial", 30), text_color="#d4dcdd")
        alarm_enable_switch.pack(side="right", anchor="center")
        global initialized

        if (initialized==False):
            try:
                counter_id = 0
                for i in alarms:
                    if (i[5] == new_id):
                        break
                    counter_id += 1
                if (alarms_active[counter_id] == "On"):
                    alarm_enable_switch.toggle()
            except IndexError:
                print("Alarm Empty")

    def cancel(new_window_alarm):
        new_window_alarm.destroy()
        root.attributes("-topmost", True)




    def add_alarm():
        window_loaded = False

        new_window_alarm = tk.Toplevel(root)
        root.attributes("-topmost", False)
        new_window_alarm.attributes("-topmost", True)

        mouse.click('left')


        start_x = 0
        start_y = 0

        def on_button_press(event):
            global start_x, start_y
            # Record the initial mouse coordinates

            if(window_loaded==True):
                start_x = event.x_root - root.winfo_x()
                start_y = event.y_root - root.winfo_y()

                start_x = event.x_root - new_window_alarm.winfo_x()
                start_y = event.y_root - new_window_alarm.winfo_y()

        def on_mouse_drag(event):
            global start_x, start_y
            # Calculate the new window coordinates based on the mouse motion
            if(window_loaded==True):
                x = event.x_root - start_x
                y = event.y_root - start_y

                # Move the window to the new coordinates
                root.geometry("+{}+{}".format(x, y))
                # Bind the mouse events
                new_window_alarm.geometry("+{}+{}".format(x, y))

        #wali2





        def save_alarm():

            check = True
            hour = int(entry_hour.get())
            minute = int(entry_minute.get())
            period = int(radio_var.get())
            alarm_name = entry_name.get()
            repetition = 1 # 1 for never, 0 for every day

            try:
                if(hour<1 or hour>12 or minute<0 or minute>60 or period==0):
                    mouse.click('left')

                    tk.messagebox.showerror("Invalid Input","Please provide Time in Valid Format\n"
                                                            "Hours 1-12 Minutes 0-60\nMake Sure to Also Select Am/Pm",parent=new_window_alarm)
                    check = False
            except ValueError:
                mouse.click('left')

                tk.messagebox.showerror("Empty Field","Make Sure to Fill Out All the Fields",
                                        parent=new_window_alarm)
                check = False
            try:
                new_id = int(alarms[-1][5])+1
            except IndexError:
                new_id = 0


            if(everyDay_switch.get()=="on"):
                repetition=0


            if(alarm_name==''):
                alarm_name=f"Alarm {new_id}"
            if(check==True):
                alarms_new = [hour,minute,period,repetition,alarm_name,new_id]
                alarms.append(alarms_new)
                create_alarm(hour, minute, period, repetition, alarm_name, new_id)
                alarms_active.append("off")
                root.attributes("-topmost", True)
                new_window_alarm.destroy()


            # alarms = [{"hour", "minute", "am/pm", "Every Day/Never", "Alarm Name", "ID"}]
            #              2       32      am=0 pm=1    0/1                 name     1,2,3,4



            print(alarms)


        new_window_alarm.bind("<ButtonPress-1>", on_button_press)
        new_window_alarm.bind("<B1-Motion>", on_mouse_drag)



        new_window_alarm.geometry("400x600")
        new_window_alarm.resizable(False, False)
        new_window_alarm.overrideredirect(True)
        new_window_alarm.geometry(f"+{root.winfo_x()}+{root.winfo_y()}")
        background_button = ctk.CTkButton(new_window_alarm, text="", image=background, bg_color=background_color, width=0, height=0,hover_color="#131313")
        background_button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        new_window_alarm.time_label = tk.Label(new_window_alarm, text="Add Alarm", font=("Arial", 16), fg="#d4dcdd", bg=background_color)
        new_window_alarm.time_label.place(relx=0.5, rely=0.05, anchor=ctk.CENTER)

        cancel_button = ctk.CTkButton(new_window_alarm, text="Cancel", fg_color='#131313', font=("Arial", 20), width=40, height=30,
                                    corner_radius=0, text_color="#FFA00E", hover_color='#131313')
        cancel_button.configure(command=lambda:cancel(new_window_alarm))
        cancel_button.place(relx=0.1, rely=0.05, anchor=ctk.CENTER)

        save_button = ctk.CTkButton(new_window_alarm, text="Save", fg_color='#131313', font=("Arial", 20), width=40, height=30,
                                    corner_radius=0, text_color="#FFA00E", hover_color='#131313')
        save_button.configure(command=save_alarm)
        save_button.place(relx=0.9, rely=0.05, anchor=ctk.CENTER)

        entry_hour = ctk.CTkEntry(master=new_window_alarm,
                                       placeholder_text="1-12  ",
                                       width=80,
                                       height=60,
                                       border_width=0,corner_radius=0,
                                       font=("Arial", 30),justify="center", text_color="#d4dcdd",fg_color="black")
        entry_hour.place(relx=0.25, rely=0.305, anchor=tk.CENTER)

        new_window_alarm.time_label = tk.Label(new_window_alarm, text=":", font=("Arial", 30), fg="#d4dcdd",
                                               bg="black")
        new_window_alarm.time_label.place(relx=0.4, rely=0.3, anchor=ctk.CENTER)

        entry_minute = ctk.CTkEntry(master=new_window_alarm,
                                  placeholder_text="0-60  ",
                                  width=80,
                                  height=60,
                                  border_width=0, corner_radius=0,
                                  font=("Arial", 30), justify="center", text_color="#d4dcdd", fg_color="black")
        entry_minute.place(relx=0.55, rely=0.305, anchor=tk.CENTER)

        entry_name = ctk.CTkEntry(master=new_window_alarm,
                                  placeholder_text="Alarm Name",
                                  width=300,
                                  height=60,
                                  border_width=0, corner_radius=0,
                                  font=("Arial", 30), justify="center", text_color="#d4dcdd", fg_color="black")
        entry_name.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        switch_var_everyDay = ctk.StringVar(value="on")
        switch_var_never = ctk.StringVar(value="off")


        def switch_event_everyDay():
            print("switch toggled, current value:", switch_var_everyDay.get())
            if (switch_var_never.get() == "on" and switch_var_everyDay.get() == "on"):
                never_switch.toggle()
            if (switch_var_everyDay.get() == "off" and switch_var_never.get() == "off"):
                never_switch.toggle()

        def switch_event_never():
            print("switch toggled, current value:", switch_var_never.get())
            if(switch_var_everyDay.get()=="on" and switch_var_never.get() == "on"):
                everyDay_switch.toggle()

            if (switch_var_everyDay.get() == "off" and switch_var_never.get() == "off"):
                everyDay_switch.toggle()




        everyDay_switch = ctk.CTkSwitch(master=new_window_alarm, text="Every Day", command=switch_event_everyDay,
                                           variable=switch_var_everyDay, onvalue="on", offvalue="off",fg_color="#444348",progress_color=green_color, button_color="white",
                                 button_hover_color="#D0d1d3", bg_color="black",switch_width=90,switch_height=40,
                                  font=("Arial", 30),text_color="#d4dcdd")
        everyDay_switch.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)

        never_switch = ctk.CTkSwitch(master=new_window_alarm, text="Never", command=switch_event_never,
                                        variable=switch_var_never, onvalue="on", offvalue="off", fg_color="#444348",
                                        progress_color=green_color, button_color="white",
                                        button_hover_color="#D0d1d3", bg_color="black", switch_width=90,
                                        switch_height=40,
                                        font=("Arial", 30), text_color="#d4dcdd")

        never_switch.place(relx=0.43, rely=0.65, anchor=ctk.CENTER)







        radio_var = ctk.IntVar()

        def radiobutton_event():
            print("radiobutton toggled, current value:", radio_var.get())

        radiobutton_1 = ctk.CTkRadioButton(master=new_window_alarm, text="AM",
                                                     command=radiobutton_event, variable=radio_var, value=1)
        radiobutton_2 = ctk.CTkRadioButton(master=new_window_alarm, text="PM",
                                                     command=radiobutton_event, variable=radio_var, value=2)

        radiobutton_1.configure( bg_color="black",text_color="#d4dcdd",fg_color="#656F77")
        radiobutton_2.configure( bg_color="black",text_color="#d4dcdd",fg_color="#656F77")

        radiobutton_1.place(relx=0.85, rely=0.29, anchor=tk.CENTER)
        radiobutton_2.place(relx=0.85, rely=0.33, anchor=tk.CENTER)



        window_loaded = True




        new_window_alarm.mainloop()

    # Define a function for quit the window
    def quit_window(icon, item):
        icon.stop()
        root.destroy()

    # Define a function to show the window again
    def show_window(icon, item):
        icon.stop()
        root.after(0, root.deiconify())

    # Hide the window and show on the system taskbar



    def hide_window():
        global alarms_widgets
        global alarms
        global alarms_active
        print(alarms)
        # Save the alarms data to a JSON file
        # Writing data to 'alarms_data.json'
        alarms_file_path = os.path.join(os.getcwd(), 'alarms_data.json')
        with open(alarms_file_path, 'w') as file:
            json.dump({'alarms': alarms}, file)

        # Writing data to 'alarms_status_data.json'
        alarms_active_file_path = os.path.join(os.getcwd(), 'alarms_status_data.json')
        with open(alarms_active_file_path, 'w') as file:
            json.dump({'alarms_active': alarms_active}, file)




        root.withdraw()
        image = Image.open("alarmicon.ico")
        menu = (item('Quit', quit_window), item('Show', show_window))
        icon = pystray.Icon("name", image, "My System Tray Icon", menu)
        icon.run()


    def delete_alarm(alarm_id):
        print("del")
        counter_id = 0
        for i in alarms:
            if(i[5]==alarm_id):
                break
            counter_id += 1
        print(counter_id)

        box_widgets[counter_id].destroy()
        del alarms_widgets[counter_id]
        del box_widgets[counter_id]
        del alarms[counter_id]
        del alarms_active[counter_id]

        # for child in frame.winfo_children():
        #     child.destroy()



    def edit_alarms():
        #wali1
        def done_edit():
            done_button.destroy()
            edit_button.place(relx=0.1, rely=0.05, anchor=ctk.CENTER)

            for i in alarms_widgets:
                print(f"HERE: {i}")
                i[0].forget()  # Hide the widget
                i[1].forget()
                i[2].forget()

                i[0].configure(padx=0)  # Reset padx for label_time
                i[0].pack(side="left",anchor="w")  # Re-pack the widget
                i[1].pack(side="left", anchor="w", pady=(14, 0))
                i[2].place(relx=0.025,rely=0.6)
                i[3].place(relx=1.5)



        # alarms_widgets.append([label_time,label_period,label_name,delete_button])
        edit_button.pack_forget()
        done_button = ctk.CTkButton(root, text="Done", fg_color='#131313', font=("Arial", 20), width=40, height=30,
                                    corner_radius=0, text_color="#FFA00E",
                                    hover_color='#131313', command=done_edit)
        done_button.place(relx=0.1, rely=0.05, anchor=ctk.CENTER)

        for i in alarms_widgets:
            i[0].forget()  # Hide the widget
            i[1].forget()
            i[2].forget()

            i[0].configure(padx=100)  # Configure padx for label_time
            i[0].pack(side="right",anchor="center")  # Re-pack the widget
            i[1].place(relx=0.48,rely=0.35)
            i[2].place(relx=0.28,rely=0.55)
            i[3].place(relx=0.1, rely=0.3)







    plus_icon = Image.open("plus.png")
    plus_icon = plus_icon.resize((32,32))
    plus_icon = ImageTk.PhotoImage(plus_icon)

    background = Image.open("background.png")
    background = background.resize((400,600))
    background = ImageTk.PhotoImage(background)

    background_button = ctk.CTkButton(root, text="", image=background, bg_color=background_color,width=0,height=0,hover_color="#131313")
    background_button.place(relx=0.5,rely=0.5, anchor=ctk.CENTER)

    frame = ctk.CTkScrollableFrame(master=root, width=400, height=530, corner_radius=0, fg_color="Black")
    frame.place(relx=0.5, rely=0.56, anchor=tk.CENTER)



    exit = ctk.CTkButton(root, text="Exit", width=40, height=30,font=("Arial", 20),fg_color=background_color,
                               hover_color="Gray",corner_radius=0 )
    exit.configure(command=hide_window)
    exit.place(relx=0.5,rely=0.05, anchor=ctk.CENTER)


    add_button = ctk.CTkButton(root, text="", image=plus_icon, width=0,height=0,fg_color=background_color, hover_color=background_color)
    add_button.configure(command= add_alarm)

    add_button.place(relx=0.9, rely=0.05, anchor=ctk.CENTER)

    edit_button = ctk.CTkButton(root, text="Edit", fg_color='#131313',font=("Arial", 20), width=40,height=30,corner_radius=0,text_color="#FFA00E",
                                hover_color='#131313', command=edit_alarms)
    edit_button.place(relx=0.1, rely=0.05, anchor=ctk.CENTER)

    root.protocol('WM_DELETE_WINDOW', hide_window)

    def initialize_alarms():
        for i in alarms:
            create_alarm(i[0], i[1], i[2], i[3], i[4], i[5])
        time.sleep(3)

    # fix this!!!!!
    # Perform the initialization only if it hasn't been done yet
    initialize_alarms()

    initialized=True
    alarm_ring_thread = Thread(target=alarm_ring, daemon=True)
    alarm_ring_thread.start()
    root.mainloop()

if __name__ == "__main__":
    # Load the alarms data from the JSON file


    try:
        # Get the absolute path of the 'alarms_data.json' file
        file_path = os.path.join(os.getcwd(), 'alarms_data.json')

        with open(file_path, 'r') as file:
            data = json.load(file)
            alarms = data.get('alarms', [])
    except (json.JSONDecodeError, FileNotFoundError):
        # Handle the case where the file is empty or not found
        print("Exception Json Decode error")

    try:
        # Get the absolute path of the 'alarms_status_data.json' file
        file_path = os.path.join(os.getcwd(), 'alarms_status_data.json')

        with open(file_path, 'r') as file:
            data = json.load(file)
            alarms_active = data.get('alarms_active', [])
    except (json.JSONDecodeError, FileNotFoundError):
        # Handle the case where the file is empty or not found
        print("Exception Json Decode error")
        alarms_active = []

    print("Active after data:", alarms_active)


    for i in alarms:
        print(i)

    AlarmApp()
