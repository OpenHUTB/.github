# 寻找社区技术文档所对应的作者和源码

该页面是为了解决当对某个文档页面有疑问想找到对应作者和源代码的问题。

## 寻找页面的作者

以[公众号文章](https://mp.weixin.qq.com/s/HS6_iq1081vJjsdgrta8wQ)为例，点击末尾“阅读全文”跳转到[文档页面](https://openhutb.github.io/ros2/water/rov_trajectory_tracking)。

![](../img/adv/full_article.png)

然后，点击页面右上角的“编辑页面”，

![](../img/adv/edit_page.png)

将跳转到 GitHub 仓库的代码编辑页面。先确认页面显示的仓库名称，再点击文件路径中的文件夹：

![](../img/adv/edit_tool.png)

点击上一步绿色框中的文件名（即页面所对应的 .md 文件）。

![](../img/adv/file_edited.png)

点击页面右上角的 `History`：

![](../img/adv/click_history.png)

历史记录会显示编辑过该页面的用户名和对应提交；同一页面可能由多人维护。

## 寻找页面的源代码

以同一篇文章为例，从“编辑页面”记下文档所在仓库和目录，例如 `docs/water/rov_trajectory_tracking.md`。文档目录不能直接说明程序代码所在目录，不同项目的组织方式可能不同。

返回对应仓库首页后，可以先查看 `src` 目录，再结合文档中的模块名称、仓库链接和页面历史记录定位相关代码。

![](../img/adv/click_index.png)

该示例对应模块位于 `src/water/rov_mujoco`：

![](../img/adv/src_directory.png)

![](../img/adv/src_location.png)

如果没有找到同名目录，可查看页面链接指向的项目和提交历史，确认文档与程序代码之间的关系。
