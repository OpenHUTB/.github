# 撰写科学论文的技巧和窍门

## 目录

  * [撰写科学论文的技巧和窍门](#tips-and-tricks-for-writing-scientific-papers)
    * [目录](#table-of-contents)
    * [这是什么？](#what-is-this)
  * [排版你的论文](#typesetting-your-paper)
    * [每行一个句子](#one-sentence-per-line)
    * [大写](#capitalization)
    * [保持参考文献完整](#keep-references-whole)
    * [表格](#tables)
    * [数字格式](#number-formatting)
  * [数学符号](#mathematical-notation)
    * [符号](#notation)
      * [定义自定义命令](#define-custom-commands)
      * [对列等元素使用正确的符号](#use-the-correct-notation-for-columns-et-elements)
    * [环境](#environments)
  * [参考书目](#bibliography)
    * [反向引用](#back-references)
  * [创建图形](#creating-figures)
    * [每个数据驱动图形一个脚本](#one-script-per-data-driven-figure)
    * [Python 帮助脚本](#python-helper-script)
    * [图形格式](#figures-format)
    * [将图形的部分栅格化](#rasterize-parts-of-the-figure)
  * [有用的资源](#useful-resources)

# 排版你的论文

排版是通过排列字体（例如字母和符号）来编写文本的过程。这主要关乎美观，但精美的字体设计能让文档更易于阅读，更赏心悦目，帮助读者更好地理解信息。

我们列出了一些排版技巧和工具，以帮助您撰写文档。其中一些技巧仅适用于 LaTeX，但其他技巧则适用于任何语言。

## 每行一个句子

编写 LaTeX 文档时，请在源文件中每行放一个句子。例如：
```
This is my first sentence.
This is the second one.
```
而不是：
```
This is my first sentence. This is the second one.
```

这样做的主要原因是为了源代码控制和协作：查看提交的更改时，如果每个句子都单独放在一行，就能更容易地识别哪些句子被更改了。这样，你的同志就能更容易地看到更改。

另一个好处是，当我们的 LaTeX 编译器仅给出行号时，您将能够更好地识别错误。

## 大写

下面我们将提到两种大写类型：

* 句子格式：好书的标题
* 标题格式：好书的标题

所有章节、小节等标题都应使用标题格式。为了帮助您正确使用大写字母，有一个方便的网站： [capitalizemytitle.com](https://capitalizemytitle.com)。

## 保持参考文献完整

有时，对象（例如图形、表格、图表或算法）的名称及其参考编号会分成两行。例如，对象名称可能在一行，而参考编号则出现在下一行。

为了确保 LaTeX 将对象名称及其引用保持在同一行，您可以在对象和引用之间使用`~`字符。通过`~`这种方式使用波浪号，您可以避免不雅的换行，并在 LaTeX 文档中保持对象名称和引用编号的格式一致。

```latex
Figure~\ref{fig:example} displays that the project ...
```

为了确保不会忘记使用波浪号，您可以通过创建自定义命令来简化自动化流程。以下是示例：


```latex
\newcommand{\refalg}[1]{Algorithm~\ref{#1}}
\newcommand{\refapp}[1]{Appendix~\ref{#1}}
\newcommand{\refchap}[1]{Chapter~\ref{#1}}
\newcommand{\refeq}[1]{Equation~\ref{#1}}
\newcommand{\reffig}[1]{Figure~\ref{#1}}
\newcommand{\refsec}[1]{Section~\ref{#1}}
\newcommand{\reftab}[1]{Table~\ref{#1}}
```

一旦定义了这些命令，就无需再写：

```latex
Figure~\ref{fig:example}
```

只需输入：

```latex
\reffig{fig:example}
```

## 表格

[(完整示例)](https://github.com/Wookai/paper-tips-and-tricks/tree/master/examples/booktabs)

[booktabs](https://www.ctan.org/pkg/booktabs) 可以帮助您制作干净、美观的表格。

```latex
\usepackage{booktabs}
% --
\begin{table}
	\centering
	\begin{tabular}{lcc}
		\toprule
		& \multicolumn{2}{c}{Data} \\ \cmidrule(lr){2-3}
		Name & Column 1 & Another column \\
		\midrule
		Some data & 10 & 95 \\
		Other data & 30 & 49 \\
		\addlinespace
		Different stuff & 99 & 12 \\
		\bottomrule
	\end{tabular}
	\caption{My caption.}
	\label{tab-label}
\end{table}
```

![Booktabs example](https://github.com/Wookai/paper-tips-and-tricks/raw/master/examples/booktabs/booktabs.png)

一般来说，避免在表格中使用垂直线。如果要对列进行分组，请在标题中使用`\cmidrule` 进行分组。您也可以使用 `\addlinespace` 用空格代替水平线。

列标题应使用句子格式大写（请参阅 http://www.chicagomanualofstyle.org/15/ch13/ch13_sec019.html ）。

您可以在这里找到更多关于表格格式的建议： http://www.inf.ethz.ch/personal/markusp/teaching/guides/guide-tables.pdf 。
这里有一个很棒的 GIF，演示了其中一些规则：

![Better table formatting](http://darkhorseanalytics.com/blog/wp-content/uploads/2014/03/ClearOffTheTableMd.gif)

## 数字格式

[(完整示例)](https://github.com/Wookai/paper-tips-and-tricks/tree/master/examples/siunitx)

使用 [siunitx](https://ctan.org/pkg/siunitx) 包格式化所有数字、货币、单位等：
```latex
\usepackage{siunitx}
% ---
This thing costs \SI{123456}{\$}.
There are \num{987654} people in this room, \SI{38}{\percent} of which are male.
```

![Siunitx formatting](https://github.com/Wookai/paper-tips-and-tricks/raw/master/examples/siunitx/siunitx-formatting.png)

您还可以使用它来对数字进行舍入：
```latex
\usepackage{siunitx}
% ---
\sisetup{
	round-mode = places,
	round-precision = 3
}%
You can also round numbers, for example \num{1.23456}.
```
![Siunitx formatting](https://github.com/Wookai/paper-tips-and-tricks/raw/master/examples/siunitx/siunitx-rounding.png)

最后，它可以帮助您更好地对齐表格中的数字：
```latex
\usepackage{booktabs}
\usepackage{siunitx}
%---
\begin{table}
	\centering
	\begin{tabular}{lS}
		\toprule
		Name & {Value} \\ % headers of S columns have to be in {}
		\midrule
		Test & 2.3456 \\
		Blah & 34.2345 \\
		Foo & -6.7835 \\
		Bar & 5642.5 \\
		\bottomrule
	\end{tabular}
	\caption{Numbers alignment with \texttt{siunitx}.}
\end{table}
```
![Siunitx formatting](https://github.com/Wookai/paper-tips-and-tricks/raw/master/examples/siunitx/siunitx-table.png)

# 数学符号

[(完整示例)](https://github.com/Wookai/paper-tips-and-tricks/tree/master/examples/notation)

在写方程式时，以连贯一致的方式书写变量、向量、矩阵等会很有帮助。它可以帮助读者识别你在说什么，并记住每个符号的语义。

## 符号

我们提出以下数学书写规则：

 * 变量用小写斜体表示： *x* (`$x$`)
 * 向量的小写斜体粗体： **_x_** (`$\mathbold{x}$`)
 * 矩阵的大写斜体粗体： **_X_** (`$\mathbold{X}$`)
 * 大写斜体表示随机变量： *X* (`$X$`)

该`\mathbold`命令来自[`fixmath`](https://www.ctan.org/pkg/fixmath)包，类似于`\boldmath`或`\bm`，不同之处在于所有符号都是斜体，甚至希腊字母也是如此（其他包不会将希腊字母斜体化）。

向变量添加索引或指数时，请确保将它们添加到变量的样式之外，即写为`$\mathbold{x}_i$`而不是`$\mathbold{x_i}$`。

### 定义自定义命令

因为我们经常引用变量，所以建议定义以下两个命令：

```latex
\renewcommand{\vec}[1]{\mathbold{#1}}
\newcommand{\mat}[1]{\mathbold{#1}}
```

然后，您就可以在文档中使用`$\vec{x}$`和 `$\mat{X}$` 了。如果您决定更改矩阵的格式，只需更改`\mat`命令即可，它将更新整个文档。

我们还建议为最常用的变量定义命令。例如，如果您经常使用`\vec{x}`和`\mat{X}`，可以考虑定义以下命令：

```latex
\newcommand{\vx}{\vec{x}}
\newcommand{\vX}{\mat{X}}
```

然后您可以写出更紧凑的方程： `$\vx^T \vy = \vZ$`。

### 对列和元素使用正确的符号

请注意，应始终根据变量的类型来设置其样式。例如，向量的第 $i$ 个元素`\vx`是`x_i`，而非`\vx_i`（它是一个数字）。类似地，如果有一个矩阵`\vX`，则可以将其第 *i* 列称为`\vx_i`（它是一个向量，因此以粗体显示），如果其元素`x_{ij}`，而非 `\vX_i`且`\vX_{ij}`，则可以将其第 *i* 列称为`\vx_i`。

## 环境

用于`\(...\)`编写内联方程式。您也可以使用`$...$`，但它是一个 TeX 命令，并且会给出更隐晦的错误信息。

要使公式居中并排，请勿使用（这是LaTeX 的致命错误`$$...$$`之一）。虽然可以使用，但间距不正确。请使用`\begin{equation*}`或`\begin{align*}`。


# 参考书目

## 反向引用

[(完整示例)](https://github.com/Wookai/paper-tips-and-tricks/tree/master/examples/backref)

对于较长的文档，例如学士、硕士或博士论文，在参考书目中添加参考文献以显示参考文献的引用位置会很有用。为此，只需在`hyperref`包中添加`backref=page`选项：


```latex
\usepackage[backref=page]{hyperref}
```

您可以使用以下命令自定义反向引用的显示方式：

```latex
\renewcommand*{\backref}[1]{}
\renewcommand*{\backrefalt}[4]{{\footnotesize [%
    \ifcase #1 Not cited.%
	\or Cited on page~#2%
	\else Cited on pages #2%
	\fi%
]}}
```

![Backref custom appearance](https://github.com/Wookai/paper-tips-and-tricks/raw/master/examples/backref/backref.png)

# 创建图形

图表是任何论文的重要组成部分，因为它们可以向读者传达你的研究结果。你应该思考每幅图上的信息究竟能传达给读者什么，并确保信息量刚好足以支撑你的信息，不要过多。例如，如果你想展示二维点的模式（有两个分离良好的簇），就没有必要在坐标轴上标注刻度和数值（比例尺其实并不重要）？图表不应该过于复杂。用几幅图来传达一两条信息（方法A优于方法B，但收敛速度较慢）比用一张又大又乱的图表要好。

## 每个数据驱动的图形对应一个脚本

有些图形是手工制作的，例如用于解释系统或提供全局视图；而另一些图形则是数据驱动的，即用于说明一些数据。这些数据驱动的图形应尽可能脚本化：理想情况下，如果数据发生变化，只需运行一次脚本即可更新图形，而无需任何其他干预（设置视图、缩放、保存/裁剪图形等）。同样，如果生成图形所需的数据需要几秒钟以上的时间，则应该使用第一个脚本来计算和保存数据，并使用第二个脚本来绘制数据。这样，您将在绘图时节省大量时间：您不必在对图形进行每次微小更改后等待才能看到其效果。

我们还建议将用于生成图形的命令保存在 LaTeX 文件中，例如作为图形上方的注释，特别是当脚本需要参数时。

```latex
\documentclass{article}

\usepackage{graphicx}

\begin{document}

% python figure_example.py --save ../../examples/figure/figure.eps
\begin{figure}
	\centering
	\includegraphics{figure.eps}
	\caption{Example of a sigmoid function}
\end{figure}

\end{document}
```

## Python 帮助脚本

如果可能，所有图形的标签、坐标轴等都应使用相同的字体。尤其要注意，不要让一个图形的标签/刻度较大，而另一个图形的标签/刻度较小。一个解决方案是在生成图形的脚本中定义图形的大小，而不是在文档中重新缩放（例如，不要在 LaTeX 文档中更改图形的宽度设置`\textwidth`）。

为了获得一致的图形，我们建议使用类似于我们的辅助脚本[`plot_utils.py`](https://github.com/Wookai/paper-tips-and-tricks/blob/master/src/python/plot_utils.py)。使用此脚本，您只需调用`figure_setup()`函数定义所有尺寸，然后创建所需尺寸的图形并保存即可。

```python
import argparse
import matplotlib.pyplot as plt
import numpy as np
import plot_utils as pu


def main(args):
    x = np.linspace(-6, 6, 200)
    y = 1/(1 + np.exp(-x))

    pu.figure_setup()

    fig_size = pu.get_fig_size(10, 5)
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(111)

    ax.plot(x, y, c='b', lw=pu.plot_lw())

    ax.set_xlabel('$x$')
    ax.set_ylabel('$\\sigma(x)$')

    ax.set_axisbelow(True)

    plt.grid()
    plt.tight_layout()

    if args.save:
        pu.save_fig(fig, args.save)
    else:
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--save')

    args = parser.parse_args()
    main(args)
```

## 图形格式

我们建议将所有图表保存为`EPS`格式。这样，您可以同时使用`latex`和`pdflatex`来生成文档，并欣赏精美的矢量图形和文本。

自 2015 年 9 月起，在 Mac OS X 上以及使用最新版本的 Python、Matplotlib 和 TeX Live 时，打印直接用 Matplotlib 保存为 `PDF` 格式的图表时会有一些质量损失。打印在纸上时，这个问题会更加明显；您可以亲自尝试一下。这也是为什么最好将 Matplotlib 生成的图片保存为 `EPS` 格式的原因之一。如果您确实只想保留图表的 PDF 版本，请使用 `epspdf` 命令行工具——生成的 PDF 会比直接用 Matplotlib 生成的 PDF 更好。

为了完整起见，请注意 Matplotlib 的另一个后端 [PGF](http://matplotlib.org/users/pgf.html) ，其结果略胜一筹。然而，截至 2015 年 9 月，生成的 PDF 文件大小是使用默认后端和 `epspdf` 生成的 PDF 文件的两倍。

Matplotlib 即使使用 [紧凑的布局功能](http://matplotlib.org/users/tight_layout_guide.html) ，有时也会在页边距中添加过多的空白。一个漂亮的命令行工具 `pdfcrop`，可以将 PDF 裁剪到最紧密的边界框。

## 将图形的部分栅格化

如果绘图中包含大量数据点，生成的 EPS 文件可能会非常大。您可以将图形保存为 PNG 文件，但这会导致文本模糊。解决方案是将图形的部分内容栅格化，即告诉 `matplotlib` 数据点必须在 EPS 文件中渲染为位图，其余部分则渲染为矢量格式。

您可以将 `rasterized=True` 关键字传递给 `matplotlib` 中的大多数绘图函数。您还可以使用 `zorder` 来设置不同的图层，并使用轴的 `set_rasterization_zorder()` 方法告诉 `matplotlib` 对给定 `zorder` 以下的所有图层进行栅格化。有关栅格化的示例，请参阅 [figure_rasterized_example.py](https://github.com/Wookai/paper-tips-and-tricks/blob/master/src/python/figure_rasterized_example.py) 和 http://matplotlib.org/examples/misc/rasterization_demo.html。

# 其他检查

## 内容
* 相关工作不是对现有论文的罗列，而是做评述，最后还需要引出自己的工作

## 形式
* 所有图片尽量用矢量图，生成PDF后保证能够用鼠标选中里面的文字，放大后不会失真
* 图中的字体要注意，需要按照模板要求
* 如果文章只出现一次，又不是非常通用的缩写，可以不用缩写。并且只在第一次出现的时候声明缩写
* 所有文中的符号都是公式符号，而不是英文

# 有用的资源

* 自动将标题大写: https://capitalizemytitle.com
* 芝加哥格式手册: http://www.chicagomanualofstyle.org
* 命令行检查模棱两可的词语、被动语态等: https://github.com/devd/Academic-Writing-Check
* LaTeX 2e 使用基本指南: http://ctan.math.utah.edu/ctan/tex-archive/info/l2tabu/english/l2tabuen.pdf
* [撰写科学论文的技巧和窍门](https://github.com/Wookai/paper-tips-and-tricks/tree/master)