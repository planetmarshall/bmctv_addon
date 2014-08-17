__author__ = 'Andrew'

import unittest
import bmctv
import os.path

class TestExtractVideoInfo(unittest.TestCase):
    def setUp(self):
        with open(os.path.join("data","tv.thebmc.co.uk.htm")) as f:
            self.text = f.read()

    def test_extract_videos_on_page(self):
        videos = bmctv.available_videos(self.text)
        for title,info in videos.iteritems():
            print title
        pass


if __name__ == "__main__":
    unittest.main()