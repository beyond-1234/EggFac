from app.common.entity.task import Task


class FFmpegChecker:
    def __init__(self):
        self.nextChecker = MP4FFmpegChecker()

    def check(self, task: Task, targetFormat):
        return self.nextChecker.check(task, targetFormat)

class MP4FFmpegChecker:
    def __init__(self):
        self.nextChecker = MKVFFmpegChecker()

    def check(self, task: Task, targetFormat):
        if "mp4" != targetFormat:
            return self.nextChecker(task, targetFormat)

        return None


class MKVFFmpegChecker:
    def __init__(self):
        self.nextChecker = None

    def check(self, task: Task, targetFormat):
        pass

ffmpegChecker = FFmpegChecker()
