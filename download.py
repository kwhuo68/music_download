#!/usr/bin/python
import time, re, os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import shutil
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


#set this to your API key value from your project
DEVELOPER_KEY = "-----------------------"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

video_id = ""

""" Handles special formatting from the downloading of the mp3 """
def replaceFormat(str1):
  new_str1 = ""
  for x in str1:
    if x != '/':
      if x == "&":
        new_str1 += "&amp;"
      elif x == "|":
        new_str1 += "-"
      else:
        new_str1 += x  
  return new_str1

""" Used to get a rough match of the file names """
def charMatch(str1, str2):
  #str1 is the name of the youtube file
  #str2 is name of the downloaded file
  count = 0
  minlen = 0
  if len(str1) < len(str2):
    minlen = len(str1)
  else:
    minlen = len(str2)
  for i in xrange(0, minlen):
    if str1[i:i+1] == str2[i:i+1]:
      count += 1
  return float(count)/minlen

"""Retrieves the top youtube search of your query, gets the youtube-to-mp3 result, and puts that .mp3 file in a folder of your choice."""
def download_song(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  #gets the query
  search_response = youtube.search().list(
    q=options.q + " lyrics",
    part="id,snippet",
  ).execute()

  videos = []

  #adds results to a video list
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s#%s" % (search_result["snippet"]["title"],
        search_result["id"]["videoId"]))

  first_video = videos[0]
  video_title = first_video.split("#")[0]
  video_id = first_video.split("#")[1].strip()
  new_title = replaceFormat(video_title)

  #insert the path to chromedriver here
  path_to_chromedriver = '------------'
  browser = webdriver.Chrome(executable_path = path_to_chromedriver)

  url = 'http://www.youtube-mp3.org/#v=' + video_id
  browser.get(url)

  #the javascript changes from 2-4 varying on the video url
  try:
    browser.find_element_by_xpath('//*[@id="error_text"]/b')
    print "Youtube blocked this song from being able to be downloaded - sorry!"
    browser.close()
    return False
  except NoSuchElementException:
    dl_file = None
    try:
      browser.find_element_by_xpath('//*[@id="dl_link"]/a[3]/b')
      dl_file = browser.find_element_by_xpath('//*[@id="dl_link"]/a[3]/b')
      dl_file.click()
    except ElementNotVisibleException:
      try: 
        browser.find_element_by_xpath('//*[@id="dl_link"]/a[2]/b')
        dl_file = browser.find_element_by_xpath('//*[@id="dl_link"]/a[2]/b')
        dl_file.click()
      except ElementNotVisibleException:
        try:
          browser.find_element_by_xpath('//*[@id="dl_link"]/a[4]/b')
          dl_file = browser.find_element_by_xpath('//*[@id="dl_link"]/a[4]/b')
          dl_file.click()
        except ElementNotVisibleException:
          print "Cannot find the download link for this song - sorry!"

  #put your downloads folder path here
  download_path = '-----------'  
  downloaded = False
  while(downloaded == False):
    #handles both expected titles and altered download titles
    if os.path.isfile(download_path + video_title + ".mp3"):
      downloaded = True
      break
    elif os.path.isfile(download_path + replaceFormat(video_title) + ".mp3"):
      downloaded = True
      break
    else:
      time.sleep(2)
  
  print "done sleeping - file was found in downloads."
  found_file = False
  desired_file = None

  for file in os.listdir(download_path + '/'):
    if(charMatch(video_title, file) > 0.50):
      print "found good video title %s" %video_title
      if found_file == False:
        desired_file = file
        found_file = True
        break
  
  mp3_name = video_title + ".mp3"
  #insert the directory you wish the song to go to here
  desired_dir_path = '-----------'
  if os.path.isfile(desired_dir_path + "/" + desired_file):
    print "file already exists in your folder!"
    browser.close()
    return False
  shutil.move(download_path + '/' + desired_file, desired_dir_path)
  browser.close()

  return True

if __name__ == "__main__":
  argparser.add_argument("--q", help="Search for", default="Hello World")
  args = argparser.parse_args()

  try:
    download_song(args)
  except HttpError, e:
    print "HTTP error code of %d happened:\n%s" % (e.resp.status, e.content)