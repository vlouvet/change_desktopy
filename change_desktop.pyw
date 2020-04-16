import praw
import ctypes
import shutil
import requests
from PIL import Image
import os
import io

with open("reddit.creds.txt", "r") as fin:
    client_id = fin.readline().replace("\n", "")

if not os.path.isdir(os.path.join(os.path.expanduser("~"), "Desktop", "bgs")):
    os.mkdir(os.path.join(os.path.expanduser("~"), "Desktop", "bgs"))
    #directory created

directory = os.path.join(os.path.expanduser("~"), "Desktop", "bgs")
imagePath = os.path.join(directory, "test.png")
change_bg = 0

def changeBG(imagePath):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, imagePath, 0)


def img_resize(raw_img):
    basewidth = 1920
    baseheight = 1080
    img = Image.open(io.BytesIO(raw_img))
    # img = Image.open(raw_img)
    if img.size[0] < 1920:
        #resize img to a width of 1920p height
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    if img.size[1] < 1080:
        pass
    else:
        #resize img to a maximum of 1080p height
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseheight), Image.ANTIALIAS)
    return img



def get_submission(subreddit_name, limit):
    reddit = praw.Reddit(client_id=client_id,
                        client_secret="",
                        password="",
                        user_agent='vdesktopchange by /u/louvetvicente',
                        username='louvetvicente')
                        
    subreddit = reddit.subreddit(subreddit_name)
    for sub in subreddit.new(limit=limit):
        submission = sub # subreddit.random()
        r = requests.get(submission.url, stream=True)
        if not submission.over_18:
            if "https://i.redd.it/" in submission.url:
                filename = submission.url.replace("https://i.redd.it/", "")
            elif "https://i.imgur.com/" in submission.url:
                filename = submission.url.replace("https://i.imgur.com/", "")
            elif "https://imgur.com/" in submission.url:
                filename = submission.url.replace("https://i.imgur.com/", "")
            elif "https://live.staticflickr" in submission.url:
                filename = submission.url.replace("https://live.staticflickr.com/", "")
            else:
                # print("unknown file host, retrying")
                print(submission.url)
                pass
            exclude_list = [".gif", "gallery", "comments"]
            include_list = ["jpeg", "png", "jpg", "PNG", "JPEG", "JPG"]
            for ex_word in exclude_list:
                if ex_word not in submission.url:
                    for word in include_list:
                        if word in submission.url:
                            if r.status_code == 200:
                                r.raw.decode_content = True
                                img = img_resize(r.content)
                                if not filename in os.listdir(directory):
                                    imagePath = os.path.join(directory, filename)
                                    print(submission.title)
                                    print(submission.url)
                                    print(imagePath)
                                    img.save(imagePath)
                                    if change_bg != 0:
                                        changeBG(imagePath)
                                else:
                                    pass
                            else:
                                print("ERROR: "+str(r.status_code))
                                exit()
                            break
                    else:
                        # print("no match found in inclusion_list")
                        # print(submission.url)
                        pass
                else:
                    # print("match found in exclusion_list")
                    pass
        else:
            print("image was NSFW, retrying")
            pass

get_submission('wallpapers', 100)
