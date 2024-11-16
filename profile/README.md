```mermaid
flowchart LR
    subgraph 现实数据
    地图/孪生工具-->场景
    场景-->地图/孪生工具
    end
    UE插件-->场景
    场景-->UE插件
    subgraph 模拟器
    LibCarla-->UE插件
    UE插件-->LibCarla
    LibCarla-->boost::python
    boost::python-->LibCarla
    end
    控制-->boost::python
    boost::python-->感知
    subgraph 人/车代理
    规划-->控制 
    感知-->规划
    end
```
