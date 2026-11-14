# Python 绘图示例

本目录包含论文绘图辅助脚本 `plot_utils.py` 和两个示例：

- `figure_example.py`：绘制函数曲线。
- `figure_rasterized_example.py`：绘制栅格化散点图。

## 安装 Python 依赖

```shell
python -m pip install -r requirements.txt
```

## 运行示例

```shell
python figure_example.py
python figure_rasterized_example.py
```

`plot_utils.figure_setup()` 默认启用 LaTeX 文字渲染，因此系统还需安装 LaTeX。未安装 LaTeX 时，可以使用示例的 `--no-latex` 参数改用 Matplotlib 自带的 mathtext：

```shell
python figure_example.py --no-latex
python figure_rasterized_example.py --no-latex
```

## 保存图片

使用示例的 `--save` 参数保存图片时，除 Python 依赖外还需要对应的外部命令：

| 格式 | 外部命令 |
| --- | --- |
| EPS | `epstool` |
| PNG | ImageMagick 的 `convert` |
| PDF | `pdfcrop` |

Windows 自带的 `convert` 是磁盘格式转换工具，不是 ImageMagick。请确认 `convert` 实际指向 ImageMagick，避免图片未生成而命令看起来已经执行。
