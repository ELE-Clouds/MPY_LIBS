MicroPython Device LIB
======
HT1621x 驱动使用说明
------

**驱动文件：ht1621x.py**

![GDC03849 段式液晶][gdc]

*[HT1621B][ht]驱动[GDC03849][gdcl]段码液晶的方法*<BR>

<pre><code python>
# 示例代码
from ht1621x import HT1621B
from gdc03849 import GDC03849
from machine import Pin

# 引脚定义
CS = Pin("A0")
RD = Pin("A1")
WR = Pin("B0")
DA = Pin("B1")

ht  = HT1621B(CS, RD, WR, DA)
gdc = GDC03849(ht)

# 在LCD中显示温度
gdc.viewTemp(123.45)

# 在LCD中显示湿度
gdc.viewRH(123.45)
</code></pre>






[gdc]:./img/gdc03849.png 'GDC03849段式液晶'
[ht]:http://www.holtek.com.cn 'HOLTEK'
[gdcl]:https://www.good-display.cn '大连佳显'
