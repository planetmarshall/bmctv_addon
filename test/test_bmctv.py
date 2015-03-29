
__author__ = 'Andrew'
import unittest
import os
import os.path
import bmctv
from urlparse import urljoin

class TestExtractVideoInfo(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir,"data","tv.thebmc.co.uk.htm")) as f:
            self.text = f.read()

    def test_build_video_url(self):
        expected = "http://tv.thebmc.co.uk/channel/climbing?page=1"
        self.assertEqual(expected, bmctv.build_url("/channel/climbing", 1))

    def test_get_available_pages(self):
        pages = bmctv.available_pages(self.text)
        self.assertEqual(24, pages)

    def test_get_available_videos(self):
        videos = bmctv.available_videos(self.text)
        video_titles = set(videos.keys())
        self.assertTrue("EOFT Teaser" in video_titles)
        self.assertTrue("iWalk" in video_titles)

        info = videos["iWalk"]
        self.assertEqual(
            "/video/iwalk?current-channel=all-channels",
            info["page_url"])

    def test_get_available_channels(self):
        channels = bmctv.available_channels(self.text)
        expected_channels = [
            ("All Channels","/"),
            ("Walking","/channel/walking"),
            ("Climbing","/channel/climbing"),
            ("Mountains", "/channel/mountains"),
            ("Skills","/channel/skills"),
            ("Gear","/channel/gear"),
            ("Competition Climbing","/channel/competition-climbing"),
             ("Kendal Mountain Festival","/channel/kendal-festival"),
             ("The BMC", "/channel/the-bmc"),
             ("Award Schemes","/channel/award-schemes")
        ]
        for (expected_channel, expected_link),(channel, link) in zip(expected_channels,channels):
            self.assertEqual(expected_channel, channel)
            self.assertEqual(expected_link, link)

    def test_build_channel_url(self):
        channel_url = bmctv.build_channel_url("plugin.video.bmctv","Climbing","/channel/climbing")
        pass

class TestExtractVideo(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir,"data","mina.htm")) as f:
            self.text = f.read()

    def test_extract_video_info(self):
        info = bmctv.video_info(self.text)
        self.assertEqual("Mina Leslie-Wujastyk: Rocklands 2014", info.title)
        self.assertEqual("Mina Leslie-Wujastyk climbing 8a classics in Rocklands 2014 by Dave Mason", info.summary)
        description = '"This summer in South Africa I put a lot of effort into one climb: The Vice (8B)," explains Mina. "' \
        'I tried really hard but eventually threw the towel in, knowing I needed to come back stronger. Once I had stopped trying it, ' \
        'I turned my hand to some slightly easier classics that Rocklands and Cape Town have to offer and this video shows a few of them."'
        self.assertEqual(description, info.description)

    def test_extract_video_urls(self):
        info = bmctv.video_info(self.text)
        urls = info.video
        base_video_url = "http://dcwxwp7njqx1m.cloudfront.net/bmc/QoFGr/"
        self.assertEqual(urls["default"], urljoin(base_video_url,"default.mp4"))
        self.assertEqual(urls["720p"], urljoin(base_video_url,"hd.mp4"))
        self.assertEqual(urls["1080p"], urljoin(base_video_url,"hd1080.mp4"))


if __name__ == "__main__":
    unittest.main()