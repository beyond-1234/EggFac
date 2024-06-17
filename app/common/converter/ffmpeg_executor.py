import subprocess
import threading
import re

from ..signal_bus import signalBus


class FFmpegExecutor(threading.Thread):
    def __init__(self, command, taskCode: str):
        threading.Thread.__init__(self)
        self.command = command
        self.taskCode = taskCode

        # pattern 1 is not been used
        self.progressPattern1 = "size=\\s*([0-9]+)kB\\s+time=\\s*([0-9]+\\.[0-9]+)\\s+bitrate=\\s*([0-9]+\\.[0-9]+)kbits/s"
        self.progressPattern2 = "size=\\s*([0-9]+)kB\\s+time=\\s*([0-9][0-9]):([0-9][0-9]):([0-9][0-9](\\.[0-9][0-9]?)?)\\s+"
        self.durationPattern = (
            "Duration:\\s+([0-9][0-9]):([0-9][0-9]):([0-9][0-9](\\.[0-9][0-9]?)?)"
        )

    def run(self):
        duration = 0
        progress = 0

        process = subprocess.Popen(
            self.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        signalBus.updateTaskPidSignal.emit(self.taskCode, process.pid)
        while True:
            output = process.stderr.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                o = output.strip()

                # if video speed has changed, duration will change also
                # need to take care of this
                if duration == 0:
                    durationMatch = re.search(self.durationPattern, o)
                    if durationMatch:
                        hour = int(durationMatch.group(1))
                        min = int(durationMatch.group(2))
                        sec = float(durationMatch.group(3))
                        duration = hour * 3600 + min * 60 + sec

                if duration == 0:
                    continue

                progressMatch1 = re.search(self.progressPattern1, o)
                progressMatch2 = re.search(self.progressPattern2, o)
                if progressMatch1:
                    hour = int(progressMatch1.group(2))
                    min = int(progressMatch1.group(3))
                    sec = float(progressMatch1.group(4))
                    progress = hour * 3600 + min * 60 + sec
                elif progressMatch2:
                    hour = int(progressMatch2.group(2))
                    min = int(progressMatch2.group(3))
                    sec = float(progressMatch2.group(4))
                    progress = hour * 3600 + min * 60 + sec

                signalBus.updateProgressSignal.emit(
                    self.taskCode, (int)(progress / duration * 100)
                )

        process.stdout.close()
        process.stderr.close()
