import praw
from requests import get
from PIL import Image
import PIL.ImageOps
import pyimgur
import time
import os


client_id = 'XXXX'
client_secret = 'XXXX'
reddit_user = 'XXXX'
reddit_pass = 'XXXX'
user_agent = '!invert bot (by u/impshum)'
imgurid = 'XXXX'
target_sub = 'XXXX'
target_word = '!nvert'

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=reddit_user,
                     password=reddit_pass)


def get_parent_id(comment):
    parent = comment.parent()
    permalink = parent.permalink
    parent_id = permalink.split('/')[4]
    return parent_id


def invert_image(file):
    image = Image.open(file)
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.save(file)


def upload(file_upload, title):
    im = pyimgur.Imgur(imgurid)
    uploaded_image = im.upload_image(file_upload, title=title)
    img_link = uploaded_image.link
    img_link = img_link.replace('https://i.imgur.com/', '')
    img_link = 'https://recycledrobot.co.uk/imgee/?i={}'.format(img_link)
    os.remove(file_upload)
    return img_link


start_time = int(time.time())

for comment in reddit.subreddit(target_sub).stream.comments():
    if start_time < int(comment.created_utc):
        if target_word in comment.body:
            parent_id = get_parent_id(comment)
            submission = reddit.submission(id=parent_id)

            url = submission.url
            if url.startswith(('http://i.imgur.com', 'https://i.imgur.com', 'http://i.redd.it', 'https://i.redd.it')) and url.endswith(('.jpg', '.png', '.jpeg')):
                fname = url.rsplit('/', 1)[-1]
                img_data = get(url).content

                with open(fname, 'wb') as f:
                    f.write(img_data)

                invert_image(fname)
                image_link = upload(fname, 'Inverted')
                comment.reply(f'Here is your inverted image: [link]({image_link})')
                print(image_link)
