
from tkinter import *



class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name

    def set_init_window(self):

        self.activekeys = [ ]

        self.init_window_name.title("WechatBot")
        self.init_window_name.geometry('1068x681+10+10')

        self.Contacts = []
        self.GroupContacts = []
        #GetContacts button setting
        self.getcontactsbutton = Button(self.init_window_name, text="获取联系人", bg="lightblue", width=10)
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
        self.GroupContactScrollbar.grid(row=4,column=1)



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
        self.contactslabel.grid(row = 0, column = 0)
        self.groupslabel = Label(self.init_window_name, text="群号")
        self.groupslabel.grid(row = 2, column = 0)

        ###################设计监视框#########################################
        self.person_name = Label(self.init_window_name, text="联系人")
        self.person_name.grid(row = 0, column = 4)
        self.person_nameBox = Listbox(self.init_window_name)
        self.person_nameBox.grid(row = 1, column = 4)


        self.person_keywords = Label(self.init_window_name, text="关键词")
        self.person_keywords.grid(row = 0, column = 5)
        self.person_keywordsBox = Listbox(self.init_window_name)
        self.person_keywordsBox.grid(row = 1, column = 5)


        self.person_reply = Label(self.init_window_name, text="回复")
        self.person_reply.grid(row = 0, column = 6)
        self.person_replyBox = Listbox(self.init_window_name)
        self.person_replyBox.grid(row = 1, column = 6)


###################设计监视框群聊#########################################
        self.group_name = Label(self.init_window_name, text="群名")
        self.group_name.grid(row = 2, column = 3)
        self.group_nameBox = Listbox(self.init_window_name)
        self.group_nameBox.grid(row = 3, column = 3)


        self.group_membername = Label(self.init_window_name, text="群员名")
        self.group_membername.grid(row = 2, column = 4)
        self.group_membernameBox = Listbox(self.init_window_name)
        self.group_membernameBox.grid(row = 3, column = 4)


        self.group_keyword = Label(self.init_window_name, text="回复")
        self.group_keyword.grid(row = 2, column = 5)
        self.group_keywordBox = Listbox(self.init_window_name)
        self.group_keywordBox.grid(row = 3, column = 5)

        self.group_reply = Label(self.init_window_name, text="回复")
        self.group_reply.grid(row = 2, column = 6)
        self.group_replyBox = Listbox(self.init_window_name)
        self.group_replyBox.grid(row = 3, column = 6)




init_window = Tk()              #实例化出一个父窗口
ZMJ_PORTAL = MY_GUI(init_window)
# 设置根窗口默认属性
ZMJ_PORTAL.set_init_window()

init_window.mainloop()