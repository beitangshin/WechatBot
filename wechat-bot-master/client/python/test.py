from tkinter import *
import hashlib
import time
import traceback
import requests
import datetime
import pandas
import threading
import queue
import json
import requests
import websocket
import re
import json


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







class WechatBotMessageServer:
    def __init__(self, ip='127.0.0.1', port=5555, url='https://127.0.0.1:8888/wechat/msg/receiver/'):
        self.ws_url = f'ws://{ip}:{port}'
        self.url = url

    def start(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(
            self.ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        ws.run_forever()

    def on_open(self, ws):
        print(f'{self.ws_url} opened successfully.')

    def on_message(self, ws, message):
        print(message)
        localtime = time.asctime(time.localtime(time.time()))
        print(localtime)
        messagebox.clear()
        messagebox.update(eval(message))
        res = requests.post(self.url, json=json.loads(message))

        #print(f'resp: {res.json()}')

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print(f'{self.ws_url} closed gracefully.')




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








class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name

    def set_init_window(self):

        self.activekeys = [ ]
        self.monitor_names =monitor_name
        self.monitor_groups =monitor_group
        self.init_window_name.title("WechatBot")
        self.init_window_name.geometry('1068x681+10+10')



        self.Contacts = []
        self.GroupContacts = []
        #GetContacts button setting
        self.getcontactsbutton = Button(self.init_window_name, text="获取联系人", bg="lightblue", width=10,command=self.getcontacts)
        self.getcontactsbutton.grid(row=20, column=0)
        #startmonitor button seeting

        # self.getcontactsbutton = Button(self.init_window_name, text="开启机器人", bg="lightblue", width=10,command=self.startmonitor)
        # self.getcontactsbutton.grid(row=51, column=30)


        #scrollbar contacts setting
        self.ContactScrollbar = Scrollbar(self.init_window_name,)
        #self.ContactScrollbar.pack(side="right",fill= "y")
        self.ContactScrollbar.grid(row=1, column=1)

        #scrollbar groupcontacts setting
        self.GroupContactScrollbar = Scrollbar(self.init_window_name)
        #self.GroupContactScrollbar.pack(side="right",fill= "y")
        self.GroupContactScrollbar.grid(row=3,column=1)



        #group listboxcontacts
        self.GroupContactsBox = Listbox(self.init_window_name, yscrollcommand = self.GroupContactScrollbar.set)
        for i in self.GroupContacts:
            self.GroupContactsBox.insert("end",i)
        self.GroupContactsBox.grid(row=3, column=0)
        self.GroupContactScrollbar.config(command=self.GroupContactsBox.yview)

        #listboxcontacts
        self.ContactsBox = Listbox(self.init_window_name, yscrollcommand = self.ContactScrollbar.set)
        for i in self.Contacts:
            self.ContactsBox.insert("end",i)
        self.ContactsBox.grid(row=1, column=0)
        self.ContactScrollbar.config(command=self.ContactsBox.yview)

        ###################设计监视框#########################################
        self.contactslabel = Label(self.init_window_name, text="个人号")
        self.contactslabel.grid(row=0, column=0)
        self.groupslabel = Label(self.init_window_name, text="群号")
        self.groupslabel.grid(row=2, column=0)

        ###################设计监视框#########################################
        self.person_name = Label(self.init_window_name, text="联系人")
        self.person_name.grid(row=0, column=4)
        self.person_nameBox = Listbox(self.init_window_name)
        self.person_nameBox.grid(row=1, column=4)

        self.person_keywords = Label(self.init_window_name, text="关键词")
        self.person_keywords.grid(row=0, column=5)
        self.person_keywordsBox = Listbox(self.init_window_name)
        self.person_keywordsBox.grid(row=1, column=5)

        self.person_reply = Label(self.init_window_name, text="回复")
        self.person_reply.grid(row=0, column=6)
        self.person_replyBox = Listbox(self.init_window_name)
        self.person_replyBox.grid(row=1, column=6)

        ###################设计监视框群聊#########################################
        self.group_name = Label(self.init_window_name, text="群名")
        self.group_name.grid(row=2, column=3)
        self.group_nameBox = Listbox(self.init_window_name)
        self.group_nameBox.grid(row=3, column=3)

        self.group_membername = Label(self.init_window_name, text="群员名")
        self.group_membername.grid(row=2, column=4)
        self.group_membernameBox = Listbox(self.init_window_name)
        self.group_membernameBox.grid(row=3, column=4)

        self.group_keyword = Label(self.init_window_name, text="回复")
        self.group_keyword.grid(row=2, column=5)
        self.group_keywordBox = Listbox(self.init_window_name)
        self.group_keywordBox.grid(row=3, column=5)

        self.group_reply = Label(self.init_window_name, text="回复")
        self.group_reply.grid(row=2, column=6)
        self.group_replyBox = Listbox(self.init_window_name)
        self.group_replyBox.grid(row=3, column=6)

    def close_update_mainpage(self):

#########cleanall###############################
        self.group_nameBox.delete(0,END)
        self.group_nameBox.grid(row=3, column=3)
        self.group_keywordBox.delete(0,END)
        self.group_keywordBox.grid(row=3, column=5)
        self.group_replyBox.delete(0,END)
        self.group_replyBox.grid(row=3, column=6)
        self.person_nameBox.delete(0,END)
        self.person_nameBox.grid(row=1, column=4)
        self.person_keywordsBox.delete(0,END)
        self.person_keywordsBox.grid(row=1, column=5)
        self.person_replyBox.delete(0,END)
        self.person_replyBox.grid(row=1, column=6)

######################更新单个联系人##########
        for i in monitor_name:
            for ii in i.keys():

                for iii in i[ii].keys():

                    a =i[ii]
                    self.person_nameBox.insert('end',ii)
                    self.person_nameBox.grid(row=1, column=4)
                    self.person_keywordsBox.insert('end',iii)
                    self.person_keywordsBox.grid(row=1, column=5)
                    self.person_replyBox.insert('end',a[iii])
                    self.person_replyBox.grid(row=1, column=6)

#################################更新监视框群聊#########################################
        for i in monitor_group:
            print(i)
            for ii in i.keys():
                print(ii)
                for iii in i[ii].keys():
                    print(iii)
                    a = i[ii]
                    self.group_nameBox.insert('end', ii)
                    self.group_nameBox.grid(row=3, column=3)
                    self.group_keywordBox.insert('end', iii)
                    self.group_keywordBox.grid(row=3, column=5)
                    self.group_replyBox.insert('end', a[iii])
                    self.group_replyBox.grid(row=3, column=6)



        self.ListBoxNewWindow.destroy()

    def getcontacts(self):

        self.wb = WechatBot()
        x = self.wb.get_contact_list()

        b= x['content']

        self.GroupContacts =[]
        self.Contacts = []
#打印联系人
        for i in b:
            if i['wxid'].find('@chatroom') > 0 :

                self.GroupContacts.append(i['name'])
                contactsbook.update({i['name']:i['wxid']})

            else:

                self.Contacts.append(i['name'])
                contactsbook.update({i['name']: i['wxid']})

        for i in self.GroupContacts:
            self.GroupContactsBox.insert("end",i)
            self.GroupContactScrollbar.grid(row=13, column=0)
            self.GroupContactScrollbar.config(command=self.GroupContactsBox.yview)
            self.GroupContactScrollbar.grid(row=13, column=1,ipady=65)
            self.GroupContactsBox.bind('<Double-Button-1>',self.listboxclickGroup)
        for i in self.Contacts:
            self.ContactsBox.insert("end",i)
            self.ContactsBox.grid(row=1, column=0)
            self.ContactScrollbar.config(command=self.ContactsBox.yview)
            self.ContactScrollbar.grid(row=1, column=1,ipady=65)
            self.ContactsBox.bind('<Double-Button-1>',self.listboxclick)



    def getgroupcontacts(self):

        #@#####newwidonw
        currentgroupnames = self.GroupContactsBox.get(self.ListBoxNewWindow.selectname[0])
        currentgroupwxid = contactsbook[currentgroupnames]
        groupmembers = self.wb.get_memberid()
        currentgroupmembers = []
        temp = groupmembers['content']
        for i in temp :
            if i['room_id'] == currentgroupwxid:
                currentgroupmembers = i['member']

        # #显示群成员
        # ListBoxNewWindow.ListBoxNewWindow_qroupmem = Label(ListBoxNewWindow,text = "群成员")
        # ListBoxNewWindow.ListBoxNewWindow_qroupmem.grid(row= 0, column =20)
        # ListBoxNewWindow.ListBoxNewWindow_qroupmemBox = Listbox(ListBoxNewWindow)
        # ListBoxNewWindow.ListBoxNewWindow_qroupmemBox.grid(row=1,column=20,rowspan =10)


        self.ListBoxNewWindow.ListBoxNewWindow_qroupmemBox.grid(row=1,column=1)
        self.ListBoxNewWindow.GroupcontactsScrollbar = Scrollbar(self.ListBoxNewWindow)
        self.ListBoxNewWindow.GroupcontactsScrollbar.grid(row=1, column=10)
        self.ListBoxNewWindow.GroupcontactsScrollbar.config(command=self.ListBoxNewWindow.ListBoxNewWindow_qroupmemBox.yview)
        for ii in currentgroupmembers:
            nickname = self.wb.get_member_nick(ii,currentgroupwxid)
            xx = nickname['content']
            yy = json.loads(xx)
            self.ListBoxNewWindow.ListBoxNewWindow_qroupmemBox.insert("end",yy['nick'])
            self.ListBoxNewWindow.ListBoxNewWindow_qroupmemBox.grid(row=1, column=20,rowspan = 10)
            self.ListBoxNewWindow.GroupcontactsScrollbar.config(command=self.ListBoxNewWindow.ListBoxNewWindow_qroupmemBox.yview)
            self.ListBoxNewWindow.GroupcontactsScrollbar.grid(row=1,column=30,ipady=50,rowspan = 10)
            self.ListBoxNewWindow.ListBoxNewWindow_qroupmemBox.bind('<Double-Button-1>',self.getgroupmemb)







    def confirmbuttonGroup(self):

    ##########listbox里的名字###################################################
        temp1 = self.ListBoxNewWindow.ListBoxNewWindow_qroupmemBox.curselection()
        name = self.ListBoxNewWindow.ListBoxNewWindow_qroupmemBox.get(temp1[0])


        keywords = self.newwindow.ListBoxNewWindow_guizeinput.get()
        reply =self.newwindow.ListBoxNewWindow_replyinput.get()
        group_name = name + '-' + self.Group_name


        inflag = False
        index = -1
        outlistjiance =[]
        outlistreply=[]
        outlistname=[]

#################在monitorlist#############

        for i in self.monitor_groups:
            if group_name in i.keys():
                inflag =True
                index = self.monitor_groups.index(i)

#####################没在monitorlist里#############
        if not inflag  :
            tempdic = {group_name:{keywords:reply}}
            self.monitor_groups.append(tempdic)

        else:
            if keywords not in (self.monitor_groups[index])[group_name].keys():
                tempdic = {keywords: reply}
                (self.monitor_groups[index])[group_name].update(tempdic)
            else:
                print("do nothing because keywords repeat")





        #更新信息框
        for iiii in self.monitor_groups:
            print(iiii)
            for i in iiii.keys():
                print(i)

                for iii in iiii[i]:
                    print(iii)
                    a = iiii[i]
                    outlistjiance.append(iii)
                    outlistreply.append(a[iii])
                    outlistname.append(i)
        self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.delete(0,END)
        self.ListBoxNewWindow.ListBoxNewWindow_huifuBox.delete(0,END)
        self.ListBoxNewWindow.ListBoxNewWindow_memberBox.delete(0,END)

        for x in outlistjiance:
            self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.insert("end", x)
        for x in outlistreply:
            self.ListBoxNewWindow.ListBoxNewWindow_huifuBox.insert("end",x)
        for x in outlistname:
            self.ListBoxNewWindow.ListBoxNewWindow_memberBox.insert("end",x)
        monitor_group =self.monitor_groups


    def confirmbutton(self):

        keywords = self.ListBoxNewWindow.ListBoxNewWindow_guizeinput.get()
        reply =self.ListBoxNewWindow.ListBoxNewWindow_replyinput.get()
        name = self.ContactsBox.get(self.ListBoxNewWindow.selectname[0])
        inflag = False
        index = -1
        outlistjiance =[]
        outlistreply=[]



        for i in self.monitor_names:
            if name in i.keys():
                inflag =True
                index = self.monitor_names.index(i)


        if not inflag  :
            tempdic = {name:{keywords:reply}}
            self.monitor_names.append(tempdic)

            #更新信息窗口



        else:
            if keywords not in (self.monitor_names[index])[name].keys():
                tempdic = {keywords: reply}
                (self.monitor_names[index])[name].update(tempdic)
            else:
                print("do nothing because keywords repeat")





        #更新信息框

        for iii in self.monitor_names:
            if name in iii.keys():
                index = self.monitor_names.index(iii)
        for ii in (self.monitor_names[index])[name].keys():
            outlistjiance.append(ii)
            outlistreply.append(((self.monitor_names[index])[name])[ii])


        self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.delete(0,END)
        self.ListBoxNewWindow.ListBoxNewWindow_huifuBox.delete(0,END)
        for x in outlistjiance:
            self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.insert("end", x)
        for x in outlistreply:
            self.ListBoxNewWindow.ListBoxNewWindow_huifuBox.insert("end",x)
        monitor_name = self.monitor_names


    def cancelbutton(self):
        self.ListBoxNewWindow.destroy()
    def cancelbutton_group(self):
        self.newwindow.destroy()

        self.ListBoxNewWindow.destroy()
    def deletebutton(self):

        try:
            name = self.ContactsBox.get(self.ListBoxNewWindow.selectname[0])
            keyword = self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.curselection()
            keywords = self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.get(keyword[0])
            print(keywords)
            outlistjiance = []
            outlistreply = []
            for iii in self.monitor_names:
                if name in iii.keys():
                    index = self.monitor_names.index(iii)
            # 按keywords删除行
            temp = self.monitor_names[index]
            del ((temp[name])[keywords])
            for ii in (self.monitor_names[index])[name].keys():
                outlistjiance.append(ii)
                outlistreply.append(((self.monitor_names[index])[name])[ii])
            self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.delete(0, END)
            self.ListBoxNewWindow.ListBoxNewWindow_huifuBox.delete(0, END)
            for x in outlistjiance:
                self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.insert("end", x)
            for x in outlistreply:
                self.ListBoxNewWindow.ListBoxNewWindow_huifuBox.insert("end", x)
            print("delete", name)

        except IndexError:
            print("Empty buffer")
        else:
            print("normal")



    def deletebuttongroup(self):

        try:
            name = self.GroupContactsBox.get(self.ListBoxNewWindow.selectname[0])
            keyword = self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.curselection()
            keywords =self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.get(keyword[0])
            print(keywords)
            outlistjiance=[]
            outlistreply=[]
            for iii in self.monitor_names:
                if name in iii.keys():
                    index = self.monitor_names.index(iii)
            #按keywords删除行
            temp = self.monitor_names[index]
            del (( temp[name])[keywords])
            for ii in (self.monitor_names[index])[name].keys():
                outlistjiance.append(ii)
                outlistreply.append(((self.monitor_names[index])[name])[ii])
            self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.delete(0,END)
            self.ListBoxNewWindow.ListBoxNewWindow_huifuBox.delete(0,END)
            for x in outlistjiance:
                self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.insert("end", x)
            for x in outlistreply:
                self.ListBoxNewWindow.ListBoxNewWindow_huifuBox.insert("end",x)
            print("delete",name)
        except IndexError:
            print("Empty buffer")
        else:
            print("normal")



    def listboxclickGroup(self,event):

        #print( 'clicked at:', event)#打印出该事件（按下鼠标）的x，y轴
        index =-1
        outlistjiance =[]
        outlistreply=[]
        outlistname = []
        self.ListBoxNewWindow = Toplevel(self.init_window_name)
        self.ListBoxNewWindow.protocol('WM_DELETE_WINDOW',self.close_update_mainpage)
        self.ListBoxNewWindow.selectname = self.GroupContactsBox.curselection()

        self.Group_name= self.GroupContactsBox.get(self.ListBoxNewWindow.selectname[0])
        # ListBoxNewWindow.title("设置规则")
        # ListBoxNewWindow.ListBoxNewWindow_Title1 = Label(ListBoxNewWindow, text="请输入规则")
        # ListBoxNewWindow.ListBoxNewWindow_Title1.grid(row = 0,column=0)
        #
        # #shu ru zu
        # ListBoxNewWindow.ListBoxNewWindow_guizeinput = Entry(ListBoxNewWindow)
        # ListBoxNewWindow.ListBoxNewWindow_guizeinput.grid(row =1, column =3)
        # ListBoxNewWindow.ListBoxNewWindow_guize = Label(ListBoxNewWindow, text="关键字")
        # ListBoxNewWindow.ListBoxNewWindow_guize.grid(row =1,column =0)
        #
        #
        # ListBoxNewWindow.ListBoxNewWindow_reply = Label(ListBoxNewWindow, text="回复")
        # ListBoxNewWindow.ListBoxNewWindow_reply.grid(row = 2,column =0)
        # ListBoxNewWindow.ListBoxNewWindow_replyinput = Entry(ListBoxNewWindow)
        # ListBoxNewWindow.ListBoxNewWindow_replyinput.grid(row =2, column =3)

        # #确认按钮
        # ListBoxNewWindow.ListBoxNewWindow_confirm_button = Button(ListBoxNewWindow,text="确认", bg="lightblue", width=10,command=lambda :self.confirmbuttonGroup(ListBoxNewWindow))
        # ListBoxNewWindow.ListBoxNewWindow_confirm_button.grid(row = 3, column = 0)
        #
        #
        # #取消按钮
        # self.ListBoxNewWindow.ListBoxNewWindow_cancel_button = Button(self.ListBoxNewWindow,text="取消", bg="lightblue", width=10,command=lambda :self.cancelbutton())
        # self.ListBoxNewWindow.ListBoxNewWindow_cancel_button.grid(row = 3, column = 3)
        # #删除按钮
        # ListBoxNewWindow.ListBoxNewWindow_delete_button = Button(ListBoxNewWindow,text="删除", bg="lightblue", width=10,command=lambda :self.deletebuttongroup(ListBoxNewWindow))
        # ListBoxNewWindow.ListBoxNewWindow_delete_button.grid(row = 3, column =5)

        #获取群成员id并显示
        self.ListBoxNewWindow.ListBoxNewWindow_delete_button = Button(self.ListBoxNewWindow,text="群成员", bg="lightblue", width=10,command=lambda :self.getgroupcontacts())
        self.ListBoxNewWindow.ListBoxNewWindow_delete_button.grid(row = 3, column =7)


        #显示检测和回复内容
        self.ListBoxNewWindow.ListBoxNewWindow_jiance = Label(self.ListBoxNewWindow,text = "检测")
        self.ListBoxNewWindow.ListBoxNewWindow_jiance.grid(row= 0, column =10)
        self.ListBoxNewWindow.ListBoxNewWindow_jianceBox = Listbox(self.ListBoxNewWindow)
        self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.grid(row=1,column=10,rowspan =10)

        self.ListBoxNewWindow.ListBoxNewWindow_huifu = Label(self.ListBoxNewWindow,text = "回复")
        self.ListBoxNewWindow.ListBoxNewWindow_huifu.grid(row= 0, column =15)
        self.ListBoxNewWindow.ListBoxNewWindow_huifuBox = Listbox(self.ListBoxNewWindow)
        self.ListBoxNewWindow.ListBoxNewWindow_huifuBox.grid(row=1,column=15,rowspan =10)


        #显示群成员
        self.ListBoxNewWindow.ListBoxNewWindow_qroupmem = Label(self.ListBoxNewWindow,text = "群成员")
        self.ListBoxNewWindow.ListBoxNewWindow_qroupmem.grid(row= 0, column =20)
        self.ListBoxNewWindow.ListBoxNewWindow_qroupmemBox = Listbox(self.ListBoxNewWindow)
        self.ListBoxNewWindow.ListBoxNewWindow_qroupmemBox.grid(row=1,column=20,rowspan =10)



        #群员名字

        self.ListBoxNewWindow.ListBoxNewWindow_member = Label(self.ListBoxNewWindow,text = "jiance群成员")
        self.ListBoxNewWindow.ListBoxNewWindow_member.grid(row= 0, column =9)
        self.ListBoxNewWindow.ListBoxNewWindow_memberBox = Listbox(self.ListBoxNewWindow)
        self.ListBoxNewWindow.ListBoxNewWindow_memberBox.grid(row=1,column=9,rowspan =10)





    def getgroupmemb(self,event):

        self.newwindow = Toplevel(self.init_window_name)



        self.newwindow.title("设置规则")
        self.newwindow.ListBoxNewWindow_Title1 = Label(self.newwindow, text="请输入规则")
        self.newwindow.ListBoxNewWindow_Title1.grid(row = 0,column=0)

        #shu ru zu
        self.newwindow.ListBoxNewWindow_guizeinput = Entry(self.newwindow)
        self.newwindow.ListBoxNewWindow_guizeinput.grid(row =1, column =3)
        self.newwindow.ListBoxNewWindow_guize = Label(self.newwindow, text="关键字")
        self.newwindow.ListBoxNewWindow_guize.grid(row =1,column =0)


        self.newwindow.ListBoxNewWindow_reply = Label(self.newwindow, text="回复")
        self.newwindow.ListBoxNewWindow_reply.grid(row = 2,column =0)
        self.newwindow.ListBoxNewWindow_replyinput = Entry(self.newwindow)
        self.newwindow.ListBoxNewWindow_replyinput.grid(row =2, column =3)

        #确认按钮
        self.newwindow.ListBoxNewWindow_confirm_button = Button(self.newwindow,text="确认", bg="lightblue", width=10,command=lambda :self.confirmbuttonGroup())
        self.newwindow.ListBoxNewWindow_confirm_button.grid(row = 3, column = 0)


        # #取消按钮
        # self.newwindow.ListBoxNewWindow_cancel_button = Button(self.newwindow,text="取消", bg="lightblue", width=10,command=lambda :self.cancelbutton_group())
        # self.newwindow.ListBoxNewWindow_cancel_button.grid(row = 3, column = 3)
        #删除按钮
        self.newwindow.ListBoxNewWindow_delete_button = Button(self.newwindow,text="删除", bg="lightblue", width=10,command=lambda :self.deletebuttongroup())
        self.newwindow.ListBoxNewWindow_delete_button.grid(row = 3, column =5)

        #self.groupmembselect =  window.ListBoxNewWindow_qroupmemBox.curselection()
        print('wo haole')

    def listboxclick(self,event):


        index =-1
        outlistjiance =[]
        outlistreply=[]

        self.ListBoxNewWindow = Toplevel(self.init_window_name)
        self.ListBoxNewWindow.selectname = self.ContactsBox.curselection()
        self.ListBoxNewWindow.protocol('WM_DELETE_WINDOW',self.close_update_mainpage)
        name= self.ContactsBox.get(self.ListBoxNewWindow.selectname[0])




        self.ListBoxNewWindow.title("设置规则")
        self.ListBoxNewWindow.ListBoxNewWindow_Title1 = Label(self.ListBoxNewWindow, text="请输入规则")
        self.ListBoxNewWindow.ListBoxNewWindow_Title1.grid(row = 0,column=0)

        #shu ru zu
        self.ListBoxNewWindow.ListBoxNewWindow_guizeinput = Entry(self.ListBoxNewWindow)
        self.ListBoxNewWindow.ListBoxNewWindow_guizeinput.grid(row =1, column =3)
        self.ListBoxNewWindow.ListBoxNewWindow_guize = Label(self.ListBoxNewWindow, text="关键字")
        self.ListBoxNewWindow.ListBoxNewWindow_guize.grid(row =1,column =0)


        self.ListBoxNewWindow.ListBoxNewWindow_reply = Label(self.ListBoxNewWindow, text="回复")
        self.ListBoxNewWindow.ListBoxNewWindow_reply.grid(row = 2,column =0)
        self.ListBoxNewWindow.ListBoxNewWindow_replyinput = Entry(self.ListBoxNewWindow)
        self.ListBoxNewWindow.ListBoxNewWindow_replyinput.grid(row =2, column =3)

        #确认按钮
        self.ListBoxNewWindow.ListBoxNewWindow_confirm_button = Button(self.ListBoxNewWindow,text="确认", bg="lightblue", width=10,command=lambda :self.confirmbutton())
        self.ListBoxNewWindow.ListBoxNewWindow_confirm_button.grid(row = 3, column = 0)


        # #取消按钮
        # self.ListBoxNewWindow.ListBoxNewWindow_cancel_button = Button(self.ListBoxNewWindow,text="取消", bg="lightblue", width=10,command=lambda :self.cancelbutton())
        # self.ListBoxNewWindow.ListBoxNewWindow_cancel_button.grid(row = 3, column = 3)
        #删除按钮
        self.ListBoxNewWindow.ListBoxNewWindow_delete_button = Button(self.ListBoxNewWindow,text="删除", bg="lightblue", width=10,command=lambda :self.deletebutton())
        self.ListBoxNewWindow.ListBoxNewWindow_delete_button.grid(row = 3, column =5)

        #显示检测和回复内容
        self.ListBoxNewWindow.ListBoxNewWindow_jiance = Label(self.ListBoxNewWindow,text = "检测")
        self.ListBoxNewWindow.ListBoxNewWindow_jiance.grid(row= 0, column =10)
        self.ListBoxNewWindow.ListBoxNewWindow_jianceBox = Listbox(self.ListBoxNewWindow)
        self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.grid(row=1,column=10,rowspan =10)

        self.ListBoxNewWindow.ListBoxNewWindow_huifu = Label(self.ListBoxNewWindow,text = "回复")
        self.ListBoxNewWindow.ListBoxNewWindow_huifu.grid(row= 0, column =15)
        self.ListBoxNewWindow.ListBoxNewWindow_huifuBox = Listbox(self.ListBoxNewWindow)
        self.ListBoxNewWindow.ListBoxNewWindow_huifuBox.grid(row=1,column=15,rowspan =10)

        # 更新信息框
        for iii in self.monitor_names:
            if name in iii.keys():
                index = self.monitor_names.index(iii)
        if index >=0 :
            for ii in (self.monitor_names[index])[name].keys():
                outlistjiance.append(ii)
                outlistreply.append(((self.monitor_names[index])[name])[ii])

        self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.delete(0,END)
        self.ListBoxNewWindow.ListBoxNewWindow_huifuBox.delete(0,END)
        for x in outlistjiance:
            self.ListBoxNewWindow.ListBoxNewWindow_jianceBox.insert("end", x)
        for x in outlistreply:
            self.ListBoxNewWindow.ListBoxNewWindow_huifuBox.insert("end",x)


    #
    def startmonitor(self):
         if len(monitor_name)>0:
            self.Monitors()
         self.init_window_name.after(10,self.startmonitor)




    def Monitors(self):
        # def __init__(self,monitorname):
        #     self.monitorname = monitorname
        # def loadmonitorvaluse(self):
        #     self.monitors = monitor_names
        # def printwindows(self):
        #     if len(self.monitors)>0 :
        #         print("answer:",self.monitors)
        # def startloops(self):
        #     while(True):
        #         self.loadmonitorvaluse()
        #         self.printwindows()

        monitors_names = monitor_name
        monitors_groups =monitor_group

        ##########收取message################################################
        message = messagebox
        if len(monitors)>0 :
            #取姓名群名, names 是一个字典,

            for names in monitors:
                sendflag = True
                dictname =list(names.keys())   #dictname[0]就是用户名
                keywords_dict = names[dictname[0]]

                #取所有的keyword 和 reply
                for keys in list(keywords_dict.keys()):
                    detect_keywords = keys
                    detect_reply = keywords_dict[keys] #取key reply 完成

                    ##########提取微信id################################################

                    wxid = contactsbook[dictname[0]]
                   # print('wxid',wxid)

                    ######开始写回复代码##################################################
                    ####################################################################

                    # if len(list(message.keys())) > 0:
                    #     if (message["content"] == detect_keywords) and sendflag:
                    #         self.wb.send_txt_msg(wxid,detect_reply)
                    #         localtime = time.asctime(time.localtime(time.time()))
                    #         print("send time",localtime)
                    #         messagebox.clear()
                    #         sendflag =False
                    #
                    #
                    temp = len(list(message.keys()))
                    #print('list(message.keys())',temp)
                    if temp > 0:
                        if (self.matchfuncs(message['content'],detect_keywords)) and sendflag:
                            self.wb.send_txt_msg(wxid,detect_reply)
                            localtime = time.asctime(time.localtime(time.time()))
                            print("send time",localtime)

                            sendflag =False
            messagebox.clear()




                    ####################################################################




                    #
                    # print("keywrods:", detect_keywords )
                    # print("reply:", detect_reply )

        else:
            print("Not start empty:")

##str: message['content'] 消息内容 keywords  : match keywords

    def matchfuncs(self,str,keywords):
    ###############所有的匹配机制都要卸载这里#########################################
#################################最简单的.*?开始##########################
        matchchar = re.match(('.*?' + keywords),str)

    ############################在这更新匹配方法###############################
        if matchchar == None:
            match =False
        else:
            match =True
        print("zheng ze ",('.*?' + keywords))
        print("run match funcs",matchchar)
        return match




#定义空字典留给信息调用
monitor_name=[]  #给单人用

monitor_group=[]# 给监视群组用



#定义空字典留给信息调用
messagebox ={}


###############用name反查wxid
contactsbook = {}



wms = WechatBotMessageServer('127.0.0.1', port=5555, url='https://www.httpbin.org/anything')
wmsthreading = threading.Thread(target=wms.start)
wmsthreading.start()



init_window = Tk()              #实例化出一个父窗口
ZMJ_PORTAL = MY_GUI(init_window)
# 设置根窗口默认属性
ZMJ_PORTAL.set_init_window()
init_window.after(1,ZMJ_PORTAL.startmonitor)
init_window.mainloop()






