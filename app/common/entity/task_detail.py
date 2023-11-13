from dataclasses import dataclass

@dataclass
class TaskDetail:
    """ 任务详情实体类 """

    extraCommand: str
    # video
    videoBitRate: int
    rotation: int
    speed: int
    # audio
    audioSampleRate: int
    audioBitRate: int
    audioVolumn: int

    # video
    def setDeinterlacing(self, t):
        # 0 = false; 2 = true
        print(t)

    def setVerticalFlip(self, t):
        # 0 = false; 2 = true
        print(t)

    def setHorizontalFlip(self, t):
        # 0 = false; 2 = true
        print(t)

    def setRotation(self, t):
        print(t)
        self.rotation = t

    def setVideoBitRate(self, t):
        print(t)
        self.rotation = t

    def setSpeed(self, t):
        print(t)
        self.speed = t

    # audio
    def setAudioSampleRate(self, val):
        self.audioSampleRate = val

    def setAudioBitRate(self, val):
        self.audioBitRate = val

    def setAudioVolumn(self, val):
        self.audioVolumn = val
