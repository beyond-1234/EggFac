from dataclasses import dataclass
import subprocess

from .ffmpeg_executor import FFmpegExecutor


@dataclass
class FFmpegProbe:
    format: str
    duration: str
    bitrate: str
    videoStreams: list
    audioStreams: list
    subtitleStreams: list

    @staticmethod
    def getProbe(path: str):
        cmd = ["ffmpeg", "-i", path]
        proc = subprocess.Popen(
            cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True
        )
        output, _ = proc.communicate()
        info = {}
        vStream = []
        aStream = []
        for line in output.split("\n"):
            if "Input #0," in line:
                info["format"] = (
                    line.split(", from")[0].replace("Input #0,", "").strip()
                )
            if line.strip().startswith("Duration"):
                info["duration"] = line.split(",")[0].split(": ")[1].strip()
                info["bitrate"] = line.split(",")[2].split(": ")[1].strip()
            if "Stream #0:" in line and "Video" in line:
                paramList = line.split(",")
                v = VideoStream(
                    codec=paramList[0].split(":")[2].strip(),
                    resolution=paramList[1],
                    colorSpace=paramList[2],
                    bitrate="",
                    framerate="",
                )
                vStream.append(v)
            if "Stream #0:" in line and "Audio" in line:
                paramList = line.split(",")
                a = AudioStream(
                    codec=paramList[0].split(":")[2].strip(),
                    sampling=paramList[1],
                    bitrate=paramList[len(paramList) - 1],
                )
                aStream.append(a)
        return FFmpegProbe(
            format=info["format"],
            duration=info["duration"],
            bitrate=info["bitrate"],
            videoStreams=vStream,
            audioStreams=aStream,
            subtitleStreams=[],
        )


@dataclass
class VideoStream:
    codec: str
    resolution: str
    colorSpace: str
    bitrate: str
    framerate: str


@dataclass
class AudioStream:
    codec: str
    sampling: str
    bitrate: str
