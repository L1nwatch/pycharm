#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
20160827 增加了一个功能, 把自己新写的随机选择器集成进来了, 所以多了一个随机播放机进击的巨人的功能
20160827 以前:
本来已经用 automator 写了个显示隐藏文件和隐藏隐藏文件的 app了,但是我想再精简一下,而且提供更加可读的提示,
所以还是决定用 Python 写脚本后再用 automator 来运行

参考: http://www.conxz.net/blog/2013/10/25/sloppy-python-snippets-to-capture-command-output/
参考2:
    [Python 执行Shell 外部命令](http://unixman.blog.51cto.com/10163040/1641396)
"""

import subprocess
import tkinter
import requests
import tkinter.messagebox
import os
from library_wifi import ping_success
from random_choicer import random_player

__author__ = '__L1n__w@tch'


class MenuTool:
    """
    工具栏的类
    """

    def __init__(self):
        self.main_window = tkinter.Tk()
        self.__initialize_root()

        # 设置个大标题
        # self.__initialize_title()

        # 设置个列表, 显示相应按钮
        self.buttons = dict()
        self.set_buttons()

        self.main_window.mainloop()

    def __initialize_root(self):
        """
        初始化根窗口
        :return:
        """
        # 设置窗口大小
        self.main_window.geometry("240x240")

        self.main_window.title("个人工具箱")

        # 居中操作
        self.main_window.update()  # update window ,must do
        current_width = self.main_window.winfo_reqwidth()  # get current width
        current_height = self.main_window.winfo_height()  # get current height
        screen_width, screen_height = self.main_window.maxsize()  # get screen width and height
        configuration = '%dx%d+%d+%d' % (current_width, current_height,
                                         (screen_width - current_width) / 2, (screen_height - current_height) / 2)
        self.main_window.geometry(configuration)

    def __initialize_title(self):
        """
        设置个大标题
        :return:
        """
        label_frame = tkinter.LabelFrame(self.main_window)
        title = tkinter.Text(label_frame)
        title.insert(tkinter.END, "个人工具箱")
        title.grid()
        label_frame.grid()

    def grid_buttons(self):
        for each in self.buttons:
            self.buttons[each].grid()

    def define_buttons(self, list_box):
        self.buttons["change_hidden_status_button"] = tkinter.Button(list_box, text="更改隐藏文件显示状态",
                                                                     command=lambda: change_hidden_status_tool(True))

        self.buttons["login_school_wifi_button"] = tkinter.Button(list_box, text="登录西电校园网",
                                                                  command=lambda: logging_school_wifi(True))
        self.buttons["open_aria2c_button"] = tkinter.Button(list_box, text="开启 aria2c", command=open_aria2c)
        self.buttons["open_shadowsocks_button"] = tkinter.Button(list_box, text="开启 shadowsocks",
                                                                 command=open_shadowsocks)
        self.buttons["random_play_attack"] = tkinter.Button(list_box, text="随机播放一集进击的巨人",
                                                            command=lambda: random_player(
                                                                "/Users/L1n/Desktop/Entertainment/进击的巨人第一季全集", ["mp4"]))
        self.buttons["switch_privoxy"] = tkinter.Button(list_box, text="开启或关闭 Privoxy",
                                                        command=lambda: switch_open_privoxy(True))

    def set_buttons(self):
        """
        设置相应按钮
        :return:
        """
        label_frame = tkinter.LabelFrame(self.main_window)
        list_box = tkinter.Listbox(label_frame)

        # 初始化按钮
        self.define_buttons(list_box)

        # 按钮放置
        self.grid_buttons()

        # listbox 盒放置
        list_box.grid()
        label_frame.pack()


def change_hidden_status_tool(verbose=False):
    """
    改变隐藏文件显示状态, 如果运行前处于不显示则更改为显示, 如果为显示则更改为不显示
    :param verbose: 是否要开启弹窗提醒
    :return:
    """
    if verbose:
        tk = tkinter.Tk()
        tk.withdraw()

    cmd = "defaults read com.apple.finder AppleShowAllFiles -boolean"
    popen = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE)
    res = popen.stdout.readline().strip()

    change_command = "defaults write com.apple.finder AppleShowAllFiles -boolean {} ; killall Finder"
    if res == b"1":
        subprocess.call(change_command.format("false"), shell=True)
        tkinter.messagebox.showinfo("取消显示隐藏文件", "取消显示成功") if verbose else None
    elif res == b"0":
        subprocess.call(change_command.format("true"), shell=True)
        tkinter.messagebox.showinfo("显示隐藏文件", "显示隐藏文件成功") if verbose else None
    else:
        tkinter.messagebox.showerror("Something wrong!") if verbose else None

    exit()


def logging_school_wifi(verbose=False):
    """
    尝试登陆学校 wifi
    :return:
    """
    ifconfig_output = subprocess.check_output("ifconfig").decode()
    if "std-wlan" not in ifconfig_output.lower():
        tkinter.messagebox.showinfo("登录校园网", "你没连上学校 wifi 啊")
    else:
        # 认证页面
        url = "http://10.255.44.33:803/include/auth_action.php"
        post_data = {"action": "login", "username": "13030110024", "password": "5w8zPKpw4#cE*5woatwj",
                     "ac_id": "1", "save_me": 0}  # &user_ip=&nas_ip=&user_mac=&save_me=0&ajax=1"}
        response = requests.post(url, post_data)

        if ping_success():
            tkinter.messagebox.showinfo("登录校园网", "登录成功") if verbose else None
        else:
            tkinter.messagebox.showerror("登录校园网", response.text) if verbose else None


def open_aria2c(verbose=True):
    """
    开启 aria2c 程序
    :param verbose: 是否显示详细信息
    :return:
    """
    # subprocess.call("aria2c", shell=True) # 必须得用 os.system 才能运行成功, 原因未知
    # 另外用 os.system("aria2c") 也失败了, 用 Automator 打开的时候好像权限降低了, 自己用 Pycharm 倒是成功的
    os.system("/usr/local/aria2/bin/aria2c")  # 最终成功

    tkinter.messagebox.showinfo("开启 aria2c", "开启成功") if verbose else None


def open_shadowsocks(verbose=True):
    """
    开启 aria2c 程序
    :param verbose: 是否显示详细信息
    :return:
    """
    # subprocess.call("aria2c", shell=True) # 必须得用 os.system 才能运行成功, 原因未知s
    os.system("open /Applications/ShadowsocksX.app/")

    tkinter.messagebox.showinfo("开启 aria2c", "开启成功") if verbose else None


def is_privoxy_running():
    """
    查看 Privoxy 是否在开启中
    :return:
    """
    try:
        result = subprocess.check_output("netstat -an | grep 8118", shell=True)
    except subprocess.CalledProcessError:
        return False
    return True


def switch_open_privoxy(verbose=True):
    """
    如果 privoxy 是开启的, 就关闭掉, 否则就开启
    :param verbose: True or False, 表示是否要打印详细信息
    :return:
    """
    # 尝试使用 sudo 命令失败了, 最终是参考这篇教程成功的:
    # http://askubuntu.com/questions/155791/how-do-i-sudo-a-command-in-a-script-without-being-asked-for-a-password
    # 基本步骤是:
    # 1. 创建一个 sh 文件,并且赋予执行权限
    # 2. sudo visudo, 添加这么一句话:
    # 3. username ALL=(ALL) NOPASSWD: /Applications/Privoxy/start_privoxy_without_sudo.sh
    if is_privoxy_running():
        os.system("sudo /Applications/Privoxy/stop_privoxy_without_sudo.sh")
        tkinter.messagebox.showinfo("关闭 Privoxy", "关闭成功") if verbose else None
    else:
        os.system("sudo /Applications/Privoxy/start_privoxy_without_sudo.sh")
        tkinter.messagebox.showinfo("开启 Privoxy", "开启成功") if verbose else None


if __name__ == "__main__":
    my_menu_tool = MenuTool()
