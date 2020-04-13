# Wallpaper



## 工作描述

​	无参数运行Wallpaper时，Wallpaper会依次执行如下操作

1. 检查根目录下是否存在 data 文件夹，不存在则创建，检测是否有config.json文件，不存在进入配置
2. 无命令行参数执行配置，有则执行参数



## 使用

### 仅下载图片

仅想下载bing当日的壁纸，不希望设置为壁纸时

```cmd
Wallpaper -d
```



### 随机设置壁纸

在程序的data文件夹下随机选择一张图片设置为壁纸

方法一(此方法重启Wallpaper失效)：

```cmd
Wallpaper -random
```

方法二：

```cmd
# 使用如下命令重新配置，然后重启Wallpaper
Wallpaper -config
```

方法三：

修改config.json文件的"ChangeMode": "bing-day"为"ChangeMode": "random"



### 打开下载图片/随机库文件夹

```cmd
Wallpaper -od
```