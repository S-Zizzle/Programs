from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui
import time

pyautogui.PAUSE = 0.005

start_time = time.time()
current_time = time.time()
time.sleep(2)

#METHOD 1 - SPAM CLICK

while True:
    for x in range(750,1175,70):
        pyautogui.click(x,860)

#METHOD 2 - DETECT CHANGE
'''
game_coords = [780,830,1050,870]

while True:
    time.sleep(1)
    if current_time < start_time+5:
        screen = np.array(ImageGrab.grab(bbox=game_coords))
        screen = cv2.cvtColor(screen, 6)

        super_threshold_indices = screen >= 40
        screen[super_threshold_indices] = 0
        points = np.nonzero(screen)

        print (points[0])

'''
'''
        for idxx,x in enumerate(range(game_coords[0],game_coords[2])):
            for idxy,y in enumerate(range(game_coords[1],game_coords[3])):
                if screen[idxy][idxx] < 40:
                    pyautogui.moveTo(x,y)
                    #pyautogui.click(x,y)
'''
'''

        current_time = time.time()
    else:
        quit()
'''

#METHOD 3 - TRACK BALL AND FOLLOW IT'S X POSITION, KEEPING Y CONSTANT, AND SPAM CLICKING