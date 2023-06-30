#水表

class WaterMeter:
    def __init__(self,addr,distance,modbus) -> None:
        """初始化类WaterMeter

        Args:
            addr (int): 设备id
            distance (int): 设备与主机之间的物理距离
            modbus(modbusDevise):485总线
        """
        self.addr=addr
        self.distance=distance
        self.modbus=modbus


    # 水表转换
    def Uint16ToDec(data) -> float:
        data = data[3:7]
        data = (data[3] + data[2]*256 + data[1]*256*256 + data[0]*256*256*256)/10
        return data

    async def getCumulativeDischarge(self):
        RevMessFlag,message =await self.modbus.send_cmd(self.addr,func=3,start_addr=1,data=2,distance=self.distance,timeout=1)
        if RevMessFlag is True:
            data=Uint16ToDec(message)
            return data
        else:
            raise Exception("WaterMeter getCumulativeDischarge error--"+", flag="+str(RevMessFlag)+","+message) 
        




