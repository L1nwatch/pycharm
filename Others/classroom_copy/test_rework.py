#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 对自己写的拷贝程序进行单元测试
'''
__author__ = '__L1n__w@tch'

import unittest
import random
import os
import shutil
from try_rework import FilesSaver
import filecmp
import time

test_src = r"C:\Users\L1n\Desktop"
test_des = r"D:\goodgoodstudy"
retention = {'desktop.ini', 'Software', 'Study.lnk', '小Q屏幕截图.lnk'}
wait_time = 0.5


class TestSir(unittest.TestCase):
    def setUp(self):
        self.src = test_src
        self.des = test_des
        self.test_files_path = os.curdir
        self.wait_time = wait_time
        self.retention = retention

    def test_files_saver_ensure(self):
        def _test1():
            test_file_name = "just_a_file"
            test_file = os.path.join(os.curdir, "for_test", "just_a_file")
            shutil.copy(test_file, self.src)
            files_saver.ensure()
            time.sleep(self.wait_time)
            files = os.listdir(self.des)
            self.failUnless(test_file_name in files)

        def _test2():
            # TODO
            self.failUnless(True)

        def _test3():
            test_file = os.path.join(os.curdir, "for_test", "just_a_file")
            shutil.copy(test_file, self.src)
            files_saver.ensure()
            with open(test_file, "a") as f:
                f.write("test" * 30)
            files_saver.ensure()
            time.sleep(self.wait_time)
            file1 = os.path.join(self.src, test_file)
            file2 = os.path.join(self.des, test_file)
            self.failUnless(filecmp.cmp(file1, file2))

        def _test4():
            shutil.copytree("for_test", self.src)
            files_saver.ensure()
            with open(os.path.join(self.src, "for_test", "test1"), "a") as f:
                f.write("test" * 3)
            files_saver.ensure()
            time.sleep(5)
            result = filecmp.dircmp(self.src, self.des).diff_files
            self.failIf(len(result) <= 0)

        files_saver = FilesSaver(self.src, self.des, self.retention)

        # case: 有文件复制到了源文件夹
        _test1()

        # case: 源文件夹中, retention文件列表中的文件被删除了
        _test2()

        # case: 源文件夹中, 非retention文件发生了改变
        _test3()

        # case: 源文件夹中, 非retention文件夹中的文件发生了改变
        _test4()

    def test_files_saver_delete(self):
        files_saver = FilesSaver(self.src, self.des, self.retention)

        test_file = os.path.join(os.curdir, "for_test", "just_a_file")
        shutil.copy(test_file, self.src)
        files_saver.delete()
        self.failIf(test_file in os.listdir(self.src))


def main():
    unittest.main()


if __name__ == "__main__":
    main()
