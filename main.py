from machine import UART, Pin, WDT
import utime
import uasyncio as asyncio
import gc
import json

from log import loginfo
from modbusDevice import modbusDevice
from ballFlowMeter import BallFlowMeter
from waterMeter import WaterMeter

modbus1=modbusDevise(1,9600,4,5, 8, None, 1)
modbus2=modbusDevise(0,115200,0,1, 8, None, 1)

sw1 = Pin(2, Pin.IN)
sw2 = Pin(3, Pin.IN)
sw3 = Pin(6, Pin.IN)
sw4 = Pin(7, Pin.IN)
sw5 = Pin(8, Pin.IN)
sw6 = Pin(9, Pin.IN)
sw7 = Pin(10, Pin.IN)
sw8 = Pin(11, Pin.IN)
sw9 = Pin(12, Pin.IN)
sw10 = Pin(13, Pin.IN)
sw11 = Pin(14, Pin.IN)
sw12 = Pin(15, Pin.IN)
sw13 = Pin(16, Pin.IN)
sw14 = Pin(17, Pin.IN)
sw15 = Pin(18, Pin.IN)
sw16 = Pin(19, Pin.IN)
sw17 = Pin(20, Pin.IN)
sw18 = Pin(21, Pin.IN)

ballFlowMeter=BallFlowMeter(8,150,modbus1)
waterMeter1=WaterMeter(10,400,modbus1)
waterMeter2=WaterMeter(11,350,modbus1)
waterMeter3=WaterMeter(12,300,modbus1)
waterMeter4=WaterMeter(13,250,modbus1)
waterMeter5=WaterMeter(14,200,modbus1)
waterMeter6=WaterMeter(15,150,modbus1)
waterMeter7=WaterMeter(16,100,modbus1)

erha = WDT(timeout=5000)

number = 0
wm = [0,0,0,0,0,0,0]


def create_upload_json(name,value, method="thing.event.property.post"):
    time_stamp = int(utime.time())
    js = {}
    js["id"] = time_stamp
    js["version"] = "1.0"
    js["params"] = {}
    js["sys"] = {}
    js["sys"]["ack"] = 0
    js["method"] = method
    for i in range(len(name)):
        js["params"][name[i]] = value[i]
    # 返回json格式
    return json.dumps(js)
  








