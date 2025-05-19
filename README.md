# More99 - 抖音自动识别与点赞工具

More99 是一个自动识别抖音视频内容并模拟点赞、转发行为的工具。通过将手机投屏至 Linux 环境，结合计算机视觉与深度学习技术，完成点赞任务。

## 功能简介

- 自动识别抖音视频内容
- 判断是否是直播，如果是则自动跳过
- 自动模拟点赞、转发、下一个视频动作
- **仅适用于 Linux 系统**

---

## 环境依赖

在运行前，请确保已在 Linux 系统上安装以下组件：

### 1. Python 依赖

请使用 Python 3.8+，并安装以下包：

```bash
pip install opencv-python torch torchvision torchaudio ultralytics
````

### 2. 安装 scrcpy

`scrcpy` 是一个用于将 Android 设备画面投屏到电脑的开源工具。在 Linux 下安装：

```bash
sudo apt update
sudo apt install scrcpy
```

或者使用 snap：

```bash
sudo snap install scrcpy
```

### 3. 启用 ADB 并连接手机

确保你已启用手机的 **开发者模式** 和 **USB 调试** 功能。

然后连接手机：

```bash
adb devices
```

确保设备已连接成功。

---

## 使用方法

### 1. 将手机画面投屏到虚拟摄像头 `/dev/video0`

我们使用 `v4l2loopback` 将 scrcpy 输出推送到 `/dev/video0`：

#### 安装 v4l2loopback：

```bash
sudo apt install v4l2loopback-dkms
```

#### 加载内核模块：

```bash
sudo modprobe v4l2loopback video_nr=0 card_label="scrcpy" exclusive_caps=1
```

#### 启动 scrcpy 并将画面导入到 `/dev/video0`：

```bash
scrcpy --v4l2-sink=/dev/video0 --no-audio-playback
```

---

### 2. 运行程序

确保上述环境与设备准备就绪，运行主程序：

```bash
python play.py
```

程序将从虚拟摄像头中读取视频流，自动识别视频内容，并根据模型判断是否执行点赞动作。

---

## 注意事项

* 本项目仅供学习与研究使用，请勿用于商业或非法用途。
* 请确保使用该工具的合法性，遵守相关平台的服务条款。

---

## 开源许可

MIT License
