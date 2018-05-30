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

'''
******************************************************************************
* 文  件：ht1621x.py
* 概  述：ht1621x芯片驱动文件
* 版  本：V0.13
* 作  者：Robin Chen
* 日  期：2018年5月9日
* 历  史： 日期             编辑           版本         记录
          2018年5月9日    Robin Chen    V0.10       创建文件
          2018年5月11日   Robin Chen    V0.11       将所有命令以二进制字符串的形式列了出来
          2018年5月17日   Robin Chen    V0.12       将代码使用类封装成可调用的驱动
          2018年5月30日   Robin Chen    V0.13       完成代码封装
******************************************************************************'''
from micropython import const
from time import sleep_ms, sleep_us, sleep

# 命令清单
# -------------------------
# 功能符号(标志字)
FLAG_CMD      = const(0x04)  # 100 命令
FLAG_READ     = const(0x06)  # 110 只读RAM
FLAG_WRITE    = const(0x05)  # 101 只写RAM
FLAG_MODIFY   = const(0x05)  # 101 读和写RAM(即修改RAM)READ-MODIFY-WRITE

# 液晶控制
CMD_LCDON     = const(0x006)  # 000000110 打开LCD偏压发生器
CMD_LCDOFF    = const(0x004)  # 000000100 关闭LCD偏压发生器   （上电时默认设置）

# 系统控制
CMD_SYSEN     = const(0x002)  # 000000010 打开系统振荡器
CMD_SYSDIS    = const(0x000)  # 000000000 关半系统振荡器和LCD偏压发生器 （上电时默认设置）

# Bias与COM设置，即偏置电压与COM端,当前参数根据液晶的资料文件进行选择，比如1/4DUTY,1/3BIAL，则选择"B3C4"
# 1/2偏压设置
CMD_B2C2      = const(0x040)  # 001000000 2COM,1/2 bias
CMD_B2C3      = const(0x048)  # 001001000 3COM,1/2 bias
CMD_B2C4      = const(0x050)  # 001010000 4COM,1/2 bias

# 1/3偏压设置
CMD_B3C2      = const(0x042)  # 001000010 2COM,1/3 bias
CMD_B3C3      = const(0x04A)  # 001001010 3COM,1/3 bias
CMD_B3C4      = const(0x052)  # 001010010 4COM,1/3 bias

# 时钟设置
CMD_RC256K    = const(0x030)  # 000110000 系统时钟源，片内RC振荡器   （上电时默认设置）
CMD_EXT256K   = const(0x038)  # 000111000 系统时钟源，外部时钟
CMD_XTAL32K   = const(0x028)  # 000101000 系统时钟源（晶振）

# 时基设置
CMD_TIMER_EN  = const(0x00C)  # 000001100 时基输出使能
CMD_TIMER_DIS = const(0x008)  # 000001000 时基输出失效
CMD_CLR_TIMER = const(0x018)  # 000011000 时基发生器清零

# WDT设置
CMD_WDT_DIS = const(0x00A)  # 000001010 WDT溢出标志输出失效，禁用看门狗
CMD_WDT_EN  = const(0x00E)  # 000001110 WDT溢出标志输出有效，启用看门狗
CMD_CLR_WDT = const(0x01C)  # 000011100 清除WDT状态

# 声音输出设置
CMD_TONE2K  = const(0x0C0)  # 011000000 设置声音频率输出为2KHz
CMD_TONE4K  = const(0x080)  # 010000000 设置声音频率输出为4KHz
CMD_TONEON  = const(0x012)  # 000010010 打开声音输出
CMD_TONEOFF = const(0x010)  # 000010000 关闭声音输出   （上电时默认设置）

# 时基/WDT输出设置
CMD_F1      = const(0x140)  # 101000000 时基/WDT时钟输出:1Hz | WDT超时标志后: 4s
CMD_F2      = const(0x142)  # 101000010 时基/WDT时钟输出:2Hz | WDT超时标志后: 2s
CMD_F4      = const(0x144)  # 101000100 时基/WDT时钟输出:4Hz | WDT超时标志后: 1s
CMD_F8      = const(0x146)  # 101000110 时基/WDT时钟输出:8Hz | WDT超时标志后: 1/2s
CMD_F16     = const(0x148)  # 101001000 时基/WDT时钟输出:16Hz | WDT超时标志后: 1/4s
CMD_F32     = const(0x14A)  # 101001010 时基/WDT时钟输出:32Hz | WDT超时标志后: 1/8s
CMD_F64     = const(0x14C)  # 101001100 时基/WDT时钟输出:64Hz | WDT超时标志后: 1/16s
CMD_F128    = const(0x14E)  # 101001110 时基/WDT时钟输出:128Hz | WDT超时标志后: 1/32s   （上电时默认设置）

# IRQ设置
CMD_IRQ_DIS = const(0x100)  # 100000000 使IRQ输出失效   （上电时默认设置）
CMD_IRQ_EN  = const(0x110)  # 100010000 使IRQ输出有效

# 工作模式设置
CMD_TEST    = const(0x1C0)  # 111000000 测试模式
CMD_NORMAL  = const(0x1C6)  # 111000110 普通模式   （上电时默认设置）

# 默认设置清单
'''----------------------------------------
|  CMD_LCDOFF   |  LCD偏压发生器关闭       |
|  CMD_SYSDIS   |  系统振荡器关闭          |
|  CMD_RC256K   |  使能RC振荡器           | 
|  CMD_TONEOFF  |  声音通道关闭            |   
|  CMD_F128     |  时基/WDT时钟输出为128Hz |
|  CMD_IRQ_DIS  |  IRQ输出关闭            |
|  CMD_NORMAL   |  系统设置为默认工作模式    |
-----------------------------------------'''


# -------------- 结束 -----------------


class HT1621B:
    '''*************************************************************************
    * 功   能：芯片引脚初始化
    * 说   明：根据液晶情况，对芯片引脚进行初始化
    * 输入参数：
    *          _cs:   CS引脚
    *          _rd:   RD引脚
    *          _wr:   WR引脚
    *          _htdata: DATA引脚
    * 输出参数：None
    * 返 回 值：
    **************************************************************************'''
    def __init__(self, _cs, _rd, _wr, _htdata):
        self.CS = _cs      # 定义CS引脚
        self.RD = _rd      # 定义RD引脚
        self.WR = _wr      # 定义WR引脚
        self.DA = _htdata  # 定义DATA引脚
        self.CS.init(self.CS.OUT, self.CS.PULL_UP, value=1)  # 低电平有效,初始化后拉高
        self.RD.init(self.RD.OUT, self.RD.PULL_UP, value=1)  # 低电平有效,初始化后拉高
        self.WR.init(self.WR.OUT, self.WR.PULL_UP, value=1)  # 低电平有效,初始化后拉高
        self.DA.init(self.DA.OUT, self.DA.PULL_UP, value=1)  # 高低电平有效,初始化后拉高
        self.init()

    '''*************************************************************************
    * 功   能：HT1621x参数初始化
    * 说   明：根据当前配置，打开或关闭一些功能
    * 输入参数：None
    * 输出参数：None
    * 返 回 值：
    **************************************************************************'''
    def init(self,
             _timer = CMD_TIMER_DIS,    # 时期输出设置
             _wdt   = CMD_WDT_DIS,        # WDT溢出标志输出设置
             _scs   = CMD_RC256K,         # 系统时钟源设置
             _bias  = CMD_B3C4,          # 偏压和公共端设置
             _tone  = CMD_TONE4K,        # 声音设置
             _irq   = CMD_IRQ_DIS,        # IRQ设置（生效/失效）
             _twc   = CMD_F128,           # 时期/WDT时钟输出设置（F1～F128）
             _mod   = CMD_NORMAL          # 模式设置（测试模式和普通模式）
             ):

        # 命令清单列表
        lcmd = (_timer, _scs, _bias, _irq, _twc, _mod, CMD_CLR_TIMER, CMD_CLR_WDT)

        self.CS.on()
        self.WR.on()
        self.RD.on()
        self.DA.on()
        sleep(1)
        self.HT1621xWrCmd(CMD_SYSDIS)  # 关闭系统时钟
        self.HT1621xWrCmd(_wdt)
        self.HT1621xWrCmd(CMD_SYSEN)
        # 循环发送命令
        for cmd in lcmd:
            self.HT1621xWrCmd(cmd)
        self.ALLCLEAR(0, 32)
        # self.HT1621xWrCmd(CMD_LCDON)
        return True


    '''*************************************************************************
    * 功   能：发送数据
    * 说   明：将数据转化时序波形
    * 输入参数：
              _da: 需要写入的数据 | int | bin | 9 bit
    * 输出参数：None
    * 返 回 值：
              True
    **************************************************************************'''
    def _wrData(self, _da):
        for i in _da:
            self.WR.off()
            self.DA.value(int(i))
            sleep_us(4)
            self.WR.on()
            sleep_us(4)
        return True


    '''*************************************************************************
    * 功   能：写命令
    * 说   明：
    * 输入参数：
              _cmd: 16 | str | hex | eg:0x04
    * 输出参数：None
    * 返 回 值：True
    **************************************************************************'''
    def HT1621xWrCmd(self, _cmd):
        FC = bin(FLAG_CMD)[2:]
        CMD = bin(_cmd ^ (1 << 9))[3:]
        self.CS.off()
        sleep_us(4)
        self._wrData(FC)
        self._wrData(CMD)
        self.CS.on()
        sleep_us(4)
        return True


    '''*************************************************************************
    * 功   能：指定地址写单个数据
    * 说   明：
    * 输入参数：
              名称       描述      类型  值                 示例
              addr:    数据地址 | str | hex | 0x00~0x1F | eg: 0x00
              _htdata: 数据列表 | list| hex | 0x00~0x0F | eg: 0x00
    * 输出参数：None
    * 返 回 值：
    **************************************************************************'''
    def HT1621xWrOneData(self, _addr, _htdata):
        FW = bin(FLAG_WRITE)[2:]
        ad = bin(_addr ^ (1 << 6))[3:]    # 将16进制值转化为6位二进制字符串
        da = bin(_htdata ^ (1 << 4))[3:]  # 将16进制值转化为4位二进制字符串
        self.CS.off()
        sleep_us(4)
        self._wrData(FW)
        self._wrData(ad)
        self._wrData(da)
        self.CS.on()
        sleep_us(4)
        return True


    '''*************************************************************************
    * 功   能：指定地址连续写多个数据
    * 说   明：
    * 输入参数：
              _addr: 数据起始地址  | str  | hex | 6位       | eg. 0x00
              _htdata: 数据列表   | list | hex | 32位      | eg: [0x00,0x0F,0x0A]
    * 输出参数：None
    * 返 回 值：True
    **************************************************************************'''
    def HT1621xWrAllData(self, _addr, _htdata):
        FW = bin(FLAG_WRITE)[2:]
        ad = bin(_addr ^ (1 << 6))[3:]  # 将16进制值转化为   6位二进制字符串
        self.CS.off()
        sleep_us(4)
        self._wrData(FW)  # 写命令
        self._wrData(ad)  # 写地址
        for da in _htdata:
            dat = bin(da ^ (1 << 4))[3:]  # 将16进制值转化为4位二进制字符串
            self._wrData(dat)  # 写数据
        self.CS.on()
        sleep_us(4)
        return True


    '''*************************************************************************
    * 功   能：显示所有显示字段
    * 说   明：
    * 输入参数：
              _addr: 数据起始地址 | str | hex | 0x00~0x1F | eg. 0x00
              _nbit: seg位数    | in  | de  | 1~32      | eg: 1
    * 输出参数：None
    * 返 回 值：True
    **************************************************************************'''
    def ALLSHOW(self, _addr, _nbit):
        htdata = []
        for i in range(_nbit):
            htdata.append(0x0F)
        self.HT1621xWrAllData(_addr, htdata)
        return True

    '''*************************************************************************
    * 功   能：清除屏幕全部显示
    * 说   明：
    * 输入参数：
              _addr: 数据起始地址  | str  | hex | 0x00~0x1F | eg. 0x00
              _nbit: seg位数     | de   | de  | 1~32      | eg: 2
    * 输出参数：None
    * 返 回 值：True
    **************************************************************************'''
    def ALLCLEAR(self, _addr, _nbit):
        htdata = []
        for i in range(_nbit):
            htdata.append(0x00)
        self.HT1621xWrAllData(_addr, htdata)
        return True


    '''*************************************************************************
    * 功   能：打开液晶显示
    * 说   明：
    * 输入参数：None
    * 输出参数：None
    * 返 回 值：True
    **************************************************************************'''
    def LCDON(self):
        self.HT1621xWrCmd(CMD_LCDON)
        return True


    '''*************************************************************************
    * 功   能：关闭液晶显示
    * 说   明：
    * 输入参数：None
    * 输出参数：None
    * 返 回 值：True
    **************************************************************************'''
    def LCDOFF(self):
        self.HT1621xWrCmd(CMD_LCDOFF)
        return True


    '''*************************************************************************
    * 功   能：蜂鸣器驱动
    * 说   明：设置并驱动蜂鸣器响一段时间，单位为秒
    * 输入参数：
              _t: 持续时间 | in | de |    | eg. 1
    * 输出参数：None
    * 返 回 值：True
    **************************************************************************'''
    def HTBEEP(self, _t):
        self.HT1621xWrCmd(CMD_TONEON)
        sleep(_t)
        self.HT1621xWrCmd(CMD_TONEOFF)
        return True
