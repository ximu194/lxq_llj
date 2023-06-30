#连续球流量计

class BallFlowMeter:
    def __init__(self,addr,distance,modbus) -> None:
        """初始化类BallFlowMeter

        Args:
            addr (int): 设备id
            distance (int): 设备与主机之间的物理距离
            modbus(modbusDevise):485总线
        """
        self.addr=addr
        self.distance=distance
        self.modbus=modbus


    def process_llj_data(self,data):
        zheng = data[3] * 256 + data[4] + data[5] * 256 * 256 * 256 + data[6] * 256 * 256 
        xiao = data[7] * 256 + data[8] + data[9] * 256 * 256 * 256 + data[10] * 256 * 256
        xiao = xiao /1000
        return zheng+xiao

    async def get_llj_data(self):
        RevMessFlag,message =await self.modbus.send_cmd(self.addr,func=4,start_addr=107,data=4,distance=self.distance,timeout=1)
        if RevMessFlag is True:
            data = self.process_llj_data(message)
            return data
        else:
            raise Exception("get_llj_data error--"+", flag="+str(RevMessFlag)+","+message) 
        





