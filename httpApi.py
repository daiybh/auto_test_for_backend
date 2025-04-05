from config import *
import time
import requests
import logging

def getHitomiURL():
    return f'http://{HITOMI_ANALYSER_HOST}/cgi-bin/mbServerSide.ccgi?func=statusPoll&menuName=analyser'

def switch_ref():
    ref1=f"cgi-bin/mbServerSide.ccgi?func=controlChange&name=xSdiTiming&value={HITOMi_ANALYSER_REF_PORT}&vControl=xSdiTransRef"
    url="http://"+HITOMI_ANALYSER_HOST+"/"+ref1
    requests.get(url)
    time.sleep(1)


def getElemetValue(alltext,elemetName):
    b = alltext.find(elemetName)
    c = alltext.find('document.getElementById',b)
    d = alltext[b:c]
    e = d.split('=')
    return e[1][2:-2]


def correctFormat(format):
    if format.startswith("525"):
        return 'NTSC'
    if format.startswith("625"):
        return 'PAL'   
    
    if format.endswith('29'):
        format+='97'
    
    elif format.endswith('23'):
        format+='98'
    
    elif format.endswith('59'):
        format+='94'
    if format=='1080i25':
        return '1080I50'
    #if format=='1080p25':
    #    return '1080P50'
    #if format=='720p25':
    #    return '720P50'
    
    return format.upper()

def getGenlockFormatPort():
    return f'xSdiTiming:rxFmt${HITOMi_ANALYSER_REF_PORT}'

def getGenlockFormatFromHitomi():
    r = requests.get(getHitomiURL())
    moduleFormat=getElemetValue(r.text,getGenlockFormatPort())      
    return moduleFormat

def getInfomationFromHitomi():
    r = requests.get(getHitomiURL())
    #genlockoffset  xSdiTiming:transTiming$2  -457 ln  0834 px
    #e2etiming      xSdiTiming:contTiming$2 0,1 or 0123   0.0 
    #avtiming       audioReport:avTiming$0 0-15   
    #rxFmt          xSdiTiming:rxFmt$0 
    rxFmt=[]
    ret={}
    try:
        for i in range(4):
            ret[f'transTiming{(i+1)}']=getElemetValue(r.text,f"xSdiTiming:transTiming${i}")
            ret[f'contTiming{(i+1)}']=getElemetValue(r.text,f"xSdiTiming:contTiming${i}")
            ret[f'rxFmt{(i+1)}']=getElemetValue(r.text,f"xSdiTiming:rxFmt${i}")

            #trastiming.append( getElemetValue(r.text,f"xSdiTiming:transTiming${i}"))
            #e2etiming.append( getElemetValue(r.text,f"xSdiTiming:contTiming${i}"))
            #rxFmt.append( getElemetValue(r.text,f"xSdiTiming:rxFmt${i}"))
    except:
        pass
    
    for i in range(16):
        #avtiming.append( getElemetValue(r.text,f"audioReport:avTiming${i}"))
        ret[f'avTiming{(i+1)}']=getElemetValue(r.text,f"audioReport:avTiming${i}")

   # return {"trastiming":trastiming,"e2etiming":e2etiming,"avtiming":avtiming,"rxFmt":rxFmt}
    return ret
    


def changeHitomiSourceFormat(isSDStandard, beFormatObj):
    hitomiFormatValue = beFormatObj["hitomiValue"]

    changeUrl = f'http://{hitomi_source_ip}/cgi-bin/mbServerSide.ccgi?func=controlChange&name=videoGeneration&value={hitomiFormatValue}&vControl=opFormat4K'
    response = requests.get(changeUrl)

    print(
        f"selected Hitomi source format: {beFormatObj['name']}[{hitomiFormatValue}]")


def changeBEFormat(beFormatObj):
    backend_watchdog_url = f"http://{backend_IP}:28100"
    response = requests.get(backend_watchdog_url + "/ExportConfig")
    if (response.status_code == 200):
        #print(response.text)
        data = response.json()
        data["GENERAL_CONFIG_Video_Format"] = beFormatObj["value"]

        response = requests.post(
            backend_watchdog_url + "/ImportConfig", json=data)
        if (response.status_code == 200):
            currentBackendFormat = beFormatObj["name"]
            print("Backend format changed to  "+ beFormatObj["name"])
            time.sleep(2)
        else:
            print("Error changing backend format to",
                  beFormatObj["name"], " status code:", response.status_code)
    else:
        print("Error exporting backend config, status code:", response.status_code)

def waitBE_Shutdown():
    logging.info("waitBE_Shutdown")
    for i in range(15):
        try:
            r = requests.get("http://{backend_IP}:28100/GetBackendStatus")
            if r.json()["status"] == "Backend_Not_Start":
                break
        except:
            pass
        time.sleep(1)


def restartBE():
    logging.info("restartBE")
    backend_watchdog_url =f"http://{backend_IP}:28100"
    response = requests.get(backend_watchdog_url + "/StopBackend")
    if (response.status_code == 200):
        waitBE_Shutdown()
        response = requests.get(backend_watchdog_url + "/StartBackend")
        if (response.status_code == 200):
           waitBEStartWell()
        else:
            print("Error starting backend")
    else:
        print("Error stopping backend")


def waitBEStartWell(timeout_in_minutes=5*60):
    logging.info("waitBEStartWell")
    for i in range(timeout_in_minutes): #wait for 5 minutes
        bestatus = fetchStatusOnBE()
        if bestatus!=None:
            if bestatus['genlockAverage']>10:
                break
        time.sleep(0.5)

def fetchStatusOnBE():
    
    try:
        ret={}
        url =  f"http://{backend_IP}:2888/genlockstatus"
        response = requests.get(url)
    
        data = response.json()
        ret['genlockAverage'] = float(data["average"][:5])
        ret['refStatus'] = data["status"]
    
        url = f"http://{backend_IP}:2888/camerastatus"
        response = requests.get(url)
    
        data = response.json()
        
        ret['loopcnt']=data['loopcnt'] if 'loopcnt' in data else 0
        ret['mis'] = data["cam0"]["miss"]
        ret['nov'] = data["cam0"]["nov"]
        
        return ret
    except Exception as e:
        pass
    return None



if __name__=="__main__":
    print(getGenlockFormatFromHitomi())
    
    #from itemDef import *
    #changeBEFormat( backendStandards[0])
    a= getInfomationFromHitomi()
    print(fetchStatusOnBE())
    waitBEStartWell()

