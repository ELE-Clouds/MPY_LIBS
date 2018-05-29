# HT1621B 驱动使用说明


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
