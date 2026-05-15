# LMusic

一个轻量级的免费开源音乐app，集成了歌曲搜索并下载、管理和播放等功能

## 快速开始

**你可以通过以下两种方式之一运行本项目：**

### 方式一：直接运行 EXE 文件（推荐非开发用户）

1. 前往 [Releases](https://github.com/lightyear2008/LMusic/releases) 页面下载最新版本的 `LMusic.zip`。
2. 解压下载的压缩包到你电脑上的任意位置。
3. 进入解压后的文件夹，双击运行 `LMusic.exe` 即可。

### 方式二：在 Python 环境中运行

#### 环境要求

- Python 3.8 或更高版本

- [Edge浏览器驱动](./drivers)对应版本的Edge浏览器（若此驱动较浏览器版本低，可手动替换，[查看替换教程]()）
1. **克隆项目**
   
   ```bash
   git clone https://github.com/yourusername/LMusic.git
   cd LMusic
   ```

2. **安装依赖**
   
   ```bash
   pip install -r requirements.txt
   ```

3. **运行程序**
   
   ```bash
   python main.py
   ```

## 功能特性

- **本地音乐播放** - 支持 MP3 格式
- **歌单管理** - 创建、编辑、切换不同歌单
- **多种主题** - 内置多种滑块等样式，支持自定义
- **歌曲搜索** - 自动联网搜索并下载歌曲到本地
- **现代化界面** - 暗色主题，圆角设计，平滑动画
- **轻量级应用** - 原始大小仅150MB，内存占用极低

## 界面预览

<img title="" src="./screenshots/screenshot1.jpg" alt="" width="539">                  <img title="" src="./screenshots/screenshot2.jpg" alt="" width="300">

## 文件说明

| 文件           | 功能       |
| ------------ | -------- |
| climber.py   | 所有网络爬虫函数 |
| searchbox.py | 搜索框GUI   |
|              |          |

## 支持创作者

## 许可证

## 版本日志
