#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import hashlib
import time
import traceback
import requests
import datetime

HEART_BEAT = 5005
RECV_TXT_MSG = 1
RECV_PIC_MSG = 3
USER_LIST = 5000
GET_USER_LIST_SUCCSESS = 5001
GET_USER_LIST_FAIL = 5002
TXT_MSG = 555
PIC_MSG = 500
AT_MSG = 550
CHATROOM_MEMBER = 5010
CHATROOM_MEMBER_NICK = 5020
PERSONAL_INFO = 6500
DEBUG_SWITCH = 6000
PERSONAL_DETAIL = 6550
ATTATCH_FILE = 5003

LOG_LINE_NUM = 0
class WechatBot:
    def __init__(self, ip='127.0.0.1', port=5555):
        self.base_url = f'http://{ip}:{port}/'

    @staticmethod
    def get_id():
        return str(int(datetime.datetime.now().timestamp()))

    def send(self, uri, data):
        """
        通用发送函数，可能会失败，应在外层catch error
        """
        base_data = {
            'id': self.get_id(),
            'type': 'null',
            'roomid': 'null',
            'wxid': 'null',
            'content': 'null',
            'nickname': 'null',
            'ext': 'null',
        }
        base_data.update(data)
        url = f'{self.base_url}{uri}'
        res = requests.post(url, json={'para': base_data}, timeout=5)
        return res.json()

    def send_at_msg(self, wx_id, room_id, content, nickname):
        """
        发送at消息，at会写在最前面。@付好后的内容由nickname决定，但是是否真的收到at消息取决于wx_id
        :param wx_id:
        :param room_id:
        :param content:
        :param nickname:
        :return:
        """
        uri = 'api/sendatmsg'
        data = {
            'type': AT_MSG,
            'roomid': room_id,
            'content': content,
            'wxid': wx_id,
            'nickname': nickname
        }
        return self.send(uri, data)

    def send_pic(self, to, path):
        """
        发送图片
        :param to: roomid 或 wxid
        :param path: 绝对路径
        :return:
        """
        uri = 'api/sendpic'
        data = {
            'type': PIC_MSG,
            'wxid': to,
            'content': path
        }
        return self.send(uri, data)

    def get_memberid(self):
        """
        获取群成员id
        :return:
        """
        uri = 'api/getmemberid'
        data = {
            'type': CHATROOM_MEMBER,
            'content': 'op:list member'
        }
        return self.send(uri, data)

    def get_contact_list(self):
        """
        获取通讯录信息
        :return:
        """
        uri = 'api/getcontactlist'
        data = {
            'type': USER_LIST,
        }
        return self.send(uri, data)

    def get_member_nick(self, wx_id, room_id):
        """
        获取指定群的成员的昵称（可用于at）
        :param wx_id: 成员wx id
        :param room_id: 群id
        :return:
        """
        uri = 'api/getmembernick'
        data = {
            'type': CHATROOM_MEMBER_NICK,
            'wxid': wx_id,
            'roomid': room_id
        }
        return self.send(uri, data)

    def get_chatroom_member_list(self):
        """
        获取所有群的群友
        :return:
        """
        uri = 'api/get_charroom_member_list'
        data = {
            'type': CHATROOM_MEMBER,
        }
        return self.send(uri, data)

    def send_txt_msg(self, to, content):
        """
        发送文字消息
        :param to: roomid或wxid,必填
        :param content: 内容
        :return:
        """
        uri = 'api/sendtxtmsg'
        data = {
            'type': TXT_MSG,
            'wxid': to,
            'content': content
        }
        return self.send(uri, data)

    def send_attach(self, to, path):
        """
        发送本地文件
        :param to: roomid或wxid,必填
        :param path: 绝对路径
        :return:
        """
        uri = 'api/sendattatch'
        data = {
            'type': ATTATCH_FILE,
            'wxid': to,
            'content': path
        }
        return self.send(uri, data)

    def get_personal_info(self):
        """
        获取本人用户信息
        :return:
        """
        uri = 'api/get_personal_info'
        data = {
            'type': PERSONAL_INFO
        }
        return self.send(uri, data)


def getcontacts():
    wb = WechatBot()
    x= wb.get_contact_list()
    b =x['content']

    for i in b:
        print(i['name'])
        MY_GUI.write_log_to_Text(ZMJ_PORTAL,i['name'])


class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    #设置窗口
    def set_init_window(self):




    #功能函数



    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time


    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)



init_window = Tk()              #实例化出一个父窗口
ZMJ_PORTAL = MY_GUI(init_window)
# 设置根窗口默认属性
ZMJ_PORTAL.set_init_window()
init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示







def test():
    wb = WechatBot()
    print(wb.get_personal_info())
    print(wb.get_contact_list())
    # print(wb.send_pic(to='19255741868@chatroom', path='C:\\test.png'))
    # print(wb.send_attach(to='19255741868@chatroom', path='C:\\test.png'))
    # print(wb.send_txt_msg(to='19255741868@chatroom', content='测试一下普通文字消息'))
    # print(wb.send_at_msg(wx_id='ttc9082', room_id='19255741868@chatroom', content='测试一下at消息', nickname='随便写'))
    print('test done')



