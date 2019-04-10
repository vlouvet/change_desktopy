import praw
import ctypes
import shutil
import requests
from PIL import Image

directory = 'C:\\Users\\alma\\Desktop\\bgs\\'
imagePath = directory + "\test.png"

def changeBG(imagePath):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, imagePath, 0)
    return 0;


def img_resize(imagePath):
    baseheight = 1080
    img = Image.open(imagePath)
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    img.save(imagePath)


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
if r.status_code == 200:
    with open(filename, "wb") as fout:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, fout)  
    imagePath = directory+filename
    img_resize(imagePath)
    changeBG(imagePath)
else:
    print("ERROR: "+str(r.status_code))
