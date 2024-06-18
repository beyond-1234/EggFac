import os
import signal
import uuid

from app.common.converter.ffmpeg_probe import FFmpegProbe
from app.common.entity.task import Task
from app.common.entity.task_detail import TaskDetail
from app.common.entity.task_status import TaskStatus
from app.common.signal_bus import signalBus
from .ffmpeg_executor import FFmpegExecutor
from app.common.config import cfg


class FFmpegWrapper:
    def __init__(self):
        # self.commandList = ["ffmpeg"]
        self.taskList = list()

        signalBus.startTaskSignal.connect(self.startTask)
        signalBus.deleteTaskSignal.connect(self.deleteTask)
        signalBus.updateTaskPidSignal.connect(self.updateTaskPid)
        signalBus.updateTaskTargetFormatSignal.connect(self.updateTaskTargetFormat)
        signalBus.updateTaskCommandSignal.connect(self.updateTaskCommand)
        signalBus.updateTaskIsKeepOriginalSignal.connect(
            self.updateIsKeepOriginalSetting
        )

    # def _addInputFile(self, filePath):
    #     self.commandList.append("-i")
    #     self.commandList.append(filePath)
    #
    # def _addOutputFile(self, filePath):
    #     self.commandList.append(filePath)
    #
    # def _addCopyOption(self, isVideoCopy, isAudioCopy):
    #     if isVideoCopy:
    #         self.commandList.append("-c:v")
    #         self.commandList.append("copy")
    #     if isAudioCopy:
    #         self.commandList.append("-c:a")
    #         self.commandList.append("copy")

    def initTask(self, path: str):
        if not os.path.exists(path):
            print("file not exists")
            return None

        if not os.path.isfile(path):
            print("file is dir")
            return None

        fileTuple = os.path.splitext(path)
        name = os.path.basename(fileTuple[0])
        probe = FFmpegProbe.getProbe(path)
        t = Task(
            code=uuid.uuid1().__str__(),
            path=path,
            name=name,
            targetFormat="",
            progress=0,
            status=TaskStatus.CREATED,
            isKeepingOriginalSetting=True,
            probe=probe,
            taskDetail=TaskDetail(path),
            pid=-1,
        )
        self.taskList.append(t)
        return t

    def startTask(self, taskCode: str):
        t = self.__getTaskByCode(taskCode)
        if t is not None:
            thread = FFmpegExecutor(t.getCommand(), t.code)
            thread.start()

    def stopTask(self, taskCode):
        for item in self.taskList:
            if item.code == taskCode and item.pid != -1:
                try:
                    os.kill(item.pid, signal.SIGKILL)
                    print(f"process {item.pid} has been killed.")
                except ProcessLookupError:
                    print(f"process {item.pid} not exists.")
                except PermissionError:
                    print(f"permission denied to kill {item.pid}.")
                except Exception as e:
                    print("killing process failed :", str(e))
                break

    def deleteTask(self, taskCode):
        for item in self.taskList:
            if item.code == taskCode and item.pid != -1:
                try:
                    os.kill(item.pid, signal.SIGKILL)
                    print(f"process {item.pid} has been killed.")
                    self.taskList.remove(item)
                except ProcessLookupError:
                    print(f"process {item.pid} not exists.")
                except PermissionError:
                    print(f"permission denied to kill {item.pid}.")
                except Exception as e:
                    print("killing process failed :", str(e))
                break

    def deleteAllTasks(self):
        for item in self.taskList:
            if item.pid != -1:
                try:
                    os.kill(item.pid, signal.SIGKILL)
                    print(f"process {item.pid} has been killed.")
                    self.taskList.remove(item)
                except ProcessLookupError:
                    print(f"process {item.pid} not exists.")
                except PermissionError:
                    print(f"permission denied to kill {item.pid}.")
                except Exception as e:
                    print("killing process failed :", str(e))
                break

    def updateTaskPid(self, taskCode, pid):
        t = self.__getTaskByCode(taskCode)
        if t is not None:
            t.pid = pid

    def updateTaskTargetFormat(self, taskCode, format):
        t = self.__getTaskByCode(taskCode)
        if t is not None:
            t.targetFormat = format

    def updateIsKeepOriginalSetting(self, taskCode, res):
        t = self.__getTaskByCode(taskCode)
        if t is not None:
            t.isKeepingOriginalSetting = res
            if res:
                outputPath = os.path.join(
                    cfg.get(cfg.outputFolder), t.name + "." + t.targetFormat
                )
                # An empty stream specifier matches all streams. For example, -codec copy or -codec: copy would copy all the streams without reencoding.
                t.taskDetail.commandList = [
                    "ffmpeg",
                    "-y",
                    "-i",
                    f'"{t.path}"',
                    "-map 0:v",
                    "-c:v copy",
                    "-map 0:a",
                    "-c:a copy",
                    # "-c:s copy",
                    f'"{outputPath}"',
                ]
            else:
                t.taskDetail.commandList = []

    def updateTaskCommand(self, taskCode, extraCommand):
        t = self.__getTaskByCode(taskCode)
        if t is None:
            return

        t.taskDetail.commandList = ["ffmpeg", "-i", f'"{t.path}"']
        outputPath = os.path.join(
            cfg.get(cfg.outputFolder), t.name + "." + t.targetFormat
        )

        t.taskDetail.commandList.extend(list(extraCommand.values()))

        t.taskDetail.commandList.append(f'"{outputPath}"')

    def __getTaskByCode(self, taskCode) -> Task | None:
        filtered_list = list(filter(lambda t: t.code == taskCode, self.taskList))
        if len(filtered_list) == 0:
            return None

        return filtered_list[0]


ffmpegWrapper = FFmpegWrapper()
