import bs4
import xbmc

def available_videos(text):
    xbmc.log("BMCTV : Text length : {0}".format(len(text)))
    bs = bs4.BeautifulSoup(text)
    video_list = bs.find('ul', class_='video-list')
    videos = dict()
    for video in video_list.find_all("a"):
        img_tag = video.find("img")
        videos[video["title"]] = {
            "page_url" : video["href"],
            "thumbnail" : img_tag["src"]
            }
    return videos


