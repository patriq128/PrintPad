import pygame
import time
import requests

url = "http://123.123.123.123/printer/gcode/script"  # Change IP

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()

joystick = pygame.joystick.Joystick(0)
joystick.init()

def send_gcode(script):
    try:
        requests.post(url, json={"script": script}, timeout=0.5)
    except requests.RequestException:
        print("Printer not printing :|")

filament_load = 50
filament_speed =150

AXIS_THRESHOLD = 0.5
last_move_time = 0
MOVE_INTERVAL = 0.2 

current_fanspeed = 0

while True:
    pygame.event.pump()
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)
    z_axis = joystick.get_axis(4)

    current_time = time.time()
    
    if current_time - last_move_time > MOVE_INTERVAL:
        if x_axis < -AXIS_THRESHOLD:
            print("Move left")
            send_gcode("G91\nG1 X-10 F1500")
            last_move_time = current_time
        elif x_axis > AXIS_THRESHOLD:
            print("Move right")
            send_gcode("G91\nG1 X10 F1500")
            last_move_time = current_time

        if y_axis < -AXIS_THRESHOLD:
            print("Move forward")
            send_gcode("G91\nG1 Y-10 F1500")
            last_move_time = current_time
        elif y_axis > AXIS_THRESHOLD:
            print("Move backward")
            send_gcode("G91\nG1 Y10 F1500")
            last_move_time = current_time

        if z_axis < -AXIS_THRESHOLD:
            print("Move up")
            send_gcode("G91\nG1 Z10 F1500")
            last_move_time = current_time
        elif z_axis > AXIS_THRESHOLD:
            print("Move down")
            send_gcode("G91\nG1 Z-10 F1500")
            last_move_time = current_time

    if joystick.get_button(10):
        print("Home button")
        send_gcode("G28")
        time.sleep(0.2) 

    if joystick.get_button(0):
        print("Big Light")
        send_gcode("flashlight_switch")
        time.sleep(0.2)

    if joystick.get_button(1):
        print("small Light")
        send_gcode("modlelight_switch")
        time.sleep(0.2)

    if joystick.get_button(9):
        print("Motor Stop")
        send_gcode("M84")
        time.sleep(0.2)

    if joystick.get_button(6) and joystick.get_button(7):
        print("Shutting down...")
        send_gcode("M104 S0\nM140 S0\nM107\nM84")
        break


    hat_x, hat_y = joystick.get_hat(0)

    if hat_y == 1:
        print("Fan up")
        current_fanspeed = min(255, current_fanspeed + 25)
        send_gcode(f"M106 S{current_fanspeed}")
        time.sleep(0.2)
        if current_fanspeed == 255:
            print("Fan max")
        else:
            print(current_fanspeed)

    elif hat_y == -1:
        print("Fan down")
        current_fanspeed = max(0, current_fanspeed - 25)
        send_gcode(f"M106 S{current_fanspeed}")
        time.sleep(0.2)
        if current_fanspeed == 0:
            print("Fan off")
        else:
            print(current_fanspeed)

    if joystick.get_button(8):
        print("Heating PLA")
        send_gcode("M140 S65\nM104 S170")
        time.sleep(0.2)

    if joystick.get_button(7):
        print("Filament load")
        send_gcode(f"G1 E{filament_load} F{filament_speed}")
        time.sleep(0.2)

    if joystick.get_button(6):
        print("Filament unload")
        send_gcode(f"G1 E-{filament_load} F{filament_speed}")
        time.sleep(0.2)

    clock.tick(30)
