import os
import sys
import ffmpeg
import _thread
import tempfile
import socket
import uuid

from dataclasses import dataclass

from ..signal_bus import signalBus
from .track import Track
from .task_status import TaskStatus
from ..config import cfg

@dataclass
class Task:
    """ 转换任务实体类 """
    code: str
    path: str
    name: str
    format: str
    targetFormat: str
    duration: float
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
        duration = 0.0
        tracks = []

        try:
            probe = ffmpeg.probe(path)
            duration = float(probe["format"]["duration"])
            for p in probe["streams"]:
                tracks.append(Track(p["codec_type"], p["codec_name"], p))
        except ffmpeg.Error as e:
            print(e.stderr, file=sys.stderr)
            return None

        return Task(uuid.uuid1().__str__(), path, name, format, targetFormat, duration, 0, TaskStatus.CREATED, tracks)

    def startTask(self):
        print("starting task threaded")
        _thread.start_new_thread(self.doStartTask, ())

    def _do_watch_progress(self, sock, handler):
        connection, client_address = sock.accept()
        data = b''
        try:
            while True:
                more_data = connection.recv(16)
                if not more_data:
                    break
                data += more_data
                lines=  data.split(b'\n')
                for line in lines[:-1]:
                    line = line.decode()
                    parts = line.split('=')
                    key = parts[0] if len(parts) > 0 else None
                    value = parts[1] if len(parts) > 0 else None
                    handler(key, value)
                data = lines[-1]
        finally:
            connection.close()

    def handle_progress(self, key, value):
        if key == 'out_time_ms':
            time = round(float(value) / 1000000, 2)
            self.progress = int(time / self.duration * 100)
            signalBus.updateProgressSignal.emit(self.code, self.progress)
            # print("current progress {}  ==> percentage {:.0%}".format(time, time / self.duration))
        elif key == 'progress' and value == 'end':
            print("current task ended")
            self.progress = int(100)
            signalBus.updateProgressSignal.emit(self.code, 100)

    def _create_progress_socket(self):
        """ create unix socket and listen to ffmpeg progress events """
        tmpdir = tempfile.mkdtemp()
        socket_filename = os.path.join(tmpdir, 'sock')
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(socket_filename)
        sock.listen(1)
        _thread.start_new_thread(self._do_watch_progress, (sock, self.handle_progress))
        return socket_filename

    def doStartTask(self):
        outputFolder = cfg.get(cfg.outputFolder)

        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        output = os.path.join(outputFolder, self.name + "." + self.targetFormat)
        socket_filename = self._create_progress_socket()
        try:
            (
            ffmpeg.input(self.path)
                .output(output, vcodec='copy', acodec='copy')
                .global_args('-nostats', '-progress', 'unix://{}'.format(socket_filename))
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            print(e.stderr, file=sys.stderr)


    def stopTask(self):
        pass

    def deleteTask(self):
        pass
