import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
import urlparse
import xbmc
import bmctv
import urllib2

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
cache = StorageServer.StorageServer("plugin.video.bmctv", 24)

plugin_url = sys.argv[0]
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo("path")

def read_html(url):
    f = urllib2.urlopen(url)
    data = f.read()
    f.close()
    return data

bmc_root = "tv.thebmc.co.uk"
bmc_home = "http://" + bmc_root


args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)

def read_all(pages, channel_link):
    list_items = []
    for i in range(1,pages+1):
        page_url = bmctv.build_url(channel_link,i)
        xbmc.log("BMCTV : Reading HTML from " + page_url)
        available_videos = cache.cacheFunction(bmctv.available_videos,read_html(page_url))

        for title, info in available_videos.iteritems():
            item_url = bmctv.build_item_url(plugin_url, info )
            list_items.append({"title":title, "url":item_url, "info":info})
    return list_items

if mode is None:
    # startup index page
    channels = bmctv.available_channels(read_html(bmctv.build_url("/",1)))
    channel_items = []
    for channel, link in channels:
        li = xbmcgui.ListItem(label=channel, thumbnailImage=bmctv.get_channel_icon(addon_path,channel))
        channel_items.append((bmctv.build_channel_url(plugin_url,channel,link), li, True))
    xbmcplugin.addDirectoryItems(addon_handle, channel_items)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == "channel":
    channel=args.get('channel')[0]
    channel_link = args.get('link')[0]
    pages = bmctv.available_pages(read_html(bmctv.build_url(channel_link,1)))
    list_items = []
    for item in cache.cacheFunction(read_all,pages,channel_link):
        info = item["info"]
        li = xbmcgui.ListItem(label=item["title"], thumbnailImage=info["thumbnail"])
        list_items.append((item["url"], li,True))

    xbmcplugin.addDirectoryItems(addon_handle,list_items)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == "video":
    page_url = urlparse.urljoin(bmc_home,args.get('page_url')[0])
    video_info = bmctv.video_info(read_html(page_url))
    li = xbmcgui.ListItem(
        label=video_info.title,
        label2=video_info.summary,
        iconImage=video_info.image,
        thumbnailImage=video_info.image)
    # TODO
    li.setInfo('video', {
        'title': video_info.title,
        'plotoutline': video_info.summary,
        'plot': video_info.description
    })
    #
    li.addStreamInfo('video', {'height': 720 })
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=video_info.video["720p"], listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)


