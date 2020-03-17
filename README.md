# kubernetes-deployment-tracer

实时追踪你的部署，把放心送到你家。

# 效果

![效果](https://github.com/owenliang/kubernetes-deployment-tracer/blob/master/show.jpg?raw=true)

# 使用方法

实现你的callback，注册到tracer函数：

```
if __name__ == '__main__':
    tracer(my_callback)
```