import os
import csv
import json

from apiclient.discovery import build

class BaseYoutube:
    def __init__(self):
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"
        self.DEVELOPER_KEY = open('apiKey').read()
        self.YOUTUBE = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=self.DEVELOPER_KEY)