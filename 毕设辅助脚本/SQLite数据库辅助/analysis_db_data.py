#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 统计数据库中的信息用的

2017.05.18 补充了另外一个版本的分析, 现在既有基于主域名分析, 也有基于子域名的分析
2017.05.10 完善当链接数过多时的统计代码
2017.05.08 需要对真实数据库里面的信息进行统计
"""
from create_db_data import DomainID2URLInDoc, LinkInDoc, DatabaseBasicDeal
from collections import defaultdict

real_db_path = "/Users/L1n/Desktop/Notes/毕设/毕设实现/工程文件/link_relationship.db"

__author__ = '__L1n__w@tch'


class DBAnalysis:
    def __init__(self):
        self.db = DatabaseBasicDeal()
        self.domain_id_url_dict = self.db.get_all_domain_id_url_in_doc_from_db()
        self.main_domains = ["cn.yahoo.com", "people.com.cn", "news.ifeng.com", "news.163.com", "news.sohu.com"]

    def domain_id_to_url(self, domain_id):
        """
        给定一个域名 id, 转换为对应的域名, 比如 "69713306c0bb3300" -> ""
        :param domain_id: str(), 域名 id, 比如 "69713306c0bb3300"
        :return: str(), 对应的 URL 信息, 比如 ""
        """
        return self.domain_id_url_dict[domain_id]

    def get_main_domain(self, url):
        """
        求一个 URL 属于哪个主域名
        :param url: str(), 比如 "xz.people.com.cn"
        :return: str(), 主域名, 比如 "people.com.cn"
        """
        for each_domain in self.main_domains:
            if url.endswith(each_domain):
                return each_domain
        raise RuntimeError("[-] Can not find main domain of {}".format(url))

    def print_link_info_with_main_domain(self, link_set):
        """
        按照主域名区分打印出链接情况
        :param link_set: dict(), 比如: {'news.sohu.com': 5, 'club.comment2.news.sohu.com': 1, 'club.news.sohu.com': 2}
        :return: None, 直接打印
        """
        result_dict = defaultdict(lambda: 0)
        for each in link_set:
            if isinstance(each, str):
                result_dict[self.get_main_domain(each)] += 1
            elif isinstance(each, tuple):
                result_dict[self.get_main_domain(each[0])] += 1

        for domain, count in result_dict.items():
            print("[*] {sep}{domain}{sep}---->{sep}{count}".format(sep="\t", domain=domain, count=count))

    def is_same_main_domain(self, domain_id1, domain_id2):
        """
        给定俩域名 ID, 判断是否属于同一主域名
        :param domain_id1: str(), 比如 "69713306c0bb3300"
        :param domain_id2: str(), 比如 "69713306c0bb3300"
        :return: boolean(), 比如 True
        """
        main_domain1 = self.get_main_domain(self.domain_id_to_url(domain_id1))
        main_domain2 = self.get_main_domain(self.domain_id_to_url(domain_id2))
        return main_domain1 == main_domain2

    def run(self):
        """
        基于子域名进行分析
        """
        # 需要统计的信息, 有多少链接关系, 多少内联, 分别是什么域名链接什么域名, 多少外链, 分别是什么域名链接什么域名
        total_link = len(LinkInDoc.select())
        inside_link = set()
        outside_link = set()

        print(len(DomainID2URLInDoc.select()))
        print("[*] 总共有 {} 条链接关系".format(total_link))

        for each in LinkInDoc.select():
            # 统计内联链接:
            if each.domain_id == each.out_id:
                inside_link.add(self.domain_id_url_dict[each.domain_id])
            # 统计外链链接
            else:
                outside_link.add((self.domain_id_url_dict[each.domain_id], self.domain_id_url_dict[each.out_id]))

        print("[*] 总共有 {} 条内联链接, {} 条外链链接".format(len(inside_link), len(outside_link)))
        print("[*] 内联链接情况如下: ")
        self.print_link_info_with_main_domain(inside_link)
        print("[*] 外链链接情况如下: ")
        self.print_link_info_with_main_domain(outside_link)

    def run2(self):
        """
        基于主域名进行分析
        """
        # 需要统计的信息, 有多少链接关系, 多少内联, 分别是什么域名链接什么域名, 多少外链, 分别是什么域名链接什么域名
        total_link = len(LinkInDoc.select())
        inside_link = set()
        outside_link = set()

        print("[*] 总共有 {} 条链接关系".format(total_link))

        for each in LinkInDoc.select():
            # 统计内联链接:
            if self.is_same_main_domain(each.domain_id, each.out_id):
                inside_link.add(self.domain_id_to_url(each.domain_id))
            # 统计外链链接
            else:
                outside_link.add((self.domain_id_to_url(each.domain_id), self.domain_id_to_url(each.out_id)))

        print("[*] 总共有 {} 条内联链接, {} 条外链链接".format(len(inside_link), len(outside_link)))
        print("[*] 内联链接情况如下: ")
        self.print_link_info_with_main_domain(inside_link)
        print("[*] 外链链接情况如下: ")
        self.print_link_info_with_main_domain(outside_link)


if __name__ == "__main__":
    dba = DBAnalysis()
    dba.run()
