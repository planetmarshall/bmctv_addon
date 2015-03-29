from bs4 import BeautifulSoup
from urllib import urlencode
from urlparse import urljoin, urlunparse
from HTMLParser import HTMLParser
import os
import re

page_expr = re.compile("[0-9]+$")

channel_icons = {
    "Walking":"walking.png",
    "Climbing":"climbing.png",
    "Mountains": "mountaineering.png",
    "Feature Films": "films.png",
    "Skills":"skills.png",
    "Gear":"gear.png",
    "Competition Climbing":"competitions.png",
    "Kendal Mountain Festival":"kmf.png",
    "Award Schemes":"award.png"
}

class Video:
    def __init__(self, title, summary, description,image, video_urls):
        self.title = title
        self.summary = summary
        self.description = description
        self.image = image
        video = dict()
        for res,url in zip( ("default","720p","1080p"), video_urls):
            video[res] = url
        self.video = video

def build_item_url(base, video_info):
    video_info["mode"] = "video"
    return base + "?" + urlencode(video_info)

def build_channel_url(base, channel, channel_link):
    return base + "?" + urlencode({"mode": "channel",
                            "channel": channel,
                            "link" : channel_link})

def build_url(channel, page):
    query = [("page", page)]
    return urlunparse((
        "http", # scheme
        "tv.thebmc.co.uk", # netloc
        channel, # path
        "", # params
        urlencode(query), # query
        "", # fragment
    ))

def available_pages(text):
    bs = BeautifulSoup(text, "html.parser")
    last_page = bs.find("li",class_="last")
    return int(page_expr.search(last_page.a["href"]).group(0))

def available_videos(text):
    bs = BeautifulSoup(text, "html.parser")
    video_list = bs.find('ul', { 'class':'video-list'})
    videos = dict()
    for video in video_list.findAll("a"):
        img_tag = video.find("img")
        videos[video["title"]] = {
            "page_url" : video["href"],
            "thumbnail" : img_tag["src"]
            }
    return videos

def available_channels(text):
    bs = BeautifulSoup(text, "html.parser")
    channel_items = bs.find_all("li", id=re.compile("^channel"))
    channels = []
    for channel in channel_items:
        link = channel.a
        title = " ".join(s[0].upper() + s[1:] for s in link.span.text.split(" "))
        channels.append((title, link["href"]))
    return channels

def get_channel_icon(root, channel_name):
    icon = channel_icons.get(channel_name,"bmc.png")
    return os.path.join(root, 'resources', 'img', icon)


def video_info(text):
    bs = BeautifulSoup(text, "html.parser")
    title = bs.find("meta", attrs={"property":"og:title"})["content"]
    summary = bs.find("meta", attrs={"property":"og:description"})["content"]
    image = bs.find("meta", attrs={"property":"og:image"})["content"]

    details = bs.find("div", id="videoDetails")
    h = HTMLParser()
    description = h.unescape(unicode(details.find("p").string))

    return Video(title, summary, description, image,
                 [urljoin(image, res) for res in ["default.mp4","hd.mp4","hd1080.mp4"]])



