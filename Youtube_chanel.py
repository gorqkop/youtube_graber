import os
import csv
import json

from youtube import BaseYoutube

class YoutubeChannelGrabber(BaseYoutube):
    def get_video_info(self, video_id, path=''):
        self.video_info = []
        chan_id = self.get_my_uploads_list(video_id)
        self.list_my_uploaded_videos(chan_id)

        output_file = open(os.path.join(path, '%s.csv' % video_id), 'w')
        csvwriter = csv.writer(output_file, delimiter='\t')
        csvwriter.writerow(['Text', 'IdVideo', 'Data'])
        for info in self.video_info:
            print(info)
            csvwriter.writerow(json.loads(info))
        output_file.close()

    def get_my_uploads_list(self, channel_id):
        channels_response = self.YOUTUBE.channels().list(id=channel_id, part='contentDetails').execute()

        for channel in channels_response['items']:
            chan_id = channel['contentDetails']['relatedPlaylists']['uploads']
            return chan_id

    def list_my_uploaded_videos(self, chan_id):
        playlistitems_list_request = self.YOUTUBE.playlistItems().list(playlistId=chan_id, part='snippet')
        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()
            for playlist_item in playlistitems_list_response['items']:
                title = playlist_item['snippet']['title']
                video_id = playlist_item['snippet']['resourceId']['videoId']
                publise_time = playlist_item['snippet']['publishedAt']
                AUT = json.dumps([title, video_id, publise_time], ensure_ascii=False)
                self.vidio_info.append(AUT)
                print(AUT)
            playlistitems_list_request = self.YOUTUBE.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response)


if __name__ == "__main__":
    YoutubeChannelGrabber().get_vidio_info('UCWCOM4FH3_BJ5EDJ5wg0zfg')

