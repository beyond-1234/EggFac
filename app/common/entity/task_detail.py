from dataclasses import dataclass

@dataclass
class TaskDetail:
    """ 任务详情实体类 """
    extraCommand: str
    audioSampleRate: int
    audioBitRate: int
    audioVolumn: int

    def setAudioSampleRate(self, val):
        self.audioSampleRate = val

    def setAudioBitRate(self, val):
        self.audioBitRate = val

    def setAudioVolumn(self, val):
        self.audioVolumn = val
