import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 使用微软雅黑


# 解析文本文件
def parse_file(filename):
    epicycles = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split(',')
            frequency = float(parts[0].split(':')[1].strip())
            radius = float(parts[1].split(':')[1].strip())
            phase = float(parts[2].split(':')[1].strip())
            epicycles.append((frequency, radius, phase))
    return epicycles


# 计算每个圆的中心位置
def calculate_epicycle_positions(epicycles, t):
    positions = []
    x, y = 0, 0
    for frequency, radius, phase in epicycles:
        angle = frequency * t + phase
        x += radius * np.cos(angle)
        y += radius * np.sin(angle)
        positions.append((x, y))
    return positions


# 更新动画帧
def update(frame, epicycles, trajectory, line, trace_line, speed_slider, is_paused):
    global last_speed

    if is_paused[0]:  # 如果动画暂停，返回当前图形元素，不更新
        return line, trace_line

    speed_factor = speed_slider.val

    # 如果速度发生改变，清除轨迹
    if speed_factor != last_speed:
        last_speed = speed_factor
        trajectory.clear()  # 清除现有轨迹
        trace_line.set_data([], [])  # 清空红色轨迹线
        return line, trace_line

    # 更新时间参数
    t = frame / 100.0 * 2 * np.pi * speed_factor
    positions = calculate_epicycle_positions(epicycles, t)

    # 更新周转圆的轨迹
    line.set_data([p[0] for p in positions], [p[1] for p in positions])

    # 更新最终点的轨迹
    trajectory.append(positions[-1])
    trace_line.set_data([p[0] for p in trajectory], [p[1] for p in trajectory])

    return line, trace_line


# 滑块改变时的回调函数
def on_slider_change(val):
    global last_speed
    last_speed = speed_slider.val  # 更新全局速度因子
    trajectory.clear()  # 清除轨迹点
    trace_line.set_data([], [])  # 清空红色轨迹线


# 暂停/播放按钮回调
def toggle_pause(event):
    is_paused[0] = not is_paused[0]  # 切换暂停状态


# 清除轨迹按钮回调
def clear_trajectory(event):
    trajectory.clear()
    trace_line.set_data([], [])  # 清空红色轨迹线
    fig.canvas.draw()  # 刷新画布


# 主函数
def main(filename):
    global speed_slider, last_speed, is_paused, trajectory, trace_line, fig

    epicycles = parse_file(filename)
    last_speed = 0.1  # 初始速度因子
    is_paused = [False]  # 初始化动画状态为未暂停

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)  # 调整底部区域以容纳滑块和按钮
    ax.set_aspect('equal')
    ax.set_xlim(-30, 30)
    ax.set_ylim(-20, 20)

    line, = ax.plot([], [], 'bo-', markersize=1, linewidth=0.5)  # 蓝色点和线代表周转圆
    trace_line, = ax.plot([], [], 'r-', linewidth=1)  # 红色线代表轨迹

    trajectory = []

    # 添加速度滑块
    ax_slider = plt.axes([0.25, 0.15, 0.5, 0.03], facecolor='lightgoldenrodyellow')  # 滑块的轴位置
    speed_slider = Slider(ax_slider, '倍速', 0.01, 2.0, valinit=last_speed, valstep=0.01)
    speed_slider.on_changed(on_slider_change)

    # 添加暂停按钮
    ax_button_pause = plt.axes([0.25, 0.05, 0.2, 0.04])
    button_pause = Button(ax_button_pause, '暂停/开始（跳帧）')
    button_pause.on_clicked(toggle_pause)

    # 添加清除轨迹按钮
    ax_button_clear = plt.axes([0.55, 0.05, 0.1, 0.04])
    button_clear = Button(ax_button_clear, '清除轨迹')
    button_clear.on_clicked(clear_trajectory)

    ani = FuncAnimation(
        fig, update, frames=range(1000), fargs=(epicycles, trajectory, line, trace_line, speed_slider, is_paused),
        interval=20, blit=True
    )

    plt.show()


if __name__ == "__main__":
    filename = 'epicycles.txt'
    main(filename)
