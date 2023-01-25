import pyautogui as pg
import time
import pyperclip
from io import BytesIO
import win32clipboard
from PIL import Image

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def copy_image(image_path):
    # resize the image to 300 x 200 and save it as image.jpg
    image = Image.open(image_path)
    image = image.resize((300, 200), Image.ANTIALIAS)
    image.save("images/image.jpg")
    
    image = Image.open('./images/image.jpg')
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)


def write_to_slides(word_data):
    imagePath = word_data["image_url"]
    # save the image data to clipboard
    copy_image(imagePath)

write_to_slides({"image_url": "images/apple/Image_1.jpg"})