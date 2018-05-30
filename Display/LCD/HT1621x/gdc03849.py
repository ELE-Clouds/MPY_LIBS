# -*- coding:UTF-8 -*-

'''
MIT License

Copyright (c) 2018 Robin Chen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

'''******************************************************************************
* 文  件：gdc03849.py
* 概  述：ht1621x芯片驱动GDC03849段式液晶的程序,显示范围-99.99-999.99
* 版  本：V0.10
* 作  者：Robin Chen
* 日  期：2018年5月9日
* 历  史： 日期             编辑           版本         记录
          2018年5月09日    Robin Chen    V0.10       创建文件
          2018年5月30日    Robin Chen    V0.11       完成驱动封装
******************************************************************************'''

# 16进制湿度字库(0~9,包含湿度文字、 小数点及湿度单位显示)
NUMCODE_RH_HEX = ((0x0D, 0x0F),    # 0
                  (0x08, 0x06),
                  (0x0B, 0x0D),
                  (0x0A, 0x0F),
                  (0x0E, 0x06),
                  (0x0E, 0x0B),
                  (0x0F, 0x0B),
                  (0x08, 0x0E),
                  (0x0F, 0x0F),
                  (0x0E, 0x0F))    # 9

# 16进制温度字库(0~9,包含温度文字、 小数点及温度单位显示)
NUMCODE_TEMP_HEX = ((0x0F, 0x0D),  # 0
                    (0x06, 0x08),
                    (0x0B, 0x0E),
                    (0x0F, 0x0A),
                    (0x06, 0x0B),
                    (0x0D, 0x0B),
                    (0x0D, 0x0F),
                    (0x07, 0x08),
                    (0x0F, 0x0F),
                    (0x0F, 0x0B))  # 9


class GDC03849:
    def __init__(self, _ht1621x):
        self.ht = _ht1621x
        self.ht.init()      # 此处可根据需要添加参数，当前使用默认参数
        self.ht.LCDON()
        self.LCDALLSHOW()
        self.ht.HTBEEP(1)   # 蜂鸣器响1秒
        self.LCDALLCLEAR()

    '''*************************************************************************
    * 功   能：显示温度值
    * 说   明：将进制制浮点数温度值以两位小数的形式显示出来
    * 输入参数：
              _gdcdata: 测量到的温度值 | flot | de | 000.00~999.99 | eg. 24.543
    * 输出参数：None
    * 返 回 值：True
    **************************************************************************'''
    def viewTemp(self, _gdcdata):
        val = ()
        stda = ('00000' + str(int(_gdcdata * 100)))[-5::]
        stda = list(stda)[::-1]
        for i in stda:
            val = val + NUMCODE_TEMP_HEX[int(i)]
        self.ht.HT1621xWrAllData(0x0A, val)
        return True


    '''*************************************************************************
    * 功   能：显示湿度值
    * 说   明：将进制制浮点数湿度值以两位小数的形式显示出来
    * 输入参数：
              _gdcdata: 测量到的湿度值 | flot | de | 000.00~999.99 | eg. 24.543
    * 输出参数：None
    * 返 回 值：True
    **************************************************************************'''
    def viewRH(self, _gdcdata):
        val = ()
        stda = ('00000' + str(int(_gdcdata * 100)))[-5::]
        for i in stda:
            val = val + NUMCODE_RH_HEX[int(i)]
        self.ht.HT1621xWrAllData(0x00, val)
        return True


    '''*************************************************************************
    * 功   能：显示所有显示字段
    * 说   明：所有液晶段全部显示
    * 输入参数：None
    * 输出参数：None
    * 返 回 值：True
    **************************************************************************'''
    def LCDALLSHOW(self):
        self.ht.ALLSHOW(0x00, 20)
        return True


    '''*************************************************************************
    * 功   能：清除屏幕全部显示
    * 说   明：所有液晶段全部不显示
    * 输入参数：None
    * 输出参数：None
    * 返 回 值：True
    **************************************************************************'''
    def LCDALLCLEAR(self):
        self.ht.ALLCLEAR(0x00, 20)
        return True


    '''*************************************************************************
    * 功   能：清除屏幕温度区域显示
    * 说   明：温度显示区域所有液晶段全部不显示（包括“温度”字样）
    * 输入参数：None
    * 输出参数：None
    * 返 回 值：True
    **************************************************************************'''
    def TEMPCLEAR(self):
        self.ht.ALLCLEAR(0x0A, 10)
        return True


    '''*************************************************************************
    * 功   能：清除屏幕湿度区显示
    * 说   明：湿度显示区域所有液晶段全部不显示（包括“湿度”字样）
    * 输入参数：None
    * 输出参数：None
    * 返 回 值：True
    **************************************************************************'''
    def RHCLEAR(self):
        self.ht.ALLCLEAR(0x00, 10)
        return True
