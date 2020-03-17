# kubernetes-deployment-tracer

实时追踪你的部署，把放心送到你家。

# 效果

![效果](https://github.com/owenliang/kubernetes-deployment-tracer/blob/master/show.png?raw=true)

# 使用步骤

```
kubectl apply -f files/service_account.yaml
kubectl apply -f files/tracer_deployment.yaml
```

# 二次开发

实现你的callback，注册到tracer函数：

```
if __name__ == '__main__':
    tracer(my_callback)
```

构建自己的镜像

```
docker build . -t 镜像名
```