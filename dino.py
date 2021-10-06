# Tyler Carpenter
# tylercarpenter1996@gmail.com
# High Score 272688 (10 OCT 21)

# Currently set up for a 1000 x 750 Chrome window
# Any other sizes will need adjustment for the capture

import cv2 as cv
import numpy as np

import os

import win32ui
import win32api
import win32gui
import win32con

import threading

import time
from math import exp

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def control(x,y):
  '''Presses a key based on distance and height of obstacles passed in'''

  # Logistic Differential Equation for Growth over Time
  # t         (time)
  # Po = 60   (initial population)
  # K = 380   (carrying capacity)
  # r = 0.05  (growth rate)

  t = int(time.time() - loop_time)
  Po = 60 
  K = 380
  r = 0.05

  dis = int(Po * K * exp(r * t)) / ((K - Po) + (Po * exp(r * t)))

  # Check if obstacle is close enough to jump over
  if (x < dis):
    # Check if the center point is at head height
    if y < 20:
      # === DUCK ===
      time.sleep(0.05) # Doesn't take long to duck
      win32api.keybd_event(0x28, 0,0,0) # Down Arrow
      time.sleep(0.4)
      win32api.keybd_event(0x28,0 ,win32con.KEYEVENTF_KEYUP ,0)
    else:
      # === JUMP ===
      win32api.keybd_event(0x26, 0,0,0) # Up Arrow
      time.sleep(0.2) # Depending on how long this is, you can make shorter jumps
      win32api.keybd_event(0x26,0 ,win32con.KEYEVENTF_KEYUP ,0)

def gameOver(center):
  '''Check if the game is over by searching for the center point of the restart button'''
  return center == (394, 11) # Will need adjustment for a different screen size

def capture(r, b, l, t): 
  '''Captures the screen with modifiers on the position of the screen'''

  # Get the handle to the window by the given name
  hwndtarget = win32gui.FindWindow(None, 'chrome://dino/ - Google Chrome')

  # Define the window size
  left, top, right, bot = win32gui.GetWindowRect(hwndtarget)

  # Get the width with the 'r' modifier effecting the overall width
  w = right - left - r

  # Get the height with the 'b' modifier effecting the overall height
  h = bot - top - b

  # Make the window the front target
  win32gui.SetForegroundWindow(hwndtarget)

  hdesktop = win32gui.GetDesktopWindow()
  hwndDC = win32gui.GetWindowDC(hdesktop)
  mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
  saveDC = mfcDC.CreateCompatibleDC()

  # Create the bitmap image of the given height and width
  saveBitMap = win32ui.CreateBitmap()
  saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
  
  saveDC.SelectObject(saveBitMap)
  saveDC.BitBlt((0, 0), (w, h), mfcDC, (left + l, top + t), win32con.SRCCOPY) # Bit Block

  # Reformat the image to be used with OpenCV
  signedIntsArray = saveBitMap.GetBitmapBits(True)
  img = np.array(list(signedIntsArray),'uint8')
  img.shape = (h, w, 4)

  # Clean Up
  win32gui.DeleteObject(saveBitMap.GetHandle())
  saveDC.DeleteDC()
  mfcDC.DeleteDC()
  win32gui.ReleaseDC(hdesktop, hwndDC)

  return img

# Used for multi-iteration testing
iteration = 0

# Main Loop
while (True): 
  
  if (iteration != 0) :
    score = capture(750, 635, 730, 181) # Will need adjustment for a different screen size
    cv.imwrite('./scores/score{}.jpg'.format(iteration), score)

    death = capture(700, 550, 10, 302) # Will need adjustment for a different screen size
    cv.imwrite('./death/death{}.jpg'.format(iteration), death)

    iteration += 1

  # Restart the game
  win32api.keybd_event(0x26, 0,0,0) # Down Arrow
  time.sleep(0.2)
  win32api.keybd_event(0x26,0 ,win32con.KEYEVENTF_KEYUP ,0) 

  # Start the loop timer
  loop_time = time.time()

  # Initial game loop logic
  isGameOver = False  

  while(not(isGameOver)):

    # Grab the screen shot
    screenshot = capture(120, 695, 105, 335) # Will need adjustment for a different screen size
    #cv.imshow('Capture', screenshot)  # Show View

    # Create a high contrast image for canny edge detector
    # Allow detection through day and night cycle
    (_, bwscreenshot) = cv.threshold(screenshot, 127, 255, cv.THRESH_BINARY)
    #cv.imshow('BW Screen Shot', bwscreenshot) # Show View

    # Canny Edge detector
    edge = cv.Canny(bwscreenshot,10, 100)
    #cv.imshow('Canny Edge', edge) # Show View
    cv.imwrite('./cap/edge{}.jpg'.format(iteration), edge)


    # For visualization 
    # Create a blank mask
    mask = screenshot.copy()
    mask[:] = 0

    # Find the contours from the canny edges
    contours, _ = cv.findContours(edge,
      cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    for c in contours:
      # Get the bounding circle and the center point
      (cx,cy), radius = cv.minEnclosingCircle(c)  

      # int casting
      center = (int(cx), int(cy))
      radius = int(radius)

      # For visualization
      # Draw a circle on the mask to show detected obstacles
      cv.circle(mask, center, radius, (0,255,0), 2)
      
      # Check if the game over object was detected
      isGameOver = gameOver(center)

      # Send positions of detected obstacles to the controller
      # Controller is on a thread so that the object detection can run without 
      # the pauses of the key presses interupting
      controlThread = threading.Thread(target=control, args=(cx+(radius/2),cy))
      controlThread.start()

    # Show the mask with detected obstacles
    cv.imshow('Obstacle Detection', mask) # Show View


    # Wait for the q key
    if cv.waitKey(1) == ord('q'):
      break