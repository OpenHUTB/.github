## 视频制作

## 录屏

使用 [OBS Studio](https://github.com/obsproject/obs-studio) 等软件对模拟器或操作界面进行录频，生成视频文件 record.mp4。

## 视频下载和处理


合并视频和背景文件 [Descanso_pecy.ogg](./video/Descanso_pecy.ogg) <!-- 德斯坎索 -->
```
ffmpeg -i "record.mp4" -i "Descanso_pecy.ogg" -vcodec copy -acodec copy record.mp4
```

### 其他


1. [下载Youtube视频和音频](https://youtube.iiilab.com/) 。

（可选）将高清的webm文件转成mp4文件。
```bat
ffmpeg -i videoplayback.webm -crf 17 -c:v libx264 video.mp4
```

2. [下载Youtube视频的中英字幕](https://downsub.com/) （可选第一语言和第二语言）

如果没有翻译成中文，可以把srt文件拖到浏览器中，用chrome浏览器打开该srt文件。右键将网页翻译成中文。复制所有内容，替换原srt文件。

3. 合并mp4（视频）和m4a（音频）文件

```bat
ffmpeg -i "videoplayback.mp4" -i "videoplayback.m4a" -vcodec copy -acodec copy output.mp4
rem （可选）合并mp4（视频）和 srt（字幕）文件
ffmpeg -i "output.mp4" -vf subtitles="en.srt" output_srt.mp4
```




## 技巧

将原始视频中的音频提取为单独的文件：
```shell
ffmpeg -i input.mp4 -vn -c:a copy output.aac
```

将 aac **音频截取**为 149 秒的片段，可以使用以下命令：
```shell
ffmpeg -i output.aac -ss 00:00:00 -t 149 -c copy music.aac
```

**视频截取**：input.mp4 从 0 秒开始到 63秒保存下来：
```shell
ffmpeg -ss 00:00:00 -i input.mp4 -t 63 -c copy output.mp4
```
