## task detail page

- audio

1. 取样率
2. 比特率
3. 音量
4. 选择音轨列表

- video

1. 垂直反转 水平反转
2. 视频旋转
3. 比特率
4. 去交错
5. 长宽裁剪
6. 事件裁剪
7. 播放速度

- subtitle

1. 选择字幕列表

## 视频格式转换检查

使用二维数组记录每种转换情况

- 目前已知

1. mp4不支持内嵌字幕

## code quest

1. There should be a global FFmpegWrapper object handling all tasks, there should be a global task list inside
2. command should be a property of task
3. initiating ,starting and other operation towards task should be accessed by signal to FFmpegWrapper object
4. task detail page should be handled through left side track list, data should be fetched also by list item changing event
