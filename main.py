import json
import time
import uuid
import os
from pymediainfo import MediaInfo
from datetime import datetime


dratf_root_path = 'D:/JianyingPro Drafts'


class dratf:

    def __init__(self, dratf_name) -> None:
        draft_fold_path = dratf_root_path + '/' + dratf_name
        if not os.path.exists(draft_fold_path):
            os.mkdir(draft_fold_path)

        self.meta_info = DratfMetaInfo(draft_fold_path)

        # height = 0  # 草稿高度
        # ratio = "original"  # 草稿比率
        # width = 0  # 草稿宽度

    def append_meta(self, path):
        self.meta_info.append(path)


class DratfMetaInfo:

    def __init__(self, fold_path=None, file_path=None) -> None:
        now_time = int(time.time()*1000000)
        file_path = "draft/draft_meta_info.json" if file_path is None else file_path
        with open(file_path, 'r', encoding='utf-8') as file:
            meta = json.load(file)
            if file_path is None:
                meta['draft_fold_path'] = fold_path
                meta['tm_draft_create'] = now_time
                meta['tm_draft_modified'] = now_time
                meta['draft_id'] = str(uuid.uuid4())
        self.meta = meta
        self.write()

    def append(self, path):
        # 读取媒体信息
        info = MediaInfo.parse(path)
        # 可删除部分 仅用于展示
        # with open('info.json', 'w', encoding='utf-8') as file:
        # json.dump(info.to_data(), file, indent='\t')
        # 类型判断
        general = info.general_tracks[0].to_data()
        video = info.video_tracks
        audio = info.audio_tracks
        image = info.image_tracks
        if len(video) == 0 and len(image) == 0:
            audio = audio[0].to_data()
            metetype = 'music'
            height = 0
            width = 0
            duration = 0
            start = -0
        elif len(video) == 0:
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
        # 修改
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
        # 添加到素材中 并保存
        self.meta['draft_materials'][0]['value'].append(value)
        self.write()

    def write(self):
        with open(self.meta['draft_fold_path']+'/draft_meta_info.json', 'w', encoding='utf-8')as file:
            json.dump(self.meta, file)


class DratfContent:

    def __init__(self, fold_path=None, file_path=None) -> None:
        file_path = "draft/draft_content.json" if file_path is None else file_path
        with open(file_path, 'r', encoding='utf-8') as file:
            content = json.load(file)
            if file_path is None:
                content['id'] = uuid.uuid4()

    def write(self):
        with open(self.meta['draft_fold_path']+'/draft_meta_info.json', 'w', encoding='utf-8')as file:
            json.dump(self.meta, file)


d = dratf("测试草稿")
d.append_meta("D:/Videos/Neo3/0a6d45e401664c12aaf22bd013024ea4.mp4")
d.append_meta(
    r"C:\FFOutput\0a6d45e401664c12aaf22bd013024ea4\0a6d45e401664c12aaf22bd013024ea4.aac")
d.append_meta("D:/Pictures/Neo3/-7udllh.jpg")
