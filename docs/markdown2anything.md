# Markdown 一键发到微信/知乎/小红书/Twitter

* 安装 Markdown2Anything 插件

* 打开任意 .md 文件，右键 → Markdown2Anything: 预览

* 工具栏按钮选择目标操作

## 微信公众号

* 点击上面工具栏中的“微信”->“上传到草稿箱”

* 从微信公众号的“设置与开发”->“账号设置”->“注册信息”中找到“AppID”

* 从微信公众号的“设置与开发”->“开发接口管理”->“微信开发者平台”->“我的业务与服务”->“公众号”->开发密钥->启用“AppSecret”

!!! 笔记

    * 为了便于手机端阅读，正文字体大小设置为 17，小标题字体大小设置为 18。
    
    * 风格选“微信经典”。

    * 图片前不要用空行


需要检查的内容包括：

* 图片前后没有多余的空行
* 图注是否正常显示或重复显示
* 公式如果格式混乱，改用截图
* 超过 5M 的动图一般会上传失败，使用 ScreenToGif “编辑-> 减少帧数”、“图像 -> 调整大小” 来压缩
* Python 代码的 class、def、return 等关键字后面缺少空格、代码是否对齐正确

选中除了第一行标题外的所有内容，复制到微信公众号的草稿的正文部分。

## [知乎](https://www.zhihu.com/people/OpenHUTB)

风格选“知乎精选”。


## [小红书](https://creator.xiaohongshu.com/new/home)

“写长文”->“导入链接”

风格选“小红书”风格。


## [Twitter](https://x.com/OpenHUTB)


## 自定义样式

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







## 参考

* [Markdown2Anything](https://marketplace.visualstudio.com/items?itemName=marsggbo.markdown2anything)