import os
import sys
import ffmpeg

from dataclasses import dataclass
from .track import Track
from .task_status import TaskStatus

@dataclass
class Task:
    """ 转换任务实体类 """
    path: str
    name: str
    format: str
    targetFormat: str
    progress: int
    status: TaskStatus
    tracks: list

    @staticmethod
    def initTaskOnlySource(path):
        return Task.initTask(path, None)

    @staticmethod
    def initTask(path, targetFormat):
        if not os.path.exists(path):
            print("file not exists")
            return None

        if not os.path.isfile(path):
            print("file is dir")
            return None

        name = os.path.basename(path)
        format = name.split(".")[1]
        tracks = []

        try:
            probe = ffmpeg.probe(path)
            for p in probe["streams"]:
                tracks.append(Track(p["codec_type"], p["codec_name"], p))
        except ffmpeg.Error as e:
            print(e.stderr, file=sys.stderr)
            return None

        return Task(path, name, format, targetFormat, 0, TaskStatus.CREATED, tracks)

    def startTask(self):
        pass

    def stopTask(self):
        pass

    def deleteTask(self):
        pass
