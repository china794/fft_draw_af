import random

import pygame

# 设置屏幕大小和初始参数
WIDTH, HEIGHT = 1200, 600
FPS = 30
BACKGROUND_COLOR = (0, 0, 0)  # 背景色为黑色
UP_COLOR = (0, 255, 0)  # 上涨为绿色
DOWN_COLOR = (255, 0, 0)  # 下跌为红色
LINE_COLOR = (255, 255, 255)  # 折线颜色为白色
INITIAL_PRICE = 300  # 初始股价
CANDLE_WIDTH = 5  # 每个K线的宽度
ZOOM_SCALE = 2  # 缩放因子
PAN_SPEED = 5  # 平移速度
JUMP_PROBABILITY = 0.1  # 跳空的概率
JUMP_AMOUNT = 50  # 跳空的幅度

# 初始化 pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Stock Market K-Line Simulation")
clock = pygame.time.Clock()

# 股市数据：包含开盘价、收盘价、最高价和最低价
prices = [{'open': INITIAL_PRICE, 'close': INITIAL_PRICE, 'high': INITIAL_PRICE, 'low': INITIAL_PRICE}]
x_positions = list(range(0, WIDTH, CANDLE_WIDTH * 2))  # 每个K线占据两个单位宽度
offset_x = 0  # 初始偏移量
paused = False  # 是否暂停动画
follow_last_candle = True  # 是否跟随最后一根K线
show_line = False  # 是否显示折线图


def simulate_stock_movement(prices):
    """模拟股价的涨跌变化，生成新的K线数据"""
    last_close = prices[-1]['close']

    # 随机产生跳空现象
    if random.random() < JUMP_PROBABILITY:
        new_open = last_close + random.choice([-JUMP_AMOUNT, JUMP_AMOUNT])
    else:
        new_open = last_close

    # 随机产生收盘价变化，偶尔出现大幅波动
    if random.random() < 0.001:  # 2% 的概率出现大幅波动
        change = random.uniform(-300, 300)
    else:
        change = random.uniform(-30, 30)

    new_close = new_open + change
    new_high = max(new_open, new_close) + random.uniform(0, 10)  # 最高价增加更多随机范围
    new_low = min(new_open, new_close) - random.uniform(0, 10)  # 最低价减少更多随机范围
    prices.append({'open': new_open, 'close': new_close, 'high': new_high, 'low': new_low})


def get_screen_price_range(prices, offset_x):
    """获取当前屏幕范围内的最高价和最低价"""
    min_price = float('inf')
    max_price = float('-inf')

    for i, price in enumerate(prices):
        x = i * CANDLE_WIDTH * 2 + offset_x
        if -CANDLE_WIDTH * 2 <= x <= WIDTH:
            min_price = min(min_price, price['low'])
            max_price = max(max_price, price['high'])

    return max_price, min_price


def draw_candles(screen, prices, offset_x, scale_y):
    """绘制K线图"""
    screen.fill(BACKGROUND_COLOR)  # 填充背景

    line_points = []

    max_price, min_price = get_screen_price_range(prices, offset_x)

    for i, price in enumerate(prices):
        x = i * CANDLE_WIDTH * 2 + offset_x
        if -CANDLE_WIDTH * 2 <= x <= WIDTH:
            open_price = HEIGHT - int((price['open'] - min_price) * scale_y)
            close_price = HEIGHT - int((price['close'] - min_price) * scale_y)
            high_price = HEIGHT - int((price['high'] - min_price) * scale_y)
            low_price = HEIGHT - int((price['low'] - min_price) * scale_y)

            # 确定颜色
            if price['close'] > price['open']:
                color = UP_COLOR  # 上涨为绿色
                rect_top = close_price
                rect_bottom = open_price
            else:
                color = DOWN_COLOR  # 下跌为红色
                rect_top = open_price
                rect_bottom = close_price

            # 绘制最高价和最低价的影线
            pygame.draw.line(screen, color, (x + CANDLE_WIDTH // 2, high_price), (x + CANDLE_WIDTH // 2, low_price), 1)
            # 绘制开盘价和收盘价的实体
            pygame.draw.rect(screen, color, (x, rect_top, CANDLE_WIDTH, abs(close_price - open_price)))

            # 添加折线图点
            line_points.append((x + CANDLE_WIDTH // 2, close_price))

    # 绘制折线图
    if show_line and len(line_points) > 1:
        pygame.draw.lines(screen, LINE_COLOR, False, line_points, 1)

    # 绘制准线
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if 0 <= mouse_x < WIDTH:
        # 垂直准线
        pygame.draw.line(screen, (255, 255, 255), (mouse_x, 0), (mouse_x, HEIGHT), 1)
        # 显示光标下的K线数据
        index = (mouse_x - offset_x) // (CANDLE_WIDTH * 2)
        if 0 <= index < len(prices):
            price = prices[index]
            font = pygame.font.SysFont(None, 20)
            text = font.render(
                f'O: {price["open"]:.2f} C: {price["close"]:.2f} H: {price["high"]:.2f} L: {price["low"]:.2f}', True,
                (255, 255, 255))
            screen.blit(text, (mouse_x + 10, mouse_y - 20))

    # 绘制坐标轴和水平对比线
    font = pygame.font.SysFont(None, 20)
    for i in range(5):
        y = HEIGHT - int(i * HEIGHT / 4)
        value = min_price + (max_price - min_price) * i / 4
        pygame.draw.line(screen, (50, 50, 50), (0, y), (WIDTH, y), 1)
        text = font.render(f'{value:.2f}', True, (255, 255, 255))
        screen.blit(text, (0, y - 10))
    pygame.draw.line(screen, (255, 255, 255), (0, HEIGHT - 1), (WIDTH, HEIGHT - 1), 2)


def zoom_candles(scale):
    """调整K线宽度"""
    global x_positions
    global CANDLE_WIDTH
    CANDLE_WIDTH = int(CANDLE_WIDTH * scale)
    x_positions = list(range(0, WIDTH, CANDLE_WIDTH * 2))


# 主循环
running = True
frame_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused  # 切换暂停状态
            elif event.key == pygame.K_f:
                follow_last_candle = not follow_last_candle  # 切换是否跟随最后一根K线
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                show_line = not show_line  # 切换是否显示折线图
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # 鼠标滚轮向上滚动
                zoom_candles(ZOOM_SCALE)
            elif event.button == 5:  # 鼠标滚轮向下滚动
                zoom_candles(1 / ZOOM_SCALE)
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    if not paused:
        frame_count += 1
        if frame_count % (FPS * 0.1) == 0:  # 每隔   添加一个K线
            simulate_stock_movement(prices)
            frame_count = 0

    # 更新视图跟随最后一根K线
    if follow_last_candle and prices:
        last_candle_x = len(prices) * CANDLE_WIDTH * 2
        offset_x = min(0, WIDTH - last_candle_x)

    # 计算屏幕内的最大最小价格
    max_price, min_price = get_screen_price_range(prices, offset_x)
    price_range = max_price - min_price
    if price_range == 0:
        price_range = 1  # 防止除以零
    scale_y = HEIGHT / price_range

    draw_candles(screen, prices, offset_x, scale_y)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
