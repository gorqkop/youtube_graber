import os
import json
import csv

from apiclient.errors import HttpError
from apiclient.discovery import build

class youtube_grabber:
    def __init__(self):
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"
        self.DEVELOPER_KEY = 'AIzaSyAjLsHi5V_q99YXOYladt_nSqxSHgSmlj0'
        self.YOUTUBE = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=self.DEVELOPER_KEY)

    def get_comments(self, video_id, path=''):
        self.comments = []
        try:
            video_comment_threads = self.__get_comment_threads(video_id)
            for thread in video_comment_threads:
                self.__get_comments(thread["id"], video_id)
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

        output_file = open(os.path.join(path, '%s.csv' % video_id), 'w')
        csvwriter = csv.writer(output_file, delimiter='\t')
        csvwriter.writerow(['Text', 'OriginalText', 'Data', 'Like', 'Name', 'IdVideo', 'IdComment', 'IdInnerComment'])
        for comment in self.comments:
            print(comment)
            csvwriter.writerow(json.loads(comment))
        output_file.close()
        print("Total comments: %d" % len(self.comments))


    def __get_comment_threads(self, video_id):
        threads = []
        results = self.YOUTUBE.commentThreads().list(part="snippet", videoId=video_id, textFormat="plainText").execute()
        # Get the first set of comments
        for item in results["items"]:
            threads.append(item)
            self.__pars_dict(item)
            if (item['snippet']['totalReplyCount'] > 0):
                res2 = self.__comments_list('snippet', item['id'])
                for item2 in res2['items']:
                    commentL = list()
                    commentL.append(item2['id'])
                    commentL.append(item2['snippet']['authorChannelUrl'])
        # Keep getting comments from the following pages
        while ("nextPageToken" in results):
            results = self.YOUTUBE.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=results["nextPageToken"],
                textFormat="plainText",
            ).execute()
            for item in results["items"]:
                threads.append(item)
                self.__pars_dict(item)
        return threads

    def __comments_list(self, part, parent_id):
        results = self.YOUTUBE.comments().list(
            parentId=parent_id,
            part=part
        ).execute()
        return results

    def __get_comments(self, parent_id, video_id):
        results = self.YOUTUBE.comments().list(
            part="snippet",
            parentId=parent_id,
            textFormat="plainText"
        ).execute()
        for item in results["items"]:
            text = item["snippet"]["textDisplay"]
            textOriginal = item["snippet"]["textOriginal"]
            data = item["snippet"]["updatedAt"]
            like = item["snippet"]["likeCount"]
            name = item["snippet"]["authorDisplayName"]
            parentId = item["snippet"]["parentId"]
            coment_Id = item["id"]
            info = [text, textOriginal, data, like, name, video_id, parentId, coment_Id]
            info = json.dumps(info, ensure_ascii=False)
            self.comments.append(info)

    def __pars_dict(self, item):
        comment = item["snippet"]["topLevelComment"]
        text = comment["snippet"]["textDisplay"]
        textOriginal = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
        data = item["snippet"]["topLevelComment"]["snippet"]["updatedAt"]
        like = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        name = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        id_videoo = item["snippet"]["topLevelComment"]["snippet"]["videoId"]
        parent_id = item["snippet"]["topLevelComment"]["id"]
        coment_Id = 'NoInderTwit'
        info = [text, textOriginal, data, like, name, id_videoo, parent_id, coment_Id]
        info = json.dumps(info, ensure_ascii=False)
        self.comments.append(info)

if __name__ == "__main__":
    youtube_grabber().get_comments('5UmMcLLlhsw')