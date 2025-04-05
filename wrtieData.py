import httpApi
import time
import os

currentGenlockFormat=""
currentBackendFormat=""
def writetoCsv(nanoFormat,hitomiFormat,beFormat,hitomiInfo,bestatus,icount):
    
    sorted_items = sorted(hitomiInfo.items()) 
    timestamp = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    if os .path.exists("csv/"):
        os.makedirs('csv')
    # 
    with open (f"csv/{nanoFormat}-{beFormat}.csv","w" if icount==0 else 'a') as f:
        if icount==0:
            #write header
            f.write('time,')
            f.write('nanoFormat,')
            f.write('hitomiFormat,')
            f.write('beFormat,')
            for x in bestatus:
                f.write(f"{x},")
            for x in sorted_items:
                f.write(f"{x[0]},")
            f.write("\n")
        
        f.write(f'{timestamp},')
        f.write(f'{nanoFormat},')
        f.write(f'{hitomiFormat},')
        f.write(f'{beFormat},')
        for x in bestatus:
            f.write(f"{bestatus[x]},")

        for x in sorted_items:
            f.write(f'{x[1]},')
        f.write('\n')
                

        

def logData(nanoFormat,beFormat,duration):
    seconds = duration

    print(f"Record {seconds}s")

    lastHitomiinfo = {}
    icount=0
    while seconds > 0:
        hitomiInfo = httpApi.getInfomationFromHitomi()
        bestatus = httpApi.fetchStatusOnBE()
        if hitomiInfo != lastHitomiinfo:
            writetoCsv(nanoFormat,httpApi. getGenlockFormatFromHitomi(),beFormat,hitomiInfo , bestatus,icount=icount)
        lastHitomiinfo = hitomiInfo
        icount+=1
        seconds -= 1
        time.sleep(1)



if __name__=="__main__":
    logData('test','test',10)

    