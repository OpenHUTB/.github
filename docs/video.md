## 视频制作

## 录屏

使用 [OBS Studio](https://github.com/obsproject/obs-studio) 等软件对模拟器或操作界面进行录频，生成视频文件 record.mp4。

## 视频下载和处理


合并视频和背景文件 [Descanso_pecy.ogg](./video/Descanso_pecy.ogg) <!-- 德斯坎索 -->
```bat
ffmpeg -i "record.mp4" -i "Descanso_pecy.ogg" -vcodec copy -acodec copy output.mp4
rem 解决 Twitter(X) 、抖音上传视频出现的不兼容问题
ffmpeg -i "record.mp4" -i "Descanso_pecy.ogg" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k output.mp4
```

关键改动说明

-map 0:v -map 1:a：明确指定只取第一个文件（record.mp4）的视频流，和第二个文件（.ogg）的音频流。这样可以避免 FFmpeg 默认行为可能带入不需要的流。

-c:v copy：视频流保持不变，直接复制。

-c:a aac：将 OGG 的音频重新编码为 AAC。这是 MP4 兼容性最好的音频格式。

-b:a 192k：指定音频码率为 192kbps。这是一个兼顾音质与文件大小的常用值，转码有损格式时，用稍高的码率有助于保留音质。


### 其他


**1.**[下载Youtube视频和音频](https://youtube.iiilab.com/) 。

（可选）将高清的webm文件转成mp4文件。
```bat
ffmpeg -i videoplayback.webm -crf 17 -c:v libx264 video.mp4
```

**2.**[下载Youtube视频的中英字幕](https://downsub.com/) （可选第一语言和第二语言）

如果没有翻译成中文，可以把srt文件拖到浏览器中，用chrome浏览器打开该srt文件。右键将网页翻译成中文。复制所有内容，替换原srt文件。

**3.**合并mp4（视频）和m4a（音频）文件

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
