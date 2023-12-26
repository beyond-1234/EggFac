from dataclasses import dataclass
from math import log, floor


@dataclass
class TaskDetail:
    """任务详情实体类"""

    extraCommand: dict
    commandList: list
    # video
    videoBitRate: int
    rotation: int
    speed: int
    # audio
    audioSampleRate: int
    audioBitRate: int
    audioVolumn: int

    def __init__(self, path: str):
        self.extraCommand = {}
        self.extraCommand["input"] = "-i " + path
        self.extraCommand["output"] = path.split()

    # video
    def setDeinterlacing(self, t):
        # 0 = false; 2 = true
        if t == 2:
            self.extraCommand["setDeinterlacing"] = "-deinterlacing"
        else:
            self.extraCommand.pop("setDeinterlacing")
        print(t)

    def setVerticalFlip(self, t):
        # 0 = false; 2 = true
        self.__addVideoFilterGraph("vflip", t == 2)
        print(t)

    def setHorizontalFlip(self, t):
        # 0 = false; 2 = true
        self.__addVideoFilterGraph("hflip", t == 2)
        print(t)

    def setRotation(self, t):
        # todo only support 90 / 180 or negative rotation
        print(t)
        self.rotation = t

    def setVideoBitRate(self, t):
        print(t)
        self.videoBitRate = t
        self.extraCommand["setVideoBitRate"] = "-b:v " + self.__human_format(
            self.videoBitRate
        )

    def setSpeed(self, t: str):
        print(t)
        # self.speed = t
        self.__addVideoFilterGraph("setpts=%s*PTS" % t.replace("x", ""), t != "1.0x")

    # audio
    def setAudioSampleRate(self, index, val):
        self.audioSampleRate = val
        self.extraCommand["setAudioSampling"] = "-ar  " + val

    def setAudioBitRate(self, index, val):
        self.audioBitRate = val
        self.extraCommand["setAudioBitRate"] = "-b:a " + self.__human_format(val)

    def setAudioVolumn(self, index, val):
        self.audioVolumn = val
        self.__addAudioFilterGraph("volumn=" + val / 100, val == 100)

    def __addVideoFilterGraph(self, filterName: str, addOrDelete: bool):
        vfCommand = self.extraCommand.get("setVf")
        if vfCommand is None:
            self.extraCommand["setVf"] = "-vf %s" % filterName
            return

        vfCommand = vfCommand.replace("-vf", "")

        cList = vfCommand.split(",")

        if addOrDelete is True:
            cList.append(filterName)
        else:
            cList.remove(filterName)

        self.extraCommand["setVf"] = "-vf " + (",").join(cList)

    def __addAudioFilterGraph(self, filterName: str, addOrDelete: bool):
        vfCommand = self.extraCommand.get("setAf")
        if vfCommand is None:
            self.extraCommand["setAf"] = "-af %s" % filterName
            return

        vfCommand = vfCommand.replace("-af", "")

        cList = vfCommand.split(",")

        if addOrDelete is True:
            cList.append(filterName)
        else:
            cList.remove(filterName)

        self.extraCommand["setAf"] = "-af " + (",").join(cList)

    def __human_format(self, number):
        units = ["", "K", "M", "G", "T", "P"]
        k = 1000.0
        magnitude = int(floor(log(number, k)))
        return "%.0f%s" % (number / k**magnitude, units[magnitude])
