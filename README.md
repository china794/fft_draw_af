# fft_draw_af
快速傅里叶变换绘图工具
使用说明书


1.功能介绍
该程序可以让您在画布上自由绘制任意封闭曲线，使用快速傅里叶变换（FFT）将曲线分解成一系列周转圆（epicycles）。绘制完成后，程序会自动计算这些周转圆的数据并保存到一个文本文档(epicycles.txt)中，然后自动调用draw.exe生成动画来重现您绘制的图形，最后将文本文档中的数据翻译为Excel中规整的大白话。




2.使用步骤
(1)双击运行程序：
下载并解压缩程序包后，找到 fft.exe 文件，双击运行它。

(2)绘制曲线：
打开程序后，会看到一个白色画布窗口。
使用鼠标在画布上按住左键开始绘制曲线。每一帧都会生成一个点，程序会自动将这些点连成线。
绘制时请尽量闭合曲线，以确保傅里叶变换效果最佳。如果您绘制的不是闭合曲线，会自动将首尾点相连

(3)完成绘图：
当您完成绘制曲线后，程序会自动开始计算傅里叶系数，并将这些数据保存到一个文件 epicycles.txt 中。

(4)生成动画：
程序将自动运行另一个脚本 draw.exe，根据 epicycles.txt 文件中的数据生成周转圆动画。
动画窗口会显示周转圆的运动轨迹和重新绘制的曲线，直到您关闭窗口。

(5)查看结果：
程序将自动运行另一个脚本 xlsx.exe，根据 epicycles.txt 文件中的数据生成Excel表格文件“机械师专用.xlsx”。
动画完成后，可按保存图标将动画的截图另存为png格式图片。另外，关闭动画后程序会自动打开xlsx文件。



(6)注意事项
在绘制曲线时，建议不要过快地划线，以便更精确地控制曲线形状。
如果在运行过程中遇到任何错误或问题，请联系我解决。



3.作者信息
昵称： 阿飞 qq:1391897309 qq:3824075452
V2.0
发布日期： 2024年8月28日
