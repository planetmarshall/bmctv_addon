import sys
import xbmcgui
import xbmcplugin
import urlparse
import xbmc
import bmctv
import urllib2

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')

def read_html(url):
    f = urllib2.urlopen(url)
    data = f.read()
    f.close()
    return data

bmc_home = "http://tv.thebmc.co.uk/"

video_base_url = "http://dcwxwp7njqx1m.cloudfront.net"
video = "bmc/Fu7Gr/default.mp4"
url = urlparse.urljoin(video_base_url,video)

list_items = []
xbmc.log("BMCTV : Reading HTML from " + bmc_home)
available_videos = bmctv.available_videos(read_html(bmc_home))
xbmc.log("BMCTV : Retrieved {0} videos".format(len(available_videos)))
for title in available_videos:
    li = xbmcgui.ListItem(label=title)
#    label2=summary,
        #iconImage=info["thumbnail"],
        #thumbnailImage=info["thumbnail"])
    info = available_videos[title]
    xbmc.log("BMCTV : Adding title : " + title)
    list_items.append((url,li,False))

xbmcplugin.addDirectoryItems(addon_handle,list_items)
xbmcplugin.endOfDirectory(addon_handle)
#li.setInfo('video', {"Title":title,
#                     'PlotOutline':summary,
#                     'Plot':summary,
#                     'Year':'2014'})



#title = 'iWalk'
#summary = 'iWalk to find myself, to escape the city, to find freedom. Why do you walk?'
#thumbnail = urlparse.urljoin(video_base_url,"bmc/Fu7Gr/default_4.jpg")
#icon = urlparse.urljoin(video_base_url,"bmc/Fu7Gr/thumb_4.jpg")
#li = xbmcgui.ListItem(
#    label=title,
#    label2=summary,
#    iconImage=icon,
#    thumbnailImage=thumbnail)
#li.setInfo('video', {"Title":title,
#                     'PlotOutline':summary,
#                     'Plot':summary,
#                     'Year':'2014'})

#xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
#xbmcplugin.endOfDirectory(addon_handle)


