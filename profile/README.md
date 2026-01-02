

🙋‍♀️ 该社区提供一款能快速测试 [具身人](https://openhutb.github.io/doc/#_4) 、[无人车](https://openhutb.github.io/doc/#_5) 、[无人机](https://openhutb.github.io/air_doc/) 感知、规划、控制算法的影视级物理模拟器。

<p width="100%" display="flex" align="center">
<a href="https://openhutb.github.io/doc/tuto_G_pedestrian_navigation/#conclusion"><img src="https://github.com/OpenHUTB/doc/blob/master/docs/img/pedestrian/cycle.gif?raw=true" width="30%" margin-right="10%"/></a>  <a href="https://openhutb.github.io/doc/tuto_G_chrono/"><img src="https://github.com/OpenHUTB/doc/blob/master/docs/img/chrono/vechile_turnover.gif?raw=true" width="33%"/></a> <a href="https://openhutb.github.io/air_doc/"><img src="https://github.com/OpenHUTB/air_doc/blob/master/docs/images/dev/HUTB_simulation.gif?raw=true" width="33%"/></a>
</p>

🍿 实用资源 - 从 [社区文档](https://openhutb.github.io/doc/) 中可以找到您所需要的所有详细信息，项目之间的关系如下图所示

```mermaid
graph LR
    A[人的模型 <a href='https://github.com/OpenHUTB/opensim-core'>OpenSim</a>] --> B[多体物理 <a href='https://github.com/OpenHUTB/chrono'>chrono</a>]
    B --> C[<b>人车模拟器 <a href='https://github.com/OpenHUTB/hutb'>hutb</a> </b>]
    A --> F[<a href='https://github.com/MyoHub/myoconverter'>格式转换</a> <a href='https://github.com/OpenHUTB/mujoco_plugin'>mujoco_plugin</a> ]
    F --> C
    C --> D[文档 <a href='https://github.com/OpenHUTB/doc'>doc</a>]
    D --> H[无人机文档 <a href='https://github.com/OpenHUTB/air_doc'>air_doc</a>]
    D --> I[神经原理 <a href='https://github.com/OpenHUTB/neuro'>neuro</a>]
    I --> J[规划 <a href='https://github.com/OpenHUTB/PFC'>PFC</a>]
    I --> K[控制原理 <a href='https://github.com/OpenHUTB/move'>move</a>]
    K --> A
    L[模拟引擎 <a href='https://github.com/OpenHUTB/engine'>engine</a>] --> C
    L --> M[引擎文档 <a href='https://github.com/OpenHUTB/engine_doc'>engine_doc</a>]
    M --> S[C++ 文档 <a href='https://github.com/OpenHUTB/cpp'>cpp</a>]
    D --> M
    L --> N[无人机模拟器 <a href='https://github.com/OpenHUTB/air'>air</a>]
    N --> C
    N --> H
    D --> R[<a href='https://github.com/OpenHUTB/.github/blob/master/README.md#%E5%BA%94%E7%94%A8%E5%88%97%E8%A1%A8'>应用列表</a>]
    D --> Q[<a href='https://github.com/OpenHUTB/.github/blob/master/README.md#%E5%B7%A5%E5%85%B7%E5%88%97%E8%A1%A8'>工具列表</a>]


    style I fill:#e1f5fe
    style C fill:#ccffcc
    style D fill:#fff3e0
    style Q fill:#f3e5f5
    style R fill:#F5DEB3
```

🌈 贡献指南 - 欢迎在各个项目的 [Issues 页面](https://github.com/OpenHUTB/hutb/issues) 进行交流，参与社区请参考 [贡献指南](https://github.com/OpenHUTB/.github/blob/master/CONTRIBUTING.md) 







<!--

**Here are some ideas to get you started:**

🙋‍♀️ A short introduction - what is your organization all about?
🌈 Contribution guidelines - how can the community get involved?
👩‍💻 Useful resources - where can the community find your docs? Is there anything else the community should know?
🍿 Fun facts - what does your team eat for breakfast?
🧙 Remember, you can do mighty things with the power of [Markdown](https://docs.github.com/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
-->
