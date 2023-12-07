
from app.common.converter.ffmpeg_probe import FFmpegProbe
from ..entity.task import Task
from .ffmpeg_executor import FFmpegExecutor

class FFmpegWrapper:

    def __init__(self, task: Task):
        self.commandList = ['ffmpeg'];
        self.task = task

    def _addInputFile(self, filePath):
        self.commandList.append("-i")
        self.commandList.append(filePath)

    def _addOutputFile(self, filePath):
        self.commandList.append(filePath)

    def _addCopyOption(self, isVideoCopy, isAudioCopy):
        if isVideoCopy:
            self.commandList.append("-c:v")
            self.commandList.append("copy")
        if isAudioCopy:
            self.commandList.append("-c:a")
            self.commandList.append("copy")

    @staticmethod
    def getInfo(path: str):
        return FFmpegProbe.getProbe(path)


    def startTask(self):
        command = ' '.join(self.commandList)
        thread = FFmpegExecutor(command, self.task)
        thread.start()
