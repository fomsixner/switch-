import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import *
from clientGUI import *
import socket
import time
import threading


ports = {"client1":9000, "client2":9001, "client3":9002, "client4":9005, "client5":9006, "client6":9007}       #设置端口
MAC = {"client1":"11-11-11-11-11-11-11-11", "client2":"22-22-22-22-22-22-22-22", "client3":"33-33-33-33-33-33-33-33",
       "client4":"44-44-44-44-44-44-44-44", "client5":"55-55-55-55-55-55-55-55", "client6":"66-66-66-66-66-66-66-66"}

class Client():
    def __init__(self):
        self.name = ""
        self.host = "127.0.0.1"
        self.connected = False
        self.port = 10000
        self.MAC = ""
        self.sock = None

    def create(self, MAC, port, name):
        # 创建
        self.name = name
        self.MAC = MAC
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        #建立连接
        return self.sock.connect_ex((self.host, self.port))

    def send(self, destination, data):
        #发送数据
        frame = self.MAC + '|' + destination + '|' + data
        self.sock.send(frame.encode())

    def receive(self):
        return self.sock.recv(1024)

    def close(self):
        #关闭连接
        self.sock.close()


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.__initUI()

    def __initUI(self):
        self.pushButton.clicked.connect(self.__button1Clicked)
        self.pushButton_2.clicked.connect(self.__button2Clicked)
        self.pushButton_3.clicked.connect(self.__button3Clicked)
        self.pushButton_4.clicked.connect(self.__button4Clicked)
        self.pushButton_5.clicked.connect(self.__button5Clicked)
        self.pushButton_6.clicked.connect(self.__button6Clicked)
        self.pushButton_7.clicked.connect(self.__button7Clicked)
        self.pushButton_8.clicked.connect(self.__button8Clicked)
        self.pushButton_9.clicked.connect(self.__button9Clicked)
        self.pushButton_10.clicked.connect(self.__button10Clicked)
        self.pushButton_11.clicked.connect(self.__button11Clicked)
        self.pushButton_12.clicked.connect(self.__button12Clicked)
        self.pushButton_13.clicked.connect(self.__button13Clicked)

    def __button1Clicked(self):
        #发送数据,在对应的窗口显示
        data = self.lineEdit.text()
        c1 = self.comboBox.currentText()
        c2 = self.comboBox_2.currentText()
        if c1 == 'client1':
            client1.send(MAC[c2], data)
            self.listWidget.addItem("send " + data + " to " + MAC[c2])
        elif c1 == 'client2':
            client2.send(MAC[c2], data)
            self.listWidget_2.addItem("send " + data + " to " + MAC[c2])
        elif c1 == 'client3':
            client3.send(MAC[c2], data)
            self.listWidget_3.addItem("send " + data + " to " + MAC[c2])
        elif c1 == 'client4':
            client4.send(MAC[c2], data)
            self.listWidget_4.addItem("send " + data + " to " + MAC[c2])
        elif c1 == 'client5':
            client5.send(MAC[c2], data)
            self.listWidget_5.addItem("send " + data + " to " + MAC[c2])
        elif c1 == 'client6':
            client6.send(MAC[c2], data)
            self.listWidget_6.addItem("send " + data + " to " + MAC[c2])


    def __button2Clicked(self):
        #client1 连接
        if client1.connect() == 0:
            client1.connected = True
            self.listWidget.addItem("连接成功 端口:" + str(client1.port))
        else:
            self.listWidget.addItem("连接失败")

    def __button3Clicked(self):
        #client2 连接
        if client2.connect() == 0:
            client2.connected = True
            self.listWidget_2.addItem("连接成功 端口:" + str(client2.port))
        else:
            self.listWidget_2.addItem("连接失败")

    def __button4Clicked(self):
        #client3 连接
        if client3.connect() == 0:
            client3.connected = True
            self.listWidget_3.addItem("连接成功 端口:" + str(client3.port))
        else:
            self.listWidget_3.addItem("连接失败")

    def __button5Clicked(self):
        #client4 连接
        if client4.connect() == 0:
            client4.connected = True
            self.listWidget_4.addItem("连接成功 端口:" + str(client4.port))
        else:
            self.listWidget_4.addItem("连接失败")

    def __button6Clicked(self):
        #client5 连接
        if client5.connect() == 0:
            client5.connected = True
            self.listWidget_5.addItem("连接成功 端口:" + str(client5.port))
        else:
            self.listWidget_5.addItem("连接失败")

    def __button7Clicked(self):
        #client6 连接
        if client6.connect() == 0:
            client6.connected = True
            self.listWidget_6.addItem("连接成功 端口:" + str(client6.port))
        else:
            self.listWidget_6.addItem("连接失败")

    def __button8Clicked(self):
        #client1 断开
        if client1.connected:
            client1.close()
            client1.connected = False
            self.listWidget.addItem("断开")

    def __button9Clicked(self):
        #client2 断开
        if client2.connected:
            client2.close()
            client2.connected = False
            self.listWidget_2.addItem("断开")

    def __button10Clicked(self):
        #client3 断开
        if client3.connected:
            client3.close()
            client3.connected = False
            self.listWidget_3.addItem("断开")

    def __button11Clicked(self):
        #client4 断开
        if client4.connected:
            client4.close()
            client4.connected = False
            self.listWidget_4.addItem("断开")

    def __button12Clicked(self):
        #client5 断开
        if client5.connected:
            client5.close()
            client5.connected = False
            self.listWidget_5.addItem("断开")

    def __button13Clicked(self):
        #client6 断开
        if client6.connected:
            client6.close()
            client6.connected = False
            self.listWidget_6.addItem("断开")


def client1receive():
    #print(client1.port)
    #print(client1.sock)
    while True:
        if client1.connected:
            data = client1.receive()
            if MAC["client1"] == data.decode().split('|')[1]:
                #print("client1 receive : ", data.decode())
                myWin.listWidget.addItem("receive : " + data.decode().split('|')[-1])

def client2receive():
    #print(client2.port)
    while True:
        if client2.connected:
            data = client2.receive()
            if MAC["client2"] == data.decode().split('|')[1]:
                #print("client2 receive : ", data.decode())
                myWin.listWidget_2.addItem("receive : " + data.decode().split('|')[-1])

def client3receive():
    while True:
        if client3.connected:
            data = client3.receive()
            if MAC["client3"] == data.decode().split('|')[1]:
                myWin.listWidget_3.addItem("receive : " + data.decode().split('|')[-1])

def client4receive():
    while True:
        if client4.connected:
            data = client4.receive()
            if MAC["client4"] == data.decode().split('|')[1]:
                myWin.listWidget_4.addItem("receive : " + data.decode().split('|')[-1])

def client5receive():
    while True:
        if client5.connected:
            data = client5.receive()
            if MAC["client5"] == data.decode().split('|')[1]:
                myWin.listWidget_5.addItem("receive : " + data.decode().split('|')[-1])

def client6receive():
    while True:
        if client6.connected:
            data = client6.receive()
            if MAC["client6"] == data.decode().split('|')[1]:
                myWin.listWidget_6.addItem("receive : " + data.decode().split('|')[-1])


app = QApplication(sys.argv)
myWin = MyWindow()

client1 = Client()
client2 = Client()
client3 = Client()
client4 = Client()
client5 = Client()
client6 = Client()

client1.create(MAC["client1"], ports["client1"], "client1")
client2.create(MAC["client2"], ports["client2"], "client2")
client3.create(MAC["client3"], ports["client3"], "client3")
client4.create(MAC["client4"], ports["client4"], "client4")
client5.create(MAC["client5"], ports["client5"], "client5")
client6.create(MAC["client6"], ports["client6"], "client6")
#接受消息
thread1 = threading.Thread(target=client1receive)
thread2 = threading.Thread(target=client2receive)
thread3 = threading.Thread(target=client3receive)
thread4 = threading.Thread(target=client4receive)
thread5 = threading.Thread(target=client5receive)
thread6 = threading.Thread(target=client6receive)
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()


myWin.show()
sys.exit(app.exec_())
