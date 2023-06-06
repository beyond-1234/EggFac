import os
import sys
import ffmpeg
import _thread

from dataclasses import dataclass
from .track import Track
from .task_status import TaskStatus
from ..config import cfg

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

        fileTuple = os.path.splitext(path)
        name = os.path.basename(fileTuple[0])
        format = fileTuple[1] # could be ''
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
        print("starting task threaded")
        _thread.start_new_thread(self.doStartTask, ())

    def doStartTask(self):
        outputFolder = cfg.get(cfg.outputFolder)

        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        output = os.path.join(outputFolder, self.name + "." + self.targetFormat)
        try:
            (
            ffmpeg.input(self.path)
                .output(output, vcodec='copy', acodec='copy')
                .overwrite_output()
                .run()
            )
        except ffmpeg.Error as e:
            pass


    def stopTask(self):
        pass

    def deleteTask(self):
        pass
