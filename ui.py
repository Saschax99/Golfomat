import customtkinter
from tkinter import Label, Frame, CENTER, LEFT, RIGHT, DISABLED, NORMAL
from PIL import Image, ImageTk
from config import *
import sys
from loggingsystem import writeLog, logging
import time
import datetime
from threading import Timer
import threading
from rfid import rfid
from tkinter import Tk
import RPi.GPIO as GPIO

already_active = False # max. one login
ctr_strikes = 0

# MOTOR SET DEFAULT
# if not "win" in sys.platform: 
#     GPIO.setmode(GPIO.BCM) # GPIO Pins
#     # GPIO.setwarnings(False)
#     GPIO.setup(RELAIS_1, GPIO.OUT) # set output
#     GPIO.setup(RELAIS_2, GPIO.OUT)
#     GPIO.setup(RELAIS_3, GPIO.OUT)
    
#     GPIO.output(RELAIS_1, GPIO.LOW) # set relais off
#     GPIO.output(RELAIS_2, GPIO.LOW)
#     GPIO.output(RELAIS_3, GPIO.LOW)
# /MOTOR

class login():
    '''loginsystem for chip/nfc timer'''
    def run(self, label): # start thread
        self.thread = Timer(1, self.run, args=[label]) # 1 sec
        self.thread.start()
        
        self.print_current_datetime(label) # change label
        
    def start(self, label): # initialize
        global already_active
        if not already_active:
            label.configure(text="0:00:00")
            self.start_t = time.time()
            self.thread = Timer(1, self.run, args=[label])
            self.thread.start()
            already_active = True
        
    def cancel(self, label): # logout/cancel thread
        global already_active
        self.thread.cancel()
        already_active = False
        label.configure(text="")
        label.configure(text="0:00:00")
        
    def print_current_datetime(self, label):
        self.end_t = time.time()
        calc_time = int(self.end_t - self.start_t)
        tim = str(datetime.timedelta(seconds=calc_time))
        label.configure(text=tim)
        time.sleep(1)

    
logging()
    
# display init
root = Tk()
height = WINDOW_HEIGHT
width = WINDOW_WIDTH
root.title("Golfomat")
root.geometry("800x480") #Define the size of the tkinter frame
if not "win" in sys.platform: # if execute on rpi get fullscreen
    root.attributes("-fullscreen", True)
else:
    root.attributes("-fullscreen", False)
# /display init

bg = Label(root, bg = BACKGROUND, width = 800, height = 480) # background color
bg.place(x=0, y=0)
root.resizable(False, False)


timer = login()

# UI
top_frame = Frame(root, 
                height=40, 
                width=800, 
                bg=BG)
top_frame.place(x=0,y=0)

Frame(root,
        height=3,
        width=800,
        bg=BG).place(x=0, y=40)

# title name
Label(top_frame, 
        text="Golfomat",
        bg=BG, 
        fg="white",
        width=12, 
        font=("Arial", 18)).place(x=5, y=5)

username = Label(top_frame,
                    text="Keinen Namen gefunden",
                    bg=BG, 
                    fg="white",
                    width=20, 
                    font=("Arial", 15))
username.place(x=287, y=7)       


btn_logout = customtkinter.CTkButton(master=top_frame, 
                        text="Ausloggen", 
                        text_color="white", 
                        bg_color=BG,
                        fg_color=FG,
                        hover_color=HOVER,
                        command=lambda: logout())
btn_logout.place(x=722, y=20, anchor=CENTER)

time_label = Label(root,
                    text="",
                    fg="black",
                    bg=BACKGROUND, 
                    width=12, 
                    font=("Arial", 15))
time_label.place(x=331, y=57) 

total_strikes = Label(root,
                    text="Schlaege insgesamt: 0",
                    fg="black",
                    bg=BACKGROUND, 
                    width=22, 
                    font=("Arial", 15))
total_strikes.place(x=75, y=57) 

container = customtkinter.CTkFrame(master=root,
                                            width=600,
                                            height=300,
                                            corner_radius=4,
                                            fg_color="white")
container.place(x=100, y=100)

customtkinter.CTkFrame(master=container, # HORIZONTAL BORDER
                        width=container.winfo_reqwidth(),
                        height=2,
                        corner_radius=10,
                        fg_color=FG).place(x=0, y=40)

customtkinter.CTkFrame(master=container,
                        width=2,
                        height=container.winfo_reqheight(),
                        corner_radius=10,
                        fg_color=FG).place(x=299, y=40)

Label(container,
        text="Position auswaehlen",
        bg="white", 
        width=55, 
        font=("Arial", 15)).place(x=0, y=5) 

btn_down = customtkinter.CTkButton(master=container, 
                        text="Tiefe Position", 
                        text_color="white", 
                        height=200,
                        width=200,
                        border_width=2,
                        border_color=FG,
                        corner_radius=3,
                        text_font=("Arial", 15),
                        fg_color=FG,
                        hover_color=HOVER,
                        command=lambda: smallPosition())
btn_down.place(x=49, y=71)

btn_up = customtkinter.CTkButton(master=container, 
                        text="Hohe Position", 
                        text_color="white", 
                        height=200,
                        width=200,
                        border_width=2,
                        border_color=FG,
                        corner_radius=3,
                        text_font=("Arial", 15),
                        fg_color=FG,
                        hover_color=HOVER,
                        command=lambda: bigPosition())
btn_up.place(x=351, y=71)
                        # command=lambda: print("higher position")).place(x=351, y=71)
                        
def logout():
    global login_check
    global ctr_strikes    
    
    writeLog(username["text"], time_label["text"], str(ctr_strikes))
    
    login_check = False
    timer.cancel(label=time_label)
    
    ctr_strikes = 0
    total_strikes.configure(text="Schlaege insgesamt: 0")
    
    changeUserName("Kein Benutzer")
    btn_up.configure(state=DISABLED)
    btn_down.configure(state=DISABLED)
    

def moveBigPosition():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM) # GPIO Pins
    # # GPIO.setwarnings(False)
    GPIO.setup(RELAIS_1, GPIO.OUT) # set output
    GPIO.setup(RELAIS_2, GPIO.OUT)
    GPIO.setup(RELAIS_3, GPIO.OUT)

    GPIO.output(RELAIS_1, GPIO.HIGH)
    time.sleep(MOTOR_POSITION_HIGH_DELAY)
    GPIO.output(RELAIS_1, GPIO.LOW)
    # # /move up
    
    time.sleep(MOTOR_TIME_DELAY)
    
    # # move down
    GPIO.output(RELAIS_1, GPIO.HIGH)
    GPIO.output(RELAIS_2, GPIO.HIGH)
    GPIO.output(RELAIS_3, GPIO.HIGH)
    time.sleep(MOTOR_POSITION_HIGH_DELAY)
    GPIO.output(RELAIS_1, GPIO.LOW)
    GPIO.output(RELAIS_2, GPIO.LOW)
    GPIO.output(RELAIS_3, GPIO.LOW)

thread_inst_big = threading.Thread(target=moveBigPosition,)

def bigPosition(): # change relais modes with sleeps
    print("hohe Position!")
    global ctr_strikes
    ctr_strikes += 1
    total_strikes.configure(text=f"Schlaege insgesamt: {ctr_strikes}")
    if not "win" in sys.platform:
        # move up
        btn_up.configure(state=DISABLED)
        btn_down.configure(state=DISABLED)

        thread_inst_big.start()

        btn_up.configure(state=NORMAL)
        btn_down.configure(state=NORMAL)
        # /move down
    
def moveSmallPosition():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM) # GPIO Pins
    GPIO.setwarnings(False)
    GPIO.setup(RELAIS_1, GPIO.OUT) # set output
    GPIO.setup(RELAIS_2, GPIO.OUT)
    GPIO.setup(RELAIS_3, GPIO.OUT)

    GPIO.output(RELAIS_1, GPIO.HIGH)
    time.sleep(MOTOR_POSITION_SMALL_DELAY)
    GPIO.output(RELAIS_1, GPIO.LOW)
    # # /move up
    
    time.sleep(MOTOR_TIME_DELAY)
    # # move down
    GPIO.output(RELAIS_1, GPIO.HIGH)
    GPIO.output(RELAIS_2, GPIO.HIGH)
    GPIO.output(RELAIS_3, GPIO.HIGH)
    time.sleep(MOTOR_POSITION_SMALL_DELAY)
    GPIO.output(RELAIS_1, GPIO.LOW)
    GPIO.output(RELAIS_2, GPIO.LOW)
    GPIO.output(RELAIS_3, GPIO.LOW)
    # /move down

thread_inst_small = threading.Thread(target=moveSmallPosition,)

def smallPosition(): # change relais modes with sleeps

    global ctr_strikes
    ctr_strikes += 1
    total_strikes.configure(text=f"Schlaege insgesamt: {ctr_strikes}")
    
    if not "win" in sys.platform:
        # move up
        btn_up.configure(state=DISABLED)
        btn_down.configure(state=DISABLED)

        thread_inst_small.start()
    
        btn_up.configure(state=NORMAL)
        btn_down.configure(state=NORMAL)

    
def changeTimer(calc_time):
    # global time_label
    time_label.configure(str(datetime.timedelta(seconds=calc_time)))
        
def changeUserName(name):
    username.configure(text=name)
    
login_check = False

changeUserName("Kein Benutzer")
btn_up.configure(state=DISABLED)
btn_down.configure(state=DISABLED)
btn_logout.configure(state=DISABLED)
print("disable")

def rfidChangeName():
    global login_check
    print("rfid check")
    while True:
        try:
            print("get name")
            read_name = rfid.read()
            print("newname: " + read_name[1])
            for name in USERNAMES:
                if name in read_name:
                    changeUserName(name)
                    timer.start(label=time_label)
                    btn_up.configure(state=NORMAL)
                    btn_down.configure(state=NORMAL)
                    btn_logout.configure(state=NORMAL)
                    login_check = True
                    print("enable")
                if not login_check:
                    changeUserName("Kein Benutzer")
                    btn_up.configure(state=DISABLED)
                    btn_down.configure(state=DISABLED)
                    btn_logout.configure(state=DISABLED)
                    print("disable")
                print("..")
            time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
    
t = threading.Thread(target=rfidChangeName,)
t.start()    
    
root.mainloop()
