from dataclasses import dataclass

from .task_detail import TaskDetail
from .task_status import TaskStatus
from ..converter.ffmpeg_probe import FFmpegProbe


@dataclass
class Task:
    """转换任务实体类"""

    code: str
    path: str
    name: str
    targetFormat: str
    progress: int
    status: TaskStatus
    isKeepingOriginalSeting: bool
    probe: FFmpegProbe
    taskDetail: TaskDetail
    pid: int

    def getCommand(self):
        pass

    # @staticmethod
    # def initTaskOnlySource(path):
    #     return Task.initTask(path, None)
    #
    # @staticmethod
    # def initTask(path, targetFormat):
    #     if not os.path.exists(path):
    #         print("file not exists")
    #         return None
    #
    #     if not os.path.isfile(path):
    #         print("file is dir")
    #         return None
    #
    #     fileTuple = os.path.splitext(path)
    #     name = os.path.basename(fileTuple[0])
    #     format = fileTuple[1]  # could be ''
    #     duration = 0.0
    #     tracks = []
    #
    #     # todo
    #     # task should only be used to display info
    #     # task detail should be merge into task and track
    #     # task detail widget should directly manipulate FFmpegWrapper
    #
    #     # probe = FFmpegWrapper.getInfo(path)
    #     try:
    #         probe = ffmpeg.probe(path)
    #         duration = float(probe["format"]["duration"])
    #         for p in probe["streams"]:
    #             tracks.append(Track(p["codec_type"], p["codec_name"], p))
    #     except ffmpeg.Error as e:
    #         print(e.stderr, file=sys.stderr)
    #         return None
    #
    #     videoBitRate = [t.probe["bit_rate"] for t in tracks if t.type == "video"]
    #     rotation = 0
    #     speed = 100
    #     audioBitRate = [t.probe["bit_rate"] for t in tracks if t.type == "audio"]
    #     audioBitRate = [t.probe["bit_rate"] for t in tracks if t.type == "audio"]
    #     audioBitRate = [t.probe["bit_rate"] for t in tracks if t.type == "audio"]
    #     audioSampleRate = [t.probe["sample_rate"] for t in tracks if t.type == "audio"]
    #     taskDetail = TaskDetail(
    #         extraCommand={},
    #         videoBitRate=0 if len(videoBitRate) == 0 else int(videoBitRate[0]),
    #         rotation=rotation,
    #         speed=speed,
    #         audioSampleRate=0 if len(audioSampleRate) == 0 else int(audioSampleRate[0]),
    #         audioBitRate=0 if len(audioBitRate) == 0 else int(audioBitRate[0]),
    #         audioVolumn=100,
    #     )
    #
    #     t = Task(
    #         uuid.uuid1().__str__(),
    #         path,
    #         name,
    #         format,
    #         targetFormat,
    #         duration,
    #         0,
    #         TaskStatus.CREATED,
    #         tracks,
    #         True,
    #         taskDetail,
    #         FFmpegWrapper(),
    #     )
    #
    #     signalBus.generateFFmpegCommandSignal.connect(onGeneratingFFmpegCommand)
    #
    #     return t
    #
    # def startTask(self):
    #     print("starting task threaded")
    #     self.status = TaskStatus.STARTED
    #     self.doStartTask()
    #
    # def doStartTask(self):
    #     outputFolder = cfg.get(cfg.outputFolder)
    #
    #     if not os.path.exists(outputFolder):
    #         os.makedirs(outputFolder)
    #
    #     print(self.targetFormat)
    #     output = os.path.join(outputFolder, self.name + "." + self.targetFormat)
    #     self.wrapper.startTask(self.code)
    #
    # def stopTask(self):
    #     pass
    #
    # def deleteTask(self):
    #     pass
