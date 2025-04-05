
import sys
import logging
from logging.handlers import RotatingFileHandler

# 配置 logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  - %(message)s',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=1e6, backupCount=3),
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

# 定义重定向类
class PrintToLogger:
    def __init__(self, logger, level=logging.INFO):
        self.logger = logger
        self.level = level

    def write(self, message):
        if message.strip():  # 忽略空行
            self.logger.log(self.level, message.rstrip())

    def flush(self):
        pass  # 必须实现

# 全局替换 sys.stdout 和 sys.stderr
sys.stdout = PrintToLogger(logging.getLogger("STDOUT"))
sys.stderr = PrintToLogger(logging.getLogger("STDERR"), level=logging.ERROR)


import NanoApp  
import httpApi
from config import *
from backendStandards import *
import time

print("----start------")
na=NanoApp.NanoAPP()
import json
from pathlib import Path

def loadAlradyDoneList():
    

    file_path = Path('alreadyDoneList.json')

    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    return data
                except json.JSONDecodeError as e:
                    pass
    except Exception as e:
        pass
    return {}

def writeAlreadyDoneListToFile(adlist):
    file_path = Path('alreadyDoneList.json')
    with open (file_path,'w',encoding='utf-8') as f:
        json.dump(adlist,f,indent=4)

def runBackend(nanoFormat):
    nanotext = nanoFormat['nanotext']
    alreadyDoneList = loadAlradyDoneList()
    for beFormatObj in backendStandards:
        
        beforamtName = beFormatObj['name']
        if nanotext in alreadyDoneList:
            if beforamtName in alreadyDoneList[nanotext]:
                print(f"nano:{nanotext} beformat:{beforamtName} already done")
                continue
        
        f = httpApi.getGenlockFormatFromHitomi()
        logging.info(f"----start nanoFormat:{nanoFormat} beobj:{beFormatObj}")
         # beFormatObj["value"]
        httpApi.changeHitomiSourceFormat(False, beFormatObj)
        httpApi.changeBEFormat(beFormatObj)
        httpApi.restartBE()
        #httpApi.waitBEStartWell()
        
       
        #logData(recordDuration)
        from wrtieData import logData
        logData(nanotext,beforamtName,recordDuration)
        
        if nanotext not in alreadyDoneList:
            alreadyDoneList[nanotext]=[]
        alreadyDoneList[nanotext].append(beforamtName)
        writeAlreadyDoneListToFile(alreadyDoneList)


def runSD():
    print("*******runSD*********")
    for x in NanoApp.genlockSDStandardMap:
        print(f"sd-----{x}")
        na.switchtoSD(x['nanotext'])
        f = httpApi.getGenlockFormatFromHitomi()
        if f!= x['hitomitext']:
            print(f"setGenlock Faild.nano: {x['nanotext']} want:{x['hitomitext']}  hitomi:{f}")
            continue
        runBackend(x)
            

def tryRun(x):
    print(x)
    for i in range(5):
        na.switchtoHD(x['nanotext'])
        f = httpApi.getGenlockFormatFromHitomi()
        if f!= x['hitomitext']:
            print(f"setGenlock Faild.nano: {x['nanotext']} want:{x['hitomitext']}  hitomi:{f}")
            continue
        runBackend(x)
            
    
def runHD(): 
    print("*******runHD*********")
    for x in NanoApp.genlockHDStandardMap:
        tryRun(x)

runSD()
runHD()
logging.info("over")
