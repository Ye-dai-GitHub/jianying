import json
import os
from metainfo import DratfMetaInfo
import config


class dratf:

    def __init__(self, draft_name, cover=True) -> None:
        # 新草稿文件夹目录
        self.folder_path = os.path.join(
            config.draft_config["root_path"], draft_name)
        self.file_names = config.draft_file_names
        self.folder_names = config.draft_folder_names

        self.data = {}

        # 草稿是否存在
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            for folder_name in self.folder_names:
                os.mkdir(os.path.join(self.folder_path, folder_name))
        self.load(target=not cover)

        self.meta = DratfMetaInfo(self.folder_path, self.data)

    def add_meta(self, path):
        self.meta.append(path)

    def load(self, target=False):
        # 加载源或者是目标文件
        for name in self.file_names:
            path = os.path.join(
                self.folder_path, name) if target else os.path.join('draft', name)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    if '.json' in name:
                        self.data[name] = json.load(f)
                    else:
                        self.data[name] = f.read()
            except Exception as e:
                print(f"An error occurred when loading {name}: {str(e)}")

    def save(self):
        # 保存文件到草稿目录
        for item in self.data:
            path = os.path.join(self.folder_path, item)
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    if '.json' in item:
                        json.dump(self.data[item], f)
                    else:
                        f.write(self.data[item])
            except Exception as e:
                print(f"An error occurred when saving {item}: {str(e)}")


d = dratf("测试")
d.add_meta(R"D:\Videos\Neo3\0a6d45e401664c12aaf22bd013024ea4.mp4")
d.save()
