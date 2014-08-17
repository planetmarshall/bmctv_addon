__author__ = 'Andrew'

from zipfile import ZipFile
import os
import os.path
import argparse

includes = [
    "resources",
    "addon.xml",
    "bmctv.py",
    "bmctv_main.py",
    "changelog.txt",
    "icon.png",
    "LICENSE.txt"
]

package = "plugin.video.bmctv"

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--version", help="plugin version")
args = parser.parse_args()

script_dir = os.path.dirname(os.path.realpath(__file__))
current_dir = os.getcwd()
os.chdir(script_dir)
with ZipFile(os.path.join(script_dir,"..", package + "-{0}.zip".format(args.version)), 'w') as zip:
    for include in includes:
        zip.write(include, os.path.join(package,include))
