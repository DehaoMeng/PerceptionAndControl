"""
导入第三方库
"""
import serial
import serial.tools.list_ports
from PySide2.QtUiTools import QUiLoader    #qt designer 好用的库，图形化界面必备
from PySide2.QtCore import QFile
from PySide2.QtCore import Signal, QObject
from PySide2.QtWidgets import QFileDialog
import re
import sys
import time
import binascii
from PyQt5 import QtWidgets
import threading
import matplotlib.pyplot as plt
import matplotlib
import datetime
import pyecharts.options as opts  # 绘图
from pyecharts.charts import Line   # 导入Line模块
import webbrowser

class Communication:
    # 初始化连接串口
    def __init__(self, com, bps, timeout):
        self.port = com
        self.bps = bps
        self.timeout = timeout
        global Ret
        try:
            # 打开串口，并得到串口对象
            self.main_engine = serial.Serial(self.port, self.bps, timeout=self.timeout)
            # 判断是否打开成功
            if (self.main_engine.is_open):
                Ret = True
        except Exception as e:
            print("---异常---：", e)

    # 打印设备基本信息
    def Print_Name(self):
        print(self.main_engine.name)  # 设备名字
        print(self.main_engine.port)  # 读或者写端口
        print(self.main_engine.baudrate)  # 波特率
        print(self.main_engine.bytesize)  # 字节大小
        print(self.main_engine.parity)  # 校验位
        print(self.main_engine.stopbits)  # 停止位
        print(self.main_engine.timeout)  # 读超时设置
        print(self.main_engine.writeTimeout)  # 写超时
        print(self.main_engine.xonxoff)  # 软件流控
        print(self.main_engine.rtscts)  # 软件流控
        print(self.main_engine.dsrdtr)  # 硬件流控
        print(self.main_engine.interCharTimeout)  # 字符间隔超时

    # 打开串口
    def Open_Engine(self):
        self.main_engine.open()

    # 关闭串口
    def Close_Engine(self):
        self.main_engine.close()
        print(self.main_engine.is_open)  # 检验串口是否打开

    # 打印可用串口列表
    @staticmethod
    def Print_Used_Com():
        port_list = list(serial.tools.list_ports.comports())
        print(port_list)

    # 接收指定大小的数据
    # 从串口读size个字节。如果指定超时，则可能在超时后返回较少的字节；如果没有指定超时，则会一直等到收完指定的字节数。
    def Read_Size(self, size):
        data=self.main_engine.read(size=size)
        return data

    # 接收一行数据
    # 使用readline()时应该注意：打开串口时应该指定超时，否则如果串口没有收到新行，则会一直等待。
    # 如果没有超时，readline会报异常。
    def Read_Line(self):
        return self.main_engine.readline()

    # 发数据
    def Send_data(self, data):
        self.main_engine.write(data)

    # 接收数据
    # 一个整型数据占两个字节
    # 一个字符占一个字节

    def Recive_data(self, way):
        # 循环接收数据，此为死循环，可用线程实现
        print("开始接收数据：")
        while True:
            try:
                # 一个字节一个字节的接收
                if self.main_engine.in_waiting:
                    if (way == 0):
                        for i in range(self.main_engine.in_waiting):
                            print("接收ascii数据：" + re.sub("\D","",str(self.Read_Size(1))))
                            data1 = self.Read_Size(1).hex()  # 转为十六进制
                            data2 = int(data1, 16)  # 转为十进制print("收到数据十六进制："+data1+"  收到数据十进制："+str(data2))
                    if (way == 1):
                        # 整体接收
                        data = self.main_engine.read_all()  # 方式二print("接收ascii数据：", data)
                        print(data)
                        Status.ms.text_print.emit(data)
            except Exception as e:
                print("异常报错：", e)

class MySignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    receive_print =Signal()
    text_print = Signal(str)
# 温度
class Temperature:
    def __init__(self, now_temper):  # 构造函数
        self.now_temper = now_temper  # 当前温度
        self.list_tem = [now_temper, now_temper, now_temper, now_temper, now_temper, now_temper, now_temper, now_temper, now_temper, now_temper]
        self.list_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def setTime1(self):
        now = datetime.datetime.now()
        now_time = now.strftime("%H:%M:%S")
        return now_time

    def set_time2(self):
        now = datetime.datetime.now()
        now_time = now.strftime("%H:%M:%S")
        self.list_time = [now_time, now_time, now_time, now_time, now_time]

    def add(self):
        time.sleep(0.3)
        self.now_temper = self.now_temper + 1  # 当前温度每3秒加0.5°C
        # self.start()
        self.list_tem[0] = self.list_tem[1]
        self.list_tem[1] = self.list_tem[2]
        self.list_tem[2] = self.list_tem[3]
        self.list_tem[3] = self.list_tem[4]
        self.list_tem[4] = self.list_tem[5]
        self.list_tem[5] = self.list_tem[6]
        self.list_tem[6] = self.list_tem[7]
        self.list_tem[7] = self.list_tem[8]
        self.list_tem[8] = self.list_tem[9]
        self.list_tem[9] = self.now_temper
        print(self.list_tem)
        self.list_time[0] = self.list_time[1]
        self.list_time[1] = self.list_time[2]
        self.list_time[2] = self.list_time[3]
        self.list_time[3] = self.list_time[4]
        self.list_time[4] = self.list_time[5]
        self.list_time[5] = self.list_time[6]
        self.list_time[6] = self.list_time[7]
        self.list_time[7] = self.list_time[8]
        self.list_time[8] = self.list_time[9]
        self.list_time[9] = self.setTime1()
        print(self.list_time)

    def decrease(self):
        time.sleep(0.3)
        self.now_temper = self.now_temper - 1  # 当前温度每3秒减0.5°C
        self.list_tem[0] = self.list_tem[1]
        self.list_tem[1] = self.list_tem[2]
        self.list_tem[2] = self.list_tem[3]
        self.list_tem[3] = self.list_tem[4]
        self.list_tem[4] = self.list_tem[5]
        self.list_tem[5] = self.list_tem[6]
        self.list_tem[6] = self.list_tem[7]
        self.list_tem[7] = self.list_tem[8]
        self.list_tem[8] = self.list_tem[9]
        self.list_tem[9] = self.now_temper
        print(self.list_tem)

        self.list_time[0] = self.list_time[1]
        self.list_time[1] = self.list_time[2]
        self.list_time[2] = self.list_time[3]
        self.list_time[3] = self.list_time[4]
        self.list_time[4] = self.list_time[5]
        self.list_time[5] = self.list_time[6]
        self.list_time[6] = self.list_time[7]
        self.list_time[7] = self.list_time[8]
        self.list_time[8] = self.list_time[9]
        self.list_time[9] = self.setTime1()
        print(self.list_time)

    def exchange(self,set):
        i = 10
        while i > 0:
            if self.now_temper > set:
                self.decrease()
            elif self.now_temper <= set:
                self.add()
            elif abs(self.now_temper - set) <= 1:
                i = 0
            i = i - 1
        print(self.list_tem)
        return self.list_tem

    def Scatter(self, set,colour):  # 绘制折线图html文件
        time = self.list_time[-10:]  # 取time末尾10位
        tempture = self.list_tem[-10:]  # 取温度末尾10位
        c = (
            Line(init_opts=opts.InitOpts(
                width="900px",
                height="600px",
            )).add_xaxis(time).add_yaxis('温度/°C', tempture).set_colors(colour).set_global_opts(
                title_opts=opts.TitleOpts(title="温度变化"),
                yaxis_opts=opts.AxisOpts(name="温度°C"),
                xaxis_opts=opts.AxisOpts(name="time"))
        ).render("chart.html")
        webbrowser.open("chart.html")
# 主界面
class Status:
    def __init__(self):
        qfile_Server = QFile("express_control.ui")
        qfile_Server.open(QFile.ReadOnly)
        qfile_Server.close()
        # 从 UI 定义中动态 创建一个相应的窗口对象
        self.ui = QUiLoader().load(qfile_Server)
        self.start=0
        self.a = Temperature(30)
        self.conn = Communication("com2", 38400, 0.5)
        self.ui.open_drawer.clicked.connect(self.open_drawer)
        self.ui.close_drawer.clicked.connect(self.close_drawer)
        self.ui.openbutton.clicked.connect(self.openwork)
        self.ui.closebutton.clicked.connect(self.closework)
        self.ui.control_temperature.clicked.connect(self.control_temp)
        self.ui.set_contemper.clicked.connect(self.set_controltemp)
        self.ui.temper_chart.clicked.connect(self.chart)
        self.ui.now_temperature.setText(str(self.a.now_temper))


        self.ui.dr1.setStyleSheet("background-color:#008080;")
        self.ui.dr2.setStyleSheet("background-color:#008080;")
        self.ui.dr3.setStyleSheet("background-color:#008080;")
        self.ui.dr4.setStyleSheet("background-color:#008080;")
        self.ui.dr5.setStyleSheet("background-color:#008080;")
        self.ui.dr6.setStyleSheet("background-color:#008080;")
        self.ui.dr7.setStyleSheet("background-color:#008080;")
        self.ui.dr8.setStyleSheet("background-color:#008080;")
        self.ui.dr9.setStyleSheet("background-color:#008080;")
        self.ui.dr10.setStyleSheet("background-color:#008080;")

        self.open_close='0000000000000000'  #控制抽屉开关
        self.flag='01'    #控制压缩机开关
        self.wendu='00000000'#控制温度
        self.ms = MySignals()
        self.ms.text_print.connect(self.text_signal)

    def chose_drawer(self):
        drawer=self.ui.chose_drawer.text()
        drawer=int(re.sub("\D","",drawer))
        return drawer

    def chart(self):
        set_wendu = self.ui.set_temperature.text()
        set_wendu=int(re.sub("\D","",set_wendu))
        for i in self.a.exchange(set_wendu):
            self.ui.now_temperature.setText(str(i))
        self.a.Scatter(set_wendu,"blue")

    def closework(self):
        exit(0)

    def openwork(self):
        data = 'FFFF1C'+'75'+'7F05100125F002010A020507080802FF03FF032036E8FFF7FFFF1C757F05100125F002010A020507080802FF03FF032036E8FFF7'
        data = binascii.a2b_hex(data)  # 十六进制转字节流
        self.conn.Send_data(data)


    def open_drawer(self):
        # global i
        # i = hex(int(i))[2:].zfill(2)
        point=self.chose_drawer()

        time.sleep(0.3)  # 小睡300ms，给路灯反应时间
        send_data1='FFFF0C'+'76'+'0103'   #首
        # send_data2 = '0000000000000000'
        send_data3='1E58FFF7'
        send_data2=list(self.open_close)
        if point==1:
            send_data2[7]='1'
            self.ui.dr1.setStyleSheet("background-color:#ffff00;")
        elif point==2:
            send_data2[6] = '1'
            self.ui.dr2.setStyleSheet("background-color:#ffff00;")
        elif point==3:
            # data3 = 'FFFF0C770103' + '0400' + '1E58FFF7'
            send_data2[5] = '1'
            self.ui.dr3.setStyleSheet("background-color:#ffff00;")
        elif point==4:
            # data4 = 'FFFF0C770103' + '0800' + '1E58FFF7'
            send_data2[4] = '1'
            self.ui.dr4.setStyleSheet("background-color:#ffff00;")
        elif point==5:
            # data5 = 'FFFF0C770103' + '1000' + '1E58FFF7'
            send_data2[3] = '1'
            self.ui.dr5.setStyleSheet("background-color:#ffff00;")
        elif point==6:
            send_data2[2] = '1'
            self.ui.dr6.setStyleSheet("background-color:#ffff00;")
        elif point==7:
            # data7 = 'FFFF0C770103' + '4000' + '1E58FFF7'
            send_data2[1] = '1'
            self.ui.dr7.setStyleSheet("background-color:#ffff00;")
        elif point==8:
            # data8 = 'FFFF0C770103' + '8000' + '1E58FFF7'
            send_data2[0] = '1'
            self.ui.dr8.setStyleSheet("background-color:#ffff00;")
        elif point==9:
            # data9 = 'FFFF0C770103' + '0001' + '1E58FFF7'
            send_data2[15] = '1'
            self.ui.dr9.setStyleSheet("background-color:#ffff00;")
        elif point==10:
            # data10 = 'FFFF0C770103' + '0002' + '1E58FFF7'
            send_data2[14] = '1'
            self.ui.dr10.setStyleSheet("background-color:#ffff00;")
        else:
            pass
            #self.ui.drawer_state.append(f"没有这个号码的抽屉")  # 在下发列表中表示出来
        string = ''
        for i in send_data2:
            string = string + str(i)
        self.open_close = string
        send_data2 = hex(int(string, 2))[2:].zfill(4)  # 二进制转十六进制
        data = send_data1 + send_data2 + send_data3
        data = binascii.a2b_hex(data)  # 十六进制转字节流
        self.conn.Send_data(data)

    def close_drawer(self):
        point = self.chose_drawer()
        time.sleep(0.3)  # 小睡300ms，给路灯反应时间
        send_data1 = 'FFFF0C'+'77'+'0103'  # 首
        send_data3 = '1E58FFF7'
        send_data2 = list(self.open_close)
        if point == 1:
            # data1='FFFF0C770103'+'0100'+'1E58FFF7'
            send_data2[7] = '0'
            self.ui.dr1.setStyleSheet("background-color:#008080;")
        elif point == 2:
            # data2='FFFF0C770103'+'0200'+'1E58FFF7'
            send_data2[6] = '0'
            self.ui.dr2.setStyleSheet("background-color:#008080;")
        elif point == 3:
            send_data2[5] = '0'
            self.ui.dr3.setStyleSheet("background-color:#008080;")
        elif point == 4:
            # data4 = 'FFFF0C770103' + '0800' + '1E58FFF7'
            send_data2[4] = '0'
            self.ui.dr4.setStyleSheet("background-color:#008080;")
        elif point == 5:
            # data5 = 'FFFF0C770103' + '1000' + '1E58FFF7'
            send_data2[3] = '0'
            self.ui.dr5.setStyleSheet("background-color:#008080;")
        elif point == 6:
            send_data2[2] = '0'
            self.ui.dr6.setStyleSheet("background-color:#008080;")
        elif point == 7:
            send_data2[1] = '0'
            self.ui.dr7.setStyleSheet("background-color:#008080;")
        elif point == 8:
            send_data2[0] = '0'
            self.ui.dr8.setStyleSheet("background-color:#008080;")
        elif point == 9:
            send_data2[15] = '0'
            self.ui.dr9.setStyleSheet("background-color:#008080;")
        elif point == 10:
            send_data2[14] = '0'
            self.ui.dr10.setStyleSheet("background-color:#008080;")
        else:
            pass
        string = ''
        for i in send_data2:
            string = string + str(i)
        self.open_close = string
        send_data2 = hex(int(string, 2))[2:].zfill(4)  # 二进制转十六进制
        data = send_data1 + send_data2 + send_data3
        data = binascii.a2b_hex(data)  # 十六进制转字节流
        self.conn.Send_data(data)

    def control_temp(self):
        control_zhen="FFFF0B"+'76'+"0102"+self.flag+"60C8FFF7"
        if(self.flag=='01'):
            self.ui.controller_state.setText(f'open')  # 在下发列表中表示出来
        else:
            self.ui.controller_state.setText(f'close')  # 在下发列表中表示出来

        control_zhen = binascii.a2b_hex(control_zhen)  # 十六进制转字节流
        self.conn.Send_data(control_zhen)
        self.change()


    def change(self):
        if self.flag=='01':
            self.flag='00'
        else:
            self.flag='01'
        return self.flag


    def set_controltemp(self):
        set = self.ui.set_temperature.text()
        set = int(re.sub("\D", "", set))
        if set>0:
            plus='0'
        else:
            plus='1'
        if set%1==0:
            dot='0'
        else:
            dot='1'
        set=bin(int(set))[2:].zfill(6)
        print(set)
        self.wendu=plus+set+dot
        print(self.wendu)
        self.wendu = hex(int(self.wendu, 2))[2:].zfill(2)  # 二进制转十六进制
        wendu_zhen="FFFF0B"+'78'+"0104"+ self.wendu+"8CC2FFF7"
        print(wendu_zhen)
        wendu_zhen = binascii.a2b_hex(wendu_zhen)  # 十六进制转字节流
        self.conn.Send_data(wendu_zhen)

    def text_signal(self, text):
        self.ui.drawer_state.setPlainText(self.conn.Recive_data(1))
# 加载设置参数界面
class sys_param:
    def __init__(self):
        qfile_Server = QFile("sys_parameter.ui")
        qfile_Server.open(QFile.ReadOnly)
        qfile_Server.close()
        # 从 UI 定义中动态 创建一个相应的窗口对象
        self.ui = QUiLoader().load(qfile_Server)
# 生成编码
class CRC:
    """循环冗余检验
    parameters
    ----------
    info : list
        需要被编码的信息
    crc_n : int, default: 32
        生成多项式的阶数
    p : list
        生成多项式
    q : list
        crc后得到的商
    check_code : list
        crc后得到的余数，即计算得到的校验码
    code : list
        最终的编码
    ----------
    """

    def __init__(self, info, crc_n=32):
        self.info = info
        '''
        输入参数：发送数据比特序列，CRC生成多项式阶数
        '''

        '''
        初始化CRC生成多项式p,其中P和二进制码（多项式比特序列）的关系为如下例：
        G(X)系数:  4 1 0 分别代表x的4次方，x的1次方，x的0次方以此类推
        G(X) =    1*(X^4) + 0*(X^3) + 0*(X^2) + 1*X + 1*1
        二进制码 = 1         0         0         1     1
        可根据需要自行添加修改，也可使用国际标准
        '''

        if crc_n == 8:
            loc = [8, 2, 1, 0]
        elif crc_n == 32:
            loc = [32, 26, 23, 22, 16, 12, 11, 10, 8, 7, 5, 2, 1, 0]  # 国际标准CRC-32
        elif crc_n == 16:
            loc = [16, 15, 2, 0]  # 国际标准CRC-16
        elif crc_n == 4:
            loc = [4, 3, 0]

        # 列表解析转换为多项式比特序列
        p = [0 for i in range(crc_n + 1)]
        for i in loc:
            p[i] = 1
        p = p[::-1]  # 逆序输出

        info = self.info.copy()
        times = len(info)
        n = crc_n + 1

        # 左移补零即乘积
        for i in range(crc_n):
            info.append(0)

        # 乘积除以多项式比特序列
        q = []  # 商
        for i in range(times):
            if info[i] == 1:  # 若乘积位为1，则商1，后逐位异或
                q.append(1)
                for j in range(n):  # n即p的位数
                    info[j + i] = info[j + i] ^ p[j]  # 按位异或
            else:  # 若乘积位是0，则商0，看下一位
                q.append(0)

        # 余数即为CRC编码
        check_code = info[-crc_n::]

        # 生成编码
        code = self.info.copy()
        for i in check_code:
            code.append(i)

        self.crc_n = crc_n
        self.p = p
        self.q = q
        self.check_code = check_code
        self.code = code

    def print_format(self):
        """格式化输出结果"""

        print('{:10}\t{}'.format('发送数据比特序列：', self.info))
        print('{:10}\t{}'.format('生成多项式比特序列：', self.p))
        print('{:15}\t{}'.format('商：', self.q))
        print('{:10}\t{}'.format('余数（即CRC校验码）：', self.check_code))
import numpy as np
# 设置系统参数
class jump:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.a = Status()
        self.a.ui.show()
        self.b = sys_param()
        self.a.ui.set_sys.clicked.connect(self.shift)
        self.b.ui.returnbutton.clicked.connect(self.retur)
        self.b.ui.ack.clicked.connect(self.ack)
        sys.exit(app.exec_())
     # 确认发送
    def ack(self):
        id = self.b.ui.id.text()
        id = int(re.sub("\D","", id))
        id = bin(int(id))[2:].zfill(40)
        id = hex(int(id, 2))[2:].zfill(10)  # 二进制转十六进制

        address=self.b.ui.address.text()
        address=int(re.sub("\D","",address))
        address = bin(int(address))[2:].zfill(8)
        address = hex(int(address, 2))[2:].zfill(2)  # 二进制转十六进制

        time = self.b.ui.time.text()
        time = int(re.sub("\D", "", time))

        time= bin(int(time))[2:].zfill(8)
        time = hex(int(time, 2))[2:].zfill(2)  # 二进制转十六进制

        delay=self.b.ui.delay.text()
        delay=int(re.sub("\D","",delay))

        delay= bin(int(delay))[2:].zfill(8)
        delay = hex(int(delay, 2))[2:].zfill(2)  # 二进制转十六进制

        con_temperature = self.b.ui.con_temperature.text()
        con_temperature = int(re.sub("\D", "", con_temperature))
        deviation=self.b.ui.deviation.text()
        deviation=int(re.sub("\D","",deviation))

        deviation= bin(int(deviation))[2:].zfill(8)
        deviation = hex(int(deviation, 2))[2:].zfill(2)  # 二进制转十六进制

        if con_temperature>0:
            plus='0'
        else:
            plus='1'
        if con_temperature%1==0:
            dot='0'
        else:
            dot='1'
        con_temperature = bin(int(con_temperature))[2:].zfill(6)
        con_temperature = plus + con_temperature + dot
        con_temperature = hex(int(con_temperature, 2))[2:].zfill(2)  # 二进制转十六进制
        sys_zhen = 'FFFF1C'+'75'+'7F05' + id+address+'00' + time + delay+ '0000' + con_temperature + deviation + 'FFFFFFFF00' + '36E8FFF7'
        sys_zhen = binascii.a2b_hex(sys_zhen)  # 十六进制转字节流
        self.a.conn.Send_data(sys_zhen)
    # 打开设置参数界面
    def shift(self):
        self.a.ui.close()
        self.b.ui.show()
    # 返回
    def retur(self):
        self.b.ui.close()
        self.a.ui.show()
Communication.Print_Used_Com()
Ret = False  # 是否创建成功标志
jump()
