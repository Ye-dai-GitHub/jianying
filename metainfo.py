import time
import uuid
from pymediainfo import MediaInfo
from datetime import datetime


class DratfMetaInfo:

    def __init__(self, folder_path, data) -> None:
        now_time = int(time.time()*1000000)
        meta = data['draft_meta_info.json']
        meta['draft_fold_path'] = folder_path
        meta['tm_draft_create'] = now_time
        meta['tm_draft_modified'] = now_time
        meta['draft_id'] = str(uuid.uuid4())
        self.meta = meta

    def read_meta_info(self, path):
        info = MediaInfo.parse(path)
        general = info.general_tracks[0].to_data()
        video = info.video_tracks
        audio = info.audio_tracks
        image = info.image_tracks

        if not video and not image:
            audio = audio[0].to_data()
            metetype = 'music'
            height = 0
            width = 0
            duration = 0
            start = -0
        elif not video:
            image = image[0].to_data()
            height = image['height']
            width = image['width']
            metetype = 'photo'
            duration = -1
            start = -1
        else:
            video = video[0].to_data()
            metetype = 'video'
            height = video['height']
            width = video['width']
            duration = video['duration']*1000
            start = 0

        value = {
            "create_time": int(datetime.strptime(general['file_creation_date__local'], "%Y-%m-%d %H:%M:%S.%f").timestamp()),
            "duration": 5000000 if metetype == 'photo'else duration,
            "extra_info": general['complete_name'][general['complete_name'].rfind('/')+1:],
            "file_Path": general['complete_name'],
            "height": height,
            "id": str(uuid.uuid4()),
            "import_time": int(time.time()*10),
            "md5": "",
            "metetype": metetype,
            "roughcut_time_range": {"duration": duration, "start": start},
            "type": 0,
            "width": width
        }
        return value

    def append(self, path):
        meta_info = self.read_meta_info(path)
        self.meta['draft_materials'][0]['value'].append(meta_info)
