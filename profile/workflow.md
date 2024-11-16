```mermaid
flowchart LR
    地图/孪生工具-->场景
    场景-->地图/孪生工具
    UE插件-->场景
    场景-->UE插件
    LibCarla-->UE插件
    UE插件-->LibCarla
    LibCarla-->boost::python
    boost::python-->LibCarla
    控制-->boost::python
    boost::python-->感知;
    规划-->控制 
    感知-->规划
```
