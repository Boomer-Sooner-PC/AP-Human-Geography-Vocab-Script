import pyautogui as pg
import time
import pyperclip
from io import BytesIO
import win32clipboard
from PIL import Image
from get_info import get_info
import keyboard

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def copy_image(image_path):
    image = Image.open(image_path)
    # resize image to a maximum of 400 x 275 while maintaining aspect ratio
    image.thumbnail((400, 275), Image.ANTIALIAS)

    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)

def nextSlide():
    time.sleep(0.1)
    # hold down ctrl and alt
    pg.keyDown("ctrl")
    pg.keyDown("alt")
    # press u
    pg.press("u")
    # press a
    pg.press("a")
    # release ctrl and alt
    pg.keyUp("ctrl")
    pg.keyUp("alt")
    time.sleep(0.1)
    # press down
    pg.press("down")
    time.sleep(0.1)                                     

def processSlide():
    # go to next slide
    time.sleep(0.05)
    # press tab 5 times
    pg.press("tab", presses=10, interval=0.05)
    # copy to selected text to clipboard
    pg.hotkey("ctrl", "c")
    # get the text from clipboard
    text = pyperclip.paste().strip()
    try:
        text = text.split(":")[1].strip()
    except:
        print("Word not found")
        return
    print("word found:" + text)
    # get data from get_info.py
    try:
        data = get_info(text)
    except:
        # if word cannot be found
        print("Word not found")
        return
    # press tab 1 more times
    pg.press("tab", presses=1)
    # copy definition
    pyperclip.copy(data["definition"])
    # paste definition
    pg.hotkey("ctrl", "v")
    # tab 1 time
    pg.press("tab", presses=1)
    # copy charactaristics
    pyperclip.copy(data["charactaristics"])
    # paste charactaristics
    pg.hotkey("ctrl", "v")
    # tab 1 time
    pg.press("tab", presses=1)
    # copy example
    pyperclip.copy(data["example"])
    # paste example
    pg.hotkey("ctrl", "v")
    # copy image
    copy_image(data["image_url"])
    # past image
    pg.hotkey("ctrl", "v")
    time.sleep(3)
    # press right 28 times
    pg.press("right", presses=28)
    # press down 26 times
    pg.press("down", presses=26)
    time.sleep(0.3)


def main():
    ans = input("Would you like to do slide by slide or automatically? (s/a): ")
    if (ans == "s"):
        print("Ready to do slides. Press fn12 to process slide, make sure nothing is selected on the slide, ctrl+q to quit")
        while True:
            # if ctrl q is pressed break
            if keyboard.is_pressed("ctrl+q"):
                break
            # if fn 12 is pressed
            if keyboard.is_pressed("f12"):
                print("Processing slide")
                processSlide()
                print("Slide processed, awaiting next slide")
    if (ans == "a"):
        i = int(input("How many slides to do (not including title slide): "))
        print("Starting automatic mode, make sure you are on title page")
        print("Starting in 5 seconds")
        time.sleep(5)
        while (i > 0):
            nextSlide()
            processSlide()
            i -= 1
        print("Complete")
    

main()          