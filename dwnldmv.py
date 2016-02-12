#!/usr/bin/env python

import urllib, sys, json
from subprocess import call
import config

usage = "Usage: \n- Configure the params at config.py for first time \n- use " + sys.argv[0] + " <EventIdentifier> \ne.g. " + sys.argv[0] + "  interzum2015 \nBe sure of the identifier "
try:
    identifier = sys.argv[1]
    #identifier = "interzum2015"
except IndexError:
    print usage
    sys.exit(1)

if(identifier == "-h"):
    print usage
    sys.exit(1)

url = config.url + "&event_identifier=" + identifier

filename = "urls.json"

print "Downloading json packages file for " + identifier + " from " + url
urllib.urlretrieve(url,filename)
print "Done!\n"

jdata = open(filename)
data = json.load(jdata)
jdata.close()

#urls
ap = [None]*3
ap[0] = data["packages"]["android.app_config"]
ap[1] = data["packages"]["android.build_configuration"]
ap[2] = data["packages"]["android.events_content"]

ip = [None]*3
ip[0] = data["packages"]["ios.app_config"]
ip[1] = data["packages"]["ios.build_configuration"]
ip[2] = data["packages"]["ios.events_content"]

#filenames
a_app_config_file = "android_app_config.tar.gz"
a_build_configuration_file = "android_build_configuration.tar.gz"
a_events_content_file = "android_events_content.tar.gz"

if(config.platform == "ios"):
    i_app_config_file = ip[0].split('/')[8]
    i_build_configuration_file = ip[1].split('/')[8]
    i_events_content_file = ip[2].split('/')[8]

tmp_dir = config.tmp_dir
path_to_assets = config.path_to_assets

if(config.platform == "android"):
    print "Downloading Android packages..."
    urllib.urlretrieve(ap[0], tmp_dir + a_app_config_file)
    urllib.urlretrieve(ap[1], tmp_dir + a_build_configuration_file)
    urllib.urlretrieve(ap[2], tmp_dir + a_events_content_file)
    print "Done!\n"

    build_config_file = "android_build_configuration/assets__app_config.json"
    print "Moving to assets Dir... " + path_to_assets
    call(["mv",  "-v", tmp_dir + a_app_config_file, path_to_assets + a_app_config_file])
    call(["mv", "-v", tmp_dir +  a_events_content_file, path_to_assets + a_events_content_file])
    call(["tar", "-C", tmp_dir, "-zxvf", tmp_dir +  a_build_configuration_file, build_config_file])
    call(["mv", "-v", tmp_dir + build_config_file, path_to_assets + "app_config.json" ])
    print "Done!\n"

    adb_cmd = config.path_to_sdk + "adb"
    print adb_cmd
    #call([adb_cmd, "shell", "pm", "uninstall", "de.mobileeventguide.megap"])
    #/Users/ssalman/Library/Android/sdk/platform-tools/adb shell pm uninstall de.mobileeventguide.megapp

else:
    print "Downloading iOS packages..."
    urllib.urlretrieve(ip[0], tmp_dir + i_app_config_file)
    urllib.urlretrieve(ip[1], tmp_dir + i_build_configuration_file)
    urllib.urlretrieve(ip[2], tmp_dir + i_events_content_file)
    print "Done!\n"

    build_config_file = "ios_build_configuration/app_config.json"
    print "Moving to assets Dir... " + config.path_to_assets
    call(["mv", "-v", tmp_dir + i_app_config_file, path_to_assets + i_app_config_file])
    call(["mv", "-v", tmp_dir + i_events_content_file, path_to_assets + i_events_content_file])
    call(["tar", "-C", tmp_dir, "-zxvf", tmp_dir + i_build_configuration_file, build_config_file])
    call(["mv", "-v", tmp_dir + build_config_file, path_to_assets + "app_config.json" ])
    print "Done!\n"

print identifier + " packages were downloaded to " + tmp_dir + " and moved to the assets folder of " + config.platform + " platform"

# {
#   "packages": {
#     "ios.app_config": "",
#     "ios.build_configuration": "https://adminstg.s3.amazonaws.com/uploads/valubuild_configuration.tar.gz",
#     "ios.events_content": "https://adminstg.s3e/cloud_file_va44/ios_events_content.tar.gz",
#     "android.app_config": "h.amazonaws.com/uploads/value_type/cloud_file_va/android_app_config.tar.gz",
#     "android.build_configuration": "azonaws.com/uploads/value_type/cloud_file_va/android_build_configuration.tar.gz",
#     "android.events_content": "https://adminstg.s3.amazonaws.com/upload/android_events_content.tar.gz"
#   }
# }
#
