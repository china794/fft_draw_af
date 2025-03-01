import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import subprocess
from matplotlib.backend_bases import MouseButton

plt.rcParams['font.family'] = 'Microsoft YaHei'

# 全局变量存储绘制的点
points = []
drawing = False


# 处理鼠标按下事件的函数
def onpress(event):
    global drawing
    if event.button == MouseButton.LEFT:
        drawing = True
        points.append([event.xdata, event.ydata])


# 处理鼠标移动事件的函数
def onmove(event):
    if drawing and event.xdata is not None and event.ydata is not None:
        points.append([event.xdata, event.ydata])
        plt.plot([points[-2][0], points[-1][0]], [points[-2][1], points[-1][1]], 'b-')
        plt.draw()


# 处理鼠标松开事件的函数
def onrelease(event):
    global drawing
    if event.button == MouseButton.LEFT:
        drawing = False
        process_curve(points)


# 处理绘制的曲线并执行 FFT 的函数
def process_curve(points):
    # 将点列表转换为 numpy 数组
    points = np.array(points)

    # 转换为复数 (x + iy)
    complex_points = points[:, 0] + 1j * points[:, 1]

    # 执行 FFT
    fft_result = fft(complex_points)

    # 计算频率
    n = len(fft_result)
    frequencies = np.fft.fftfreq(n)

    # 按频率大小排序
    indices = np.argsort(np.abs(frequencies))

    # 将结果写入 epicycles.txt
    with open("epicycles.txt", "w") as f:
        for i in indices:
            freq = int(np.round(frequencies[i] * n))
            radius = np.abs(fft_result[i]) / n
            phase = np.angle(fft_result[i])
            if radius > 0.01:  # 过滤掉非常小的半径
                f.write(f"Frequency: {freq}, Radius: {radius}, Phase: {phase}\n")

    # 调用 draw.exe
    subprocess.run(['python', 'draw.py'], check=True)
    subprocess.run(['python', 'xlsx.py'], check=True)
    subprocess.run(['start', '机械师专用.xlsx'], shell=True, check=True)


# 设置绘图
fig, ax = plt.subplots()
ax.set_title(
    "By 阿飞\n按住左键开始绘制，松开左键完成，第二次绘制需重开。\n关闭动画会自动打开数据表格,但第二次绘制前必须关闭表格。")
ax.set_aspect('equal')
ax.set_xlim(-30, 30)
ax.set_ylim(-20, 20)

# 连接事件处理程序
fig.canvas.mpl_connect('button_press_event', onpress)
fig.canvas.mpl_connect('motion_notify_event', onmove)
fig.canvas.mpl_connect('button_release_event', onrelease)

plt.show()
