import socket
import threading
import time
import datetime
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import *
from serverGUI import *

class MyWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        # 水平方向，表格大小拓展到适当的尺寸
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(["MAC", "PORT", "DATETIME"])
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget_2.setHorizontalHeaderLabels(["MAC", "PORT", "DATETIME"])

        self.__initUI()


    def __initUI(self):
        self.pushButton.clicked.connect(self.__button1Clicked)
        self.pushButton_2.clicked.connect(self.__button2Clicked)
        self.pushButton_3.clicked.connect(self.__button3Clicked)

    def __button1Clicked(self):
        #交换机启动
        myWin.listWidget.addItem("server1 start")
        server1.run()
        myWin.listWidget_2.addItem("server2 start")
        server2.run()
        #交换机连接,使用事先设定好的端口
        server1_to_server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server2_to_server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server1_to_server2.connect(("127.0.0.1", 9004))
        server2_to_server1.connect(("127.0.0.1", 9003))
        server1.send_sockets = server1_to_server2
        server2.send_sockets = server2_to_server1
        #t1 = threading.Thread(target=server1.link, args=(server1_to_server2, port))


    def __button2Clicked(self):
        #清空交换机1交换表
        self.clear_switch_table1()

    def __button3Clicked(self):
        #清空交换机2交换表
        self.clear_switch_table2()

    def update_switch_table1(self, data, method):
        #交换表1新增数据
        if method == "update":
            row = self.tableWidget.rowCount()
            for i in range(0, row):
                if self.tableWidget.item(i, 0).text() == data[0]:
                    self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(data[1]))
                    self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(data[2]))
                    break
        else:
            row = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(row + 1)
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(data[0]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(data[1]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(data[2]))
        QtWidgets.QApplication.processEvents()


    def clear_switch_table1(self):
        #清空交换表1
        self.tableWidget.clear()

    def update_switch_table2(self, data, method):
        #交换表2新增数据
        if method == "update":
            row = self.tableWidget_2.rowCount()
            for i in range(0, row):
                if self.tableWidget_2.item(i, 0).text() == data[0]:
                    self.tableWidget_2.setItem(i, 1, QtWidgets.QTableWidgetItem(data[1]))
                    self.tableWidget_2.setItem(i, 2, QtWidgets.QTableWidgetItem(data[2]))
                    break
        else:
            row = self.tableWidget_2.rowCount()
            self.tableWidget_2.setRowCount(row + 1)
            self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(data[0]))
            self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(data[1]))
            self.tableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(data[2]))
        QtWidgets.QApplication.processEvents()

    def clear_switch_table2(self):
        # 清空交换表2
        self.tableWidget_2.clear()

class Server():
    def __init__(self):
        #实例变量
        self.name = ""
        self.host = "127.0.0.1"
        self.switch_table = []  # 交换表
        self.sockets = []  # 所有连接
        self.send_sockets = None   #用于交换机间通信
        self.ports = []
        self.server_threads = []
        #self.history = []
        self.MAC = ""
        self.mutex = threading.Lock()

    def __isExist(self, info):
        mac_addr = info[0]
        is_exist = False
        if self.mutex.acquire():
            for item in self.switch_table:
                if item[0] == mac_addr:
                    is_exist = True
                    break
            self.mutex.release()
        return is_exist

    def __isExistDest(self, addr):
        # 目标地址已存在交换表中
        if self.mutex.acquire():
            for item in self.switch_table:
                if item[0] == addr:
                    self.mutex.release()
                    return True
            self.mutex.release()
        return False

    def __update(self, info):
        mac_addr = info[0]
        port = info[1]
        t = info[2]
        if self.name == "server1":
            myWin.update_switch_table1(info, method="update")
        elif self.name == "server2":
            myWin.update_switch_table2(info, method="update")
        if self.mutex.acquire():
            for item in self.switch_table:
                if item[0] == mac_addr:
                    item[1] = port
                    item[2] = t
                    break
            self.mutex.release()

    def __broadcast(self, frame, source_sock):
        for sock in self.sockets:
            if sock != source_sock and sock.getsockname()[-1] in self.ports:    # 向除本端口以外的所有端口转发
                if sock.getsockname()[-1] == 9003:                         #此端口与交换机2连接
                    server1.send_sockets.send(frame.encode())
                    myWin.listWidget.addItem("broadcast " + frame + " to port: 9003")
                    continue
                if sock.getsockname()[-1] == 9004:                         #此端口与交换机1连接
                    server2.send_sockets.send(frame.encode())
                    myWin.listWidget_2.addItem("broadcast " + frame + " to port: 9004")
                    continue
                sock.send(frame.encode())
                if self.name == "server1":
                    myWin.listWidget.addItem("broadcast " + frame +" to port: " + str(sock.getsockname()[-1]))
                elif self.name == "server2":
                    myWin.listWidget_2.addItem("broadcast " + frame +" to port: " + str(sock.getsockname()[-1]))

    def __forwarding(self, frame, addr, source_sock):
        for item in self.switch_table:
            if item[0] == addr:
                dest_port = item[1]
                for sock in self.sockets:
                    if sock.getsockname()[-1] == int(dest_port):
                        if source_sock == sock:            #源端口 == 目的端口, 过滤
                            if self.name == "server1":
                                myWin.listWidget.addItem(frame + "过滤")
                            elif self.name == "server2":
                                myWin.listWidget_2.addItem(frame + "过滤")
                            return
                        else:
                            if sock.getsockname()[-1] == 9003:
                                server1.send_sockets.send(frame.encode())
                                myWin.listWidget.addItem("send frame to" + addr + "through 9003")
                                return
                            if sock.getsockname()[-1] == 9004:
                                server2.send_sockets.send(frame.encode())
                                myWin.listWidget_2.addItem("send frame to" + addr + "through 9004")
                                return
                            sock.send(frame.encode())
                            if self.name == "server1":
                                myWin.listWidget.addItem("send frame to" + addr + "through" + item[1])
                            elif self.name == "server2":
                                myWin.listWidget_2.addItem("send frame to" + addr + "through" + item[1])
                            return

    def link(self, sock, port):
        #print("establish link", port)
        while True:
            data = sock.recv(1024)
            #print(data.decode())
            time.sleep(1)
            data = data.decode()
            u = data.split('|')
            #print("frame data : ", u[-1], "from", port)
            """
            if len(u) != 3:
                sock.send("frame error".encode())
                #self.history.append("frame error")
                if self.name == "server1":
                    myWin.listWidget.addItem("frame error")
                elif self.name == "server2":
                    myWin.listWidget_2.addItem("frame error")
                continue
            """
            source_addr = u[0]
            destination_addr = u[1]
            # 发送收到指令
            #sock.send("server receive : ".encode() + u[-1].encode())
            back = self.MAC + '|' + source_addr + '|' + "server received"
            sock.send(back.encode())
            # self.history.append("receive " + data)
            if self.name == "server1":
                myWin.listWidget.addItem("receive " + data)
            elif self.name == "server2":
                myWin.listWidget_2.addItem("receive " + data)

            # port = str(addr[1])
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  #转化为字符串
            new_info = [source_addr, str(port), t]
            if self.__isExist(new_info):  # 如果已经存在相关信息，则更新时间
                self.__update(new_info)
            else:
                if self.mutex.acquire():
                    self.switch_table.append(new_info)  # 如果不存在则新增
                    if self.name == "server1":
                        myWin.update_switch_table1(new_info, method="insert")
                    elif self.name == "server2":
                        myWin.update_switch_table2(new_info, method="insert")
                    self.mutex.release()

            if u[-1] == 'exit' or not len(data):  # 结束传输,关闭连接
                #print("end connect")
                break
            if self.__isExistDest(destination_addr):  # 点对点转发帧
                self.__forwarding(data, destination_addr, sock)
            else:
                self.__broadcast(data, sock)  # 广播帧

        sock.close()
        if self.mutex.acquire():
            self.sockets.remove(sock)  # 移除连接
            self.mutex.release()

    def __server(self, host, port):
        s = socket.socket()  # 创建socket连接对象
        s.bind((host, port))  # 绑定端口
        s.listen(5)  # 等待客户端连接
        while True:
            conn, address = s.accept()  # 接受一个连接
            if self.mutex.acquire():
                self.sockets.append(conn)
                self.mutex.release()
            t = threading.Thread(target=self.link, args=(conn, port))
            t.start()
        # s.close()

    def create(self, ports, name, MAC):
        self.name = name
        self.MAC = MAC
        for port in ports:
            thread =  threading.Thread(target=self.__server, args=(self.host, port))
            self.server_threads.append(thread)
            self.ports.append(port)

    def run(self):
        for thread in self.server_threads:
            thread.start()


server1 = Server()
server2 = Server()
#交换机1
server1_ports = [9000, 9001, 9002, 9003]
server1.create(server1_ports, "server1", "aa-aa-aa-aa-bb-bb-bb-bb")
#交换机2
server2_ports = [9004, 9005, 9006, 9007]
server2.create(server2_ports, "server2", "ee-ee-ee-ee-ff-ff-ff-ff")
app = QApplication(sys.argv)
myWin = MyWindow()

myWin.show()
sys.exit(app.exec_())