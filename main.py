import numpy as np
import matplotlib.pyplot as plt
import os #230719增加

#十字路口8机器人--ORCA运行结果

#设置标题大小格式--暂不需要
# plt.title('title',fontsize='large',fontweight='bold') #设置字体大小与格式
# plt.title('title',color='black') #设置字体颜色

#一次建立fig和ax设置画布大小方法
fig,ax = plt.subplots(1,1,figsize=(36,36))

# #设置坐标轴范围--IROS24-实验4-230226
# plt.xlim((-3.0, 4.2))
# plt.ylim((-2.5, 2.6))

#设置坐标轴范围--IROS24-实验3-230227
plt.xlim((-2.8, 4.3))
plt.ylim((-2.6, 2.5))

#设置坐标轴名称--字体大小
plt.xlabel('x(m)',fontsize=50)
plt.ylabel('y(m)',fontsize=50)

#设置坐标xy轴--刻度字体大小
plt.xticks(fontsize=45)
plt.yticks(fontsize=45)

#设置等比例画图
ax = plt.gca()
ax.set_aspect(1)

#全局参数的设定
##############################################################################################

# 查找 n 个二维数组的最大行数
max_line_rows = 0

#颜色列表
Color_List = ['gold','red','blue','green','aqua','black',   'darkgoldenrod','gray'] #

#颜色深度初值设定
Color_depth = [ 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95 ]

#机器人目标位置
T_x =[3.11, -3.08, -0.94, -2.93, -0.47, 2.62 ]
T_z =[ -1.87, -1.77, -1.67, 1.46, -1.97, -1.48 ]

#机器人出发位置
B_x =[-0.71, -0.36, -2.79, 2.98, 2.84, -2.86 ]
B_z =[ 0.24, -0.34, -0.76, 0.36,  -0.57,  1.00 ]

# #墙体关键点--宽度约0.5
# W_x =[5.544 , 5.544  ,-5.51  , -5.51 , 28.99 ,  28.99 , 5.5 , -5.5 , -29.22 , -29.19 , -5.54 , 5.49]
# W_z =[13.009 , 2.02  ,2.02  , 13.009 , 13.009 , 2.01 , -23.1 , -23.1 , 1.98 , 12.99 ,  39.06 , 39.06]

#墙体关键点--宽度约0.5
W_x =[-3.45, -3.45 ,-2.35 , -2.35 ,-1.25,     -1.25,  0 ,   0, 2.25, 2.25,     3.45 , 3.45 ]
W_z =[1.85 , -2.45 , -2.45 , 0.62 ,0.62 ,     -2.45,-2.45, 0.4, 0.4, -2.45,    -2.45, 1.85 ]


# Color_depth_2 = 0.9
# Color_depth_3 = 0.9
# Color_depth_4 = 0.9
# Color_depth_5 = 0.9
# Color_depth_6 = 0.9
# Color_depth_7 = 0.9
# Color_depth_8 = 0.9

# 拆分数据--机器人所有数据
new_arrays = [[] for _ in range(6)]


#提取txt文件中数据
def txt_to_array():
    # 路径按照自己存储路径修改
    file_path = r'D:\python_huatu\iros_2402\data_shiyan_4\data_240227_1.txt'   # 路径按照自己存储路径修改\data_230720_drl_2.txt

    with open(file_path, "r") as file:
        content = file.read()

    # 将数据按行拆分
    lines = content.split("\n")

    # 创建一个空的字典
    grouped_data = {}

    # 逐行处理数据
    for line in lines:
        # 去除空格字符，并将每行的值拆分成列表
        line = line.replace(" ", "")
        # 将每行的值拆分为列表
        values = line.split(",")

        # 跳过空行
        if len(values) == 0:
            continue

        for value in values:
            # 跳过空字符串
            if value == "":
                continue

            try:
                value = float(value)
                # print(value, type(value))
            except ValueError:
                print(f"Invalid value: {value}")

        # 保留3位小数
        values = [round(float(value), 3) for value in values]

        # 获取第一个数据
        first_value = float(values[0])

        # 添加到对应的数组中
        if first_value in grouped_data:
            grouped_data[first_value].append(values)
        else:
            grouped_data[first_value] = [values]


    # 打印结果
    for key, values in grouped_data.items():
        print(f"Key: {key}")
        for line in values:
            index = int(line[0])
            global new_arrays
            new_arrays[index].append([round(x, 3) for x in line[0:]])
        #     print(line)
        print(new_arrays[index])
        print()

    # n 个二维数组拼装起来的列表--用于找最大数组
    d3_arr = [new_arrays[0], new_arrays[1], new_arrays[2], new_arrays[3], new_arrays[4],
              new_arrays[5]]  # 将需要查找的数组按顺序放入列表中

    # 查找 n 个二维数组的最大行数
    global max_line_rows
    max_line_rows = max(len(array) for array in d3_arr)
    print('max_line_rows = ' + str(max_line_rows))

#绘制出发点
def draw_beginpoint():
    # 开始位置--标定
    # 数据缩小10倍处理
    for _i in range(len(B_x)):
        B_x[_i] = B_x[_i] / 1
        B_z[_i] = B_z[_i] / 1

    for _i in range(len(B_x)):
        plt.scatter(B_x[_i], B_z[_i], s=3900, c=Color_List[_i], marker='x', alpha=1)
        # 散点图 s为半径，c为颜色 ‘b’为蓝色,marker='o'箭头形状不同,alpha=''透明度

#绘制目标点
def draw_target():
    # 目标位置--标定
    # 数据缩小10倍处理
    for _i in range(len(T_x)):
        T_x[_i] = T_x[_i] / 1
        T_z[_i] = T_z[_i] / 1

    for _i in range(len(T_x)):
        plt.scatter(T_x[_i], T_z[_i], s=3900, c=Color_List[_i], marker='*', alpha=1)
        # 散点图 s为半径，c为颜色 ‘b’为蓝色,marker='o'箭头形状不同,alpha=''透明度
        # # 到达点加注释--对不齐，需要手工对齐
        # plt.annotate(str(T_t[_i]), xy=(T_x[_i], T_z[_i]), xytext=(T_x[_i] + __dui_x[_i], T_z[_i] + __dui_y[_i]), weight="bold",
        #              color=Color_List[_i], arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color=Color_List[_i]))

#绘制墙体关键点
def draw_wallpoint():
    # 墙体关键点--标定
    # 数据缩小10倍处理
    for _i in range(len(W_x)):
        W_x[_i] = W_x[_i] / 1
        W_z[_i] = W_z[_i] / 1

    for _i in range(len(W_x)):
        plt.scatter(W_x[_i], W_z[_i], s=80, c='pink', marker='s', alpha=0.9)
        # 散点图 s为半径，c为颜色 ‘b’为蓝色,marker='o'箭头形状不同,alpha=''透明度

#绘制轨迹线--index编号，jump_step轨迹点跳点的步数
def draw_traj_lines(index,jump_step): #self,是用在class类里面的
    # 提取二维数组的第一列数值到一维数组Pos_x
    Pos_x = [row[1] for row in new_arrays[index]]
    Pos_y = [row[2] for row in new_arrays[index]]

    # 打印轨迹线
    plt.plot(Pos_x, Pos_y, linewidth=4.0, color=Color_List[index])

    # 使用嵌套循环遍历二维数组
    row_counter = 0
    for row in new_arrays[index]:
        # for element in row:
        # print('robot-1')
        # 打印轨迹线
        # plt.plot(row[0], row[1], linewidth=0.3, color="gold")
        # 取模运算：如果_i对3取模余数为1，则打印轨迹点
        # if (row. + 4) % 3 == 1:

        if row_counter % jump_step == 0:
            global Color_depth
            Color_depth[index] = Color_depth[index] - 2 * 0.85 / float(max_line_rows)  # - 0.03 根据最大行数
            plt.scatter(row[1], row[2], s=1500, c=Color_List[index], marker='o', alpha=Color_depth[index])
        row_counter += 1
        # print('robot-1')

if __name__ == '__main__':
    txt_to_array()

    # # 绘制出发点
    # draw_beginpoint()
    #
    # # 绘制目标点
    # draw_target()
    #
    # # 绘制墙体关键点
    # draw_wallpoint()

    # 绘制轨迹线--index的编号应为0-5
    draw_traj_lines(0,2)
    draw_traj_lines(1,2)
    draw_traj_lines(2,2)
    draw_traj_lines(3,2)
    draw_traj_lines(4,2)
    draw_traj_lines(5,2)


    #保存和展示图片
    plt.savefig('iros_test3_1.png', bbox_inches='tight', pad_inches=0.2)#tmech_drl_2.pdf
    plt.show()

#运行程序 打开Python控制台（界面下方），在控制台输入 %run tmech_3.py   %run main.py
