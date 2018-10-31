# -*- coding: utf-8 -*-

import unittest


class TestMathFunc(unittest.TestCase):

    def setUp(self):
        print("do something before test.Prepare environment.")

    def tearDown(self):
        print("do something after test.Clean up.")

    def test_1(self):
        cnt = 0
        for i in range(1, 5):
            for j in range(1, 5):
                for k in range(1, 5):
                    if i != j and i != k and j != k:
                        print(i * 100 + j * 10 + k, " ", end="")
                        cnt += 1
        print("")
        print("cnt", cnt)

    def test_2(self):
        # python 3 input replace raw_input
        i = int(input('enter the profit: '))
        arr = [10 ** 6, 10 ** 5 * 6, 10 ** 5 * 4, 10 ** 5 * 2, 10 ** 5, 0]
        profit = [1 / 100, 1.5 / 100, 3 / 100, 5 / 100, 7.5 / 100, 10 / 100]

        r = 0
        for idx in range(0, 6):
            if i > arr[idx]:
                r += (i - arr[idx]) * profit[idx]
                i = arr[idx]
        print("利润", r)

    def test_3(self):
        import math
        num = 0
        while True:
            if (math.sqrt(num + 100) - int(math.sqrt(num + 100)) == 0) and \
                    (math.sqrt(num + 168) - int(math.sqrt(num + 168)) == 0):
                break
            num += 1
        print("num", num)

    def test_4(self):
        import datetime
        day = str(input('input day(20180503): '))
        end_dt = datetime.datetime.strptime(day, "%Y%m%d")
        start_dt = datetime.datetime.strptime(day[:4] + "0101", "%Y%m%d")

        print("是%d的第%d天" % (start_dt.year, (end_dt - start_dt).days + 1))

    def test_5(self):
        from math import sqrt
        # 在一般领域，对正整数n，如果用 2 到 n平方根 之间的所有整数去除，均无法整除，则n为质数。
        for num in range(101, 201):
            flag = False
            for i in range(2, int(sqrt(num)) + 1):
                if num % i == 0:
                    flag = True
                    break

            if not flag:
                print(str(num) + " ", end="")
        print("")

    def test_6(self):
        for num in range(100, 1000):
            a = int(num / 100)
            b = int(num % 100 / 10)
            c = num % 10
            # print(a, b, c)
            if a ** 3 + b ** 3 + c ** 3 == num:
                print(str(num) + " ", end="")
        print("")

