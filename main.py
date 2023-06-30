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

waterMeters = [waterMeter1,waterMeter2,waterMeter3,waterMeter4,waterMeter5,waterMeter6,waterMeter7]

erha = WDT(timeout=5000)

lljNumber = None
wm_level = [-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0]


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
  
  
async def updata_data_on_ali_iot(flag):
    global updataDataFlag
    count = 0
    while flag:
        try:
            if count==4:
                raise Exception("上传失败")
            count+=1
            if wm_level == [-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0]or not lljNumber:
                await asyncio.sleep(1)
                continue
            js = create_upload_json(["lxq_llj","wm0","wm1","wm2","wm3","wm4","wm5","wm6","sw1","sw2","sw3","sw4","sw5","sw6","sw7","sw8","sw9","sw10","sw11","sw12","sw13","sw14","sw15","sw16","sw17","sw18"],
                            [lljNumber,wm_level[0],wm_level[1],wm_level[2],wm_level[3],wm_level[4],wm_level[5],wm_level[6],sw1.value(),sw2.value(),sw3.value(),sw4.value(),sw5.value(),sw6.value(),sw7.value(),sw8.value(),sw9.value(),sw10.value(),sw11.value(),sw12.value(),sw13.value(),sw14.value(),sw15.value(),sw16.value(),sw17.value(),sw18.value()])
            # 将json格式转换成byte格式
            js = js.encode()
            print(js)
            await modbus2.uart_send(js)

        except Exception as e:
            loginfo("updata_data_on_ali_iot",4,str(e))
        finally:
            await asyncio.sleep(2)        


async def get_wm_level(flag):
    global get_wm_levelFlag
    while flag:
        try:
            for i in range(7):
                waterMeter0=waterMeters[i]
                level=waterMeter0.getCumulativeDischarge()
                wm_level[i]=level
            print("wm_level:",wm_level)
        except Exception as e:
            loginfo("get_wm_level",4,str(e))
        finally:
            await asyncio.sleep_ms(100)


async def get_lljNumber(flag):
    global get_lljNumberFlag
    while flag:
        try:
            status=await ballFlowMeter.get_llj_data()
            print("status:",status)
            lljNumber=status
        except Exception as e:
            loginfo("get_lljNumber",4,str(e))
        finally:
            await asyncio.sleep_ms(100)


async def main():
    get_lljNumberFlag=True
    get_wm_levelFlag=True
    updataDataFlag=True
    mainFlag=True

    asyncio.create_task(get_lljNumber(get_lljNumberFlag))
    asyncio.create_task(get_wm_level(get_wm_levelFlag))
    asyncio.create_task(updata_data_on_ali_iot(updataDataFlag))
    
    while mainFlag:
        await asyncio.sleep(2)
        erha.feed()
        gc.collect()
        print("memery free:", gc.mem_free(), "memery alloc:", gc.mem_alloc())
        
        
try:
    asyncio.run(main())
except KeyboardInterrupt:
    mainFlag=False
    get_lljNumberFlag=False
    get_wm_levelFlag=False
    updataDataFlag=False

