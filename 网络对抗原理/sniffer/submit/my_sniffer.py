#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 开启/关闭混杂模式: ifconfig en0 promisc/-promisc
开/关网卡: ifconfig en0 up/down
开启监听模式: ifconfig en0 mode monitor
======================================================================
将 airport 添加到路径(http://blog.csdn.net/jpiverson/article/details/22663101):
sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/sbin/airport
扫描命令：airport en0 scan。可以使用grep进行过滤，如：airport en0 scan |grep WEP或airport en0 scan |grep WPA
监听命令：sudo airport en0 sniff 6。en0是所使用网卡的名称，sniff表示模式，6表示信道。
======================================================================
其实在 sniff 给个 promisc 参数不就完事了..

注意, 如果装了 matplotlib 库, 会跟 tkinter 起冲突
'''
__author__ = '__L1n__w@tch'

from scapy.all import *
import threading

l_packets = list()

# 互斥量, 用来手动挂起线程的
semaphore = threading.Semaphore(0)


class MySnifferThread(threading.Thread):
    def __init__(self):
        super(MySnifferThread, self).__init__()

        # 挂起线程用了, 为了实现暂停功能
        global semaphore
        self.stopped = None
        self.configurate()

    def configurate(self, iface="en0", promisc=1, lfilter=None, store=False):
        # 设置网卡
        self.iface = iface

        # 是否开启混杂模式, 1 为开启, 0 为关闭
        self.promisc = promisc

        # 过滤器, 只留下某些包, 比如 lfilter = lambda x: x.haslayer("TCP"), 只留下 TCP 包
        self.lfilter = lfilter

        # 是否保存嗅探包
        self.store = store

    def run(self):
        self.stopped = False
        sniff(prn=self.prn, iface=self.iface, promisc=self.promisc, store=self.store, lfilter=self.lfilter)

    def stop(self):
        self.stopped = True

    def is_stopped(self):
        return self.stopped

    def restart(self):
        self.stopped = False
        MySnifferThread.v(semaphore)

    def prn(self, packet):
        global l_packets
        l_packets.append(packet)

        # 看是否要挂起线程
        if self.stopped:
            MySnifferThread.p(semaphore)

    @staticmethod
    def v(semaphore):
        """
        V 原语,相当于释放资源
        :return:
        """
        semaphore.release()

    @staticmethod
    def p(semaphore):
        """
        P 原语,相当于申请资源
        :return:
        """
        semaphore.acquire()


def sniff_thread():
    my_sniffer = MySnifferThread()
    my_sniffer.configurate(promisc=0)
    my_sniffer.start()


def print_l_packets():
    while True:
        if len(l_packets) > 0:
            print(l_packets)


if __name__ == "__main__":
    global ip_list, l_packets
    ip_list = set()

    sniff_thread = threading.Thread(target=sniff_thread)
    sniff_thread.start()
    sniff_thread.join()

    # print(l_packets)

    # 测试线程变量是否能共享更新的 l_packets
    # t = threading.Thread(target=print_l_packets)
    # t.start()

    for packet in l_packets:
        print(packet.src)

"""
之前的学习
    def all(packet):
        if packet.src == "ac:bc:32:7c:02:33" or packet.dst == "ac:bc:32:7c:02:33":
            return

        print("{} -> {}".format(packet.src, packet.dst))
        if packet.haslayer("ARP"):
            return
            # arp(packet)
        elif packet.haslayer("IP"):
            ip(packet, ["10.177.185.95"], "192.168.158")


    def ip(packet, filter=[], prefix=""):
        if packet[IP].src in filter or packet[IP].dst in filter:
            # print(".", end="", flush=True)
            return

        print("{} -> {}".format(packet[IP].src, packet[IP].dst))
        if packet[IP].src not in ip_list and packet[IP].src.startswith(prefix):
            print(packet.show())
            ip_list.add(packet[IP].src)
            print(ip_list)
        if packet[IP].dst not in ip_list and packet[IP].dst.startswith(prefix):
            print(packet.show())
            ip_list.add(packet[IP].dst)
            print(ip_list)

        if packet[IP].src != "192.168.43.17" and packet[IP].src != "192.168.43.43":
            pass


    def arp(packet):
        print("{} -> {}".format(packet[ARP].psrc, packet[ARP].pdst))

        if packet[ARP].psrc != "192.168.43.17" and packet[ARP].psrc != "192.168.43.43":
            pass


    # pcap = ctypes.cdll.LoadLibrary(find_library("libpcap"))
    # sniff(prn=test, filter="arp", iface="en0")

    # iface 网卡参数, prn 回调函数, promisc 混杂模式
    sniff(prn=all, iface="en0", promisc=1)
"""
