# import everything from tkinter module
from tkinter import *
import RPi.GPIO as GPIO
import time
from time import sleep
import requests

import yagmail

yag = yagmail.SMTP("sharmaagastya40@gmail.com", "sjsdfnspklfgkmec")

in1 = 24
in2 = 23
in3 = 14
in4 = 15
ena = 25
enb = 18
temp1=1
# create a tkinter window
root = Tk()
# for IR ssor
buzzer = 18
sensor = 16
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)
# for motors
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p=GPIO.PWM(ena,1000)
q=GPIO.PWM(enb,1000)
p.start(25)
q.start(25)



# declaring string variable
# for storing name and password
text_var = StringVar()  #for storing Time
text_var2 = StringVar() #for storing User's email address
text_var3 = StringVar() # emergency patient
hour_var = IntVar()
min_var = IntVar()
# Open window having dimension 100x100
root.geometry("300x300")

try:
    # defining a function that will
    # get the name and password and
    # print them on the screen
    def submit():
        global text_var
        global some
        global root
        
        text = text_var.get()
        hour, min = [int(i) for i in text.split(":")]
        #saving global values
        hour_var.set(hour)
        min_var.set(min)


        text_var.set("") #resetting the value
        root.update()
        root.update_idletasks()
       

    sub_btn = Button(root, text="Send", command=submit)

    # creating a label for
    # text using widget Label
    text_label = Label(root, text="Enter time in HH:MM\n", font=("calibre", 10, "bold"))

    # creating a entry for input
    # text using widget Entry
    text_entry = Entry(root, textvariable=text_var,
                       font=("calibre", 10, "normal"))

    
    text_label2 = Label(root, text="Enter your email address", font=("calibre", 10, "bold"))   
    text_entry2 = Entry(root, textvariable=text_var2,
                       font=("calibre", 10, "normal"))

    text_label3 = Label(root, text="Enter your email address", font=("calibre", 10, "bold"))   
    text_entry3 = Entry(root, textvariable=text_var3,
                       font=("calibre", 10, "normal"))

    text_label.grid(row=1, column=0)
    text_entry.grid(row=1, column=1)
    
    text_label2.grid(row=2, column=0)
    text_entry2.grid(row=2, column=1)

    text_label2.grid(row=3, column=0)
    text_entry2.grid(row=3, column=1)

    sub_btn.grid(row=4, column=1)
    val = False
    timer = 0
    #if pill is detected
    if GPIO.input(sensor):
        GPIO.output(buzzer,True)
        sleep(5)
        GPIO.output(buzzer,False)
        val = True
    #medicine is dropped, and waiting
    if val: 
        timer+=1
        if timer>1000:  #if pill is not picked
            requests.post('https://maker.ifttt.com/trigger/Medicine_not_taken/json/with/key/jhPlpb6TxLwNt2rqezn5b-Qdsj3aQmy28gRzLRrHvLy')
            yag.send(text_var2.get(), "Medicine not taken", "You have not taken medicine yet")  
            #contact person
            yag.send(text_var3.get(), "Medicine not taken", "Your's patient have not taken medicine yet")  


    #if time matches the user inputed time, medicine gets dispensed
    if time.strftime("%H") == hour_var.get() and time.strftime("%M") <= min_var.get():
        p.ChangeDutyCycle(75) #speed of the motors
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        sleep(3)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        requests.post('https://maker.ifttt.com/trigger/Medicine_dispensed/json/with/key/jhPlpb6TxLwNt2rqezn5b-Qdsj3aQmy28gRzLRrHvLy')
        yag.send(text_var2.get(), "Medicine is Dispensed", "Your patient's medicine has been dispensed") 
    # for the window to display
    # performing an infinite loop
    root.mainloop()
    GPIO.cleanup()
except Exception:
    print(Exception)