# Wallpaper



## 工作描述

​	无参数运行Wallpaper时，Wallpaper会依次执行如下操作

1. 检查根目录下是否存在 data 文件夹，不存在则创建
2. 从bing下载当日的壁纸，并以 yyyy-mm-dd.jpg 的格式保存在data文件夹下
3. 将当日的图片设为壁纸



## 参数

### 仅下载图片

当您仅仅想下载bing当日的壁纸，而不像将他设置为壁纸的时候，您可以使用如下参数

```cmd
Wallpaper -d
```



### 随机设置壁纸

使用该参数会在程序的data文件夹下随机选择一张图片，并且设置为壁纸

```cmd
Wallpaper -random
```



### 打开下载的图片文件夹

```cmd
Wallpaper -od
```