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
    isKeepingOriginalSetting: bool
    probe: FFmpegProbe
    taskDetail: TaskDetail
    pid: int

    def getCommand(self):
        return " ".join(self.taskDetail.commandList)
