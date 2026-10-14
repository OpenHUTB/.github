# Markdown 一键发到微信/知乎/小红书/Twitter

将个人信息和微信号 <a href="mailto:recipient@://example.com">发送到邮箱 open@hutb.edu.cn </a> ，邮件主题：`申请运营者权限`。邮件模板：
```
github 用户名：XXX
邮箱：xxx@xx.com
申请原因：在 OpenHUTB 微信公众号发表“xxxx”

（选填）
姓名：
单位：
联系方式：
选题、草稿等
```

## VScode 操作流程

* 安装 Markdown2Anything 插件

* 打开任意 .md 文件，右键 → Markdown2Anything: 预览

* 工具栏按钮选择目标操作，比如“微信经典”、“知乎精选”、“小红书风格”等。

## 微信公众号

<!-- 
* 点击上面工具栏中的“微信”->“上传到草稿箱”

* 从微信公众号的“设置与开发”->“账号设置”->“注册信息”中找到“AppID”

* 从微信公众号的“设置与开发”->“开发接口管理”->“微信开发者平台”->“我的业务与服务”->“公众号”->开发密钥->启用“AppSecret”
-->

!!! 笔记

    * 为了便于手机端阅读，正文字体大小设置为 17，小标题字体大小设置为 18。
    
    * 风格选“微信经典”。

    * 图片前不要用空行


需要检查的格式内容包括：

* 图片前后是否有多余的空行
* 图注是否正常显示或重复显示
* 如果公式格式混乱，改用截图
* 出现超过 5M 的 gif 动图一般会上传失败的现象，请使用 ScreenToGif “编辑-> 减少帧数”、“图像 -> 调整大小” 来压缩
* Python 代码的 class、def、return 等关键字后面是否出现：缺少空格、代码未正确对齐的情况

需要检查的内容：

* 文章需要包括一定图像和动图，不能全部是文字；
* 必要的公式、核心代码、原理的说明；
* 选填内容：在文章最后填写编辑和审核（如有）
* 必填发表选项：作者（OpenHUTB 或 github 用户名或真实姓名）、封面（最具代表性和吸引力）、摘要、原创声明（默认）、原文链接（一般为参考的文档在线地址）
* 选填发表选项：合集
* 文字、图片等内容不能有任何 AI 的风格和痕迹

确认检查完成后，选中除了第一行标题外的所有内容，复制到微信公众号的草稿的正文部分。

发表过程：

* 定时发表：设置为离编辑完成最近的有群发通知的某一天发表，时间段选择 7:50-8:50、11:50-12:50、18:00-19:00、21:00-22:00 中的随机时刻。
* 将预览链接等效果 <a href="mailto:recipient@://example.com">发送到邮箱 open@hutb.edu.cn </a> 进行**审核发表**，不直接发表，否则解除运营者权限。


### 自定义样式

在预览页面点击“更多 -> 设置 -> 打开自定义样式面板”，拖到最下面的“CSS 编辑器”，输入以下内容（这里以调整标题的字体大小为例）：

```css
.article-wrapper h2 {
    font-size: 19px;
}
.article-wrapper h3 {
    font-size: 18px;
}
.article-wrapper h4 {
    font-size: 17px;
}
```

注意：正文默认字体大小 16。
```css
.article-wrapper p {
    font-size: 18px;
}
```

点击“应用”，即可在预览窗口看到改变后的字体大小。


## [知乎](https://www.zhihu.com/people/OpenHUTB)

风格选“知乎精选”。


## [小红书](https://creator.xiaohongshu.com/new/home)

“写长文”->“导入链接”

风格选“小红书”风格。


## [Twitter](https://x.com/OpenHUTB)




## 参考

* [Markdown2Anything](https://marketplace.visualstudio.com/items?itemName=marsggbo.markdown2anything)
