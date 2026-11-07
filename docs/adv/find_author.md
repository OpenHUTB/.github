# 寻找社区技术文档所对应的作者和源码

该页面是为了解决当对某个文档页面有疑问想找到对应作者和源代码的问题。

## 寻找页面的作者

以[公众号文章](https://mp.weixin.qq.com/s/HS6_iq1081vJjsdgrta8wQ)为例，点击末尾“阅读全文”跳转到[文档页面](https://openhutb.github.io/ros2/water/rov_trajectory_tracking)。

![](../img/adv/full_article.png)

然后，点击页面右上角的“编辑页面”，

![](../img/adv/edit_page.png)

将跳转到 github 仓库的代码编辑页面，点击它所在的文件夹：

![](../img/adv/edit_tool.png)

点击上一步绿色框中的文件名（即页面所对应的 .md 文件）

![](../img/adv/file_edited.png)

点击页面右上角的`History`

![](../img/adv/click_history.png)

将显示编辑过该页面的所有用户名（可能有多个）

`History` 显示的是这个文件的提交记录，不一定等于最初作者。想确认某一段文字是谁改的，可在文件页面选择 `Blame`，找到对应行及提交；再打开提交详情，查看当时改了什么。引用作者信息时，应以该次提交记录为准。



## 寻找页面的源代码

以同一篇文章为例，从上面的“编辑页面”记下文档所在目录 docs/water/rov_trajectory_tracking.md，点击仓库名进入仓库首页

![](../img/adv/click_index.png)


部分项目会把相关代码放在 `src` 目录，但文档路径与源码路径不一定一一对应。先在仓库内搜索页面提到的类名、脚本名或函数名，再查看搜索结果及提交记录。

![](../img/adv/src_directory.png)

该模块位于 src/water/rov_mujoco

![](../img/adv/src_location.png)

最后一个目录可能有微小差别，具体请看上面提交历史（`History`）页面的详细信息。






