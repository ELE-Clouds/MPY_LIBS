from ht1621x import HT1621B
from gdc03849 import GDC03849

from machine import Pin
from dht import DHT11
from time import sleep

CS = Pin("A0")
RD = Pin("A1")
WR = Pin("B0")
DA = Pin("B1")

ht  = HT1621B(CS, RD, WR, DA)
gdc = GDC03849(ht)


# DHT11引脚设置
dhtgnd = Pin('Y10',Pin.OUT,Pin.PULL_DOWN)
dhtvcc = Pin('Y9',Pin.OUT,Pin.PULL_UP)
dhts   = Pin('Y8')
dhtgnd.off()
dhtvcc.on()
sleep(2)
dt = DHT11(dhts)
te1 = 0
dh1 = 0
while True:
    dt.measure()
    te0 = dt.temperature()   # 温度
    dh0 = dt.humidity()      # 湿度
    if te0 != te1 or dh0 != dh1:
        if te0 != te1:
            te1 = te0
            gdc.viewTemp(te1)
        if dh0 != dh1:
            dh1 = dh0
            gdc.viewRH(dh1)
        print('当前温度：', te1, ' | 当前湿度：', dh1)
    sleep(1)
