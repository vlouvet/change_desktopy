# change_desktopy
changes desktop background using Reddit API on Windows 10


This code was initially intended for use in Windows 10, but may be expanded for use on Linux/Mac in the future.

update change_desktop.py to point to a folder where the images should be stored, this should also be where the script and the .creds file lives.

change_desktop.py - actual script that makes the magic happen

reddit.creds - required credential file including client_id, client_secret and password for your reddit account.

setup:

1. Register your account for use with Reddit API
2. Clone script from Github.
3. Create a blank text file, name it "reddit.creds" and enter your client_id, client_secret and password each on their own line. save and close the file.
4. Update change_desktop.py to point to a folder on your computer where the background images should live. save and close file
5. If the folder in step 4 doesn't already exists, create it now.
6. Optionally, setup Windows task scheduler to run the script every 1, 5, or 60 minutes :-)
