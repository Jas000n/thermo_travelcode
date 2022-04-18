

import socket
from time import sleep  # 导入 socket 模块
import cv2
import numpy as np


def send_image(img, type):
    '''
    type:1表示发送行程卡 2表示发送健康码
    '''
    img = cv2.resize(img, (640, 640))
    client = socket.socket()  # 创建 socket 对象
    host = socket.gethostname()  # 获取本地主机名
    port = 11111  # 设置端口号
    print('开始连接')
    client.connect(('192.168.142.206', port))
    print('开始传输')

    if type == 1:
        client.send(b'trac')

    elif type == 2:
        client.send(b'yolo')

    send_bytes = b''
    send_num = 0
    send_bytes += img.data

    while send_num < img.shape[0] * img.shape[1] * img.shape[2]:
        send_num += client.send(send_bytes[send_num:])
        print(send_num)
    print('开始接受')
    rec = client.recv(3)
    client.close()
    '''
    这个地方使用-20表示红-30表示黄-40表示绿
    返回的时候对应返回1，2，3
    '''
    if rec == b'-10':
        return -1
    if rec == b'-20':
        return 0
    if rec == b'-30':
        return 1
    if rec == b'-40':
        return 2
    else:

        return float(rec) / 1000



