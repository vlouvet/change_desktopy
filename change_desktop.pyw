import praw
import ctypes
import shutil
import requests
import PIL
from PIL import Image
import os


if not os.path.isdir(os.path.join(os.path.expanduser("~"), "Desktop", "bgs")):
    os.mkdir(os.path.join(os.path.expanduser("~"), "Desktop", "bgs"))
    #directory created

directory = os.path.join(os.path.expanduser("~"), "Desktop", "bgs")
imagePath = os.path.join(directory, "test.png")

def changeBG(imagePath):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, imagePath, 0)

def img_resize(raw_img):
    basewidth = 1920
    baseheight = 1080
    img = Image.open(r.raw)
    if img.size[0] < 1920:
        #resize img to a width of 1920p height
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    if img.size[1] < 1080:
        pass
    else:
        #resize img to a maximum of 1080p height
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    return img

with open("reddit.creds", "r") as fin:
    client_id = fin.readline().replace("\n", "")
    client_secret = fin.readline().replace("\n", "")
    password = fin.readline().replace("\n", "")

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent='vdesktopchange by /u/louvetvicente',
                     username='louvetvicente')
                     
subreddit = reddit.subreddit('art')

submission = subreddit.random()

r = requests.get(submission.url, stream=True)
if "https://i.redd.it/" in submission.url:
    filename = submission.url.replace("https://i.redd.it/", "")
elif "https://i.imgur.com/" in submission.url:
    filename = submission.url.replace("https://i.imgur.com/", "")
if ".gif" in submission.url:
    pass
else:
    if r.status_code == 200:
        r.raw.decode_content = True
        img = img_resize(r.raw)
        imagePath = os.path.join(directory, filename)
        print(imagePath)
        img.save(imagePath)
        changeBG(imagePath)
    else:
        print("ERROR: "+str(r.status_code))
