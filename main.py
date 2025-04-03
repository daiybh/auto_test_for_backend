
# Quick start
# 
# 1. install python3
# Be sure add python folders to PATH while installing python3, so that you can run python in the command prompt.
# 
# 2. install pywinauto
# Use the following command to install pywinauto in the command prompt:
# pip install pywinauto
# use a proxy if needed, for example:
# pip install pywinauto --proxy http://localhost:58591
#
# 3. install playwright
# Use the following command to install playwright in the command prompt:
# pip install playwright
# use a proxy if needed, for example:
# pip install playwright --proxy http://localhost:58591
#
# 4. init playwright
# Use the following command to initialize playwright in the command prompt:
# playwright install
#
# 5. inistall requests
# pip install requests
#
# 6. change the "hitomi_url" to the correct url
# 
# 7. run the script in the command prompt
# python main.py
# 
# 8. change the target formats as needed
# change the array "targetSDStandards" and "targetHDStandards" to contains all formats that you want to test,
# the script will select them one by one and run the batch file
# Be sure to update the "hitomiSDStandards" and "hitomiHDStandards" arrays to contains the corresponding formats

import time
from pywinauto import Application
import subprocess
from playwright.sync_api import sync_playwright
import requests
import sys

backend_url = "http://192.168.0.133"
hitomi_url = "http://192.168.0.102/"
hitomi_source_url = "http://192.168.0.101/"

audio_channel_count = 4
output_count = 2
recordDuration = 600

backendStandards = [
    { 
        "name": "1080i 50",
        "value": 1,
        "hitomiValue":13
        },
    { 
        "name": "1080i 59.94",
        "value": 2,
        "hitomiValue":14
        },
    { 
        "name": "1080p 23.98",
        "value": 23,
        "hitomiValue":16
        },
    { 
        "name": "1080p 24",
        "value": 21,
        "hitomiValue":17
        },
    { 
        "name": "1080p 25",
        "value": 4,
        "hitomiValue":18
        },
    { 
        "name": "1080p 29.97",
        "value": 5,
        "hitomiValue":19
        },
    { 
        "name": "1080p 50",
        "value": 7,
        "hitomiValue":21
        },
    { 
        "name": "1080p 59.94 ",
        "value": 8,
        "hitomiValue":22
        },
    { 
        "name": "720p 50",
        "value": 12,
        "hitomiValue":8
        },
    { 
        "name": "720p 5994",
        "value": 13,
        "hitomiValue":9
        },
    { 
        "name": "1080psf 29.97",
        "value": 33,
        "hitomiValue":27
        },
    #{ 
    #    "name": "UHD 4Kp50",
    #    "value": 18,
    #    "hitomiValue":29
    #    },
    #{ 
    #    "name": "UHD 4Kp59.94",
    #    "value": 19,
    #    "hitomiValue":31
    #    },
    ]

targetSDStandards = [
    "NTSC", 
    "PAL 25", 
    ]

targetHDStandards = [
    "1080i 50",
    "1080i 59.94",
    "1080p 23.98",
    "1080p 24",
    "1080p 25",
    "1080p 29.97",
    "1080p 50",
    "1080p 59.94",
    "720p 23.98",
    "720p 24",
    "720p 25",
    "720p 29.97",
    "720p 50",
    "720p 59.94",
    ]

targetHDBaseStandards = [
    ["1080i 50"],                       # "1080i 50",
    ["1080i 59.94"],                    # "1080i 59.94",
    ["1080i 47.95"],                    # "1080p 23.98",
    ["1080i 48"],                       # "1080p 24",
    ["1080i 50"],                       # "1080p 25",
    ["1080i 59.94"],                    # "1080p 29.97",
    ["1080i 50"],                       # "1080p 50",
    ["1080i 59.94"],                    # "1080p 59.94 ",
    ["1080i 47.95", "1080p 23.98"],     # "720p 23.98",
    ["1080i 48", "1080p 24"],           # "720p 24",
    ["1080i 50", "1080p 25"],           # "720p 25",
    ["1080i 59.94", "1080p 59.94"],     # "720p 29.97",
    ["1080i 50", "1080p 50"],           # "720p 50",
    ["1080i 59.94", "1080p 59.94"],     # "720p 5994",
    ]

hitomiSDActualStandards = [
    "525i29",
    "625i25",
]

hitomiHDActualStandards = [
    "1080i25",      # "1080i 50",
    "1080i29",      # "1080i 59.94",
    "1080p23",     # "1080p 23.98",
    "1080p24",     # "1080p 24",
    "1080p25",      # "1080p 25",
    "1080p29",      # "1080p 29.97",
    "1080p25",      # "1080p 50",
    "1080p29",      # "1080p 59.94 ",
    "720p23",      # "720p 23.98",
    "720p24",       # "720p 24",
    "720p25",       # "720p 25",
    "720p29",       # "720p 29.97",
    "720p25",       # "720p 50",
    "720p29",       # "720p 5994",
]

hitomiSDStandardValues = [
    "1", #"525i29", NTSC
    "2", #"625i25", PAL 25
]

hitomiHDStandardValues = [
    "13", #"1080i25"
    "14", #"1080i29"
    "24", #"1080sf23"
    "25", #"1080sf24"
    "18", #"1080p25"
    "19", #"1080p29"
    "21", #"1080p50": "", # fail
    "22", #"1080p59.94": "", # fail
    "3", #"720p23.98,": "", # fail
    "4", #"720p24": "", # fail
    "5", #"720p25": "", # fail
    "6", #"720p29.97": "", # fail
    "8", #"720p50": "", # fail
    "9", #"720p59.94": "", # fail
]
    

currentGenlockFormat = "NTSC"
currentBackendFormat = "1080i 50"
genlockAverage = ""
refStatus = ""
mis = 0
nov = 0

skippedFormats = []
specifiedFormats = []

def find_window(title):
    try:
        app = pywinauto.Desktop(backend="uia").window(title=title)
        if app.exists():
            return app
    except Exception as e:
        print(f"Error finding window: {e}")
    return None

def click_button(window, button_name):
    try:
        button = window.child_window(title=button_name, control_type="Button")
        button.click()
    except Exception as e:
        print(f"Error clicking button '{button_name}': {e}")

def click_list_item(list_element, index=0):
    try:
        items = list_element.children()
        if items and len(items) > index:
            items[index].click_input()
    except Exception as e:
        print(f"Error clicking list item: {e}")

def findBaseHDStandard(standardName, listItems):
    for standard in listItems:
        if standard.window_text() == standardName:
            return standard
        
    return None

def main():
    global currentGenlockFormat
    app = Application(backend="uia").connect(title="Rosendahl nanosyncs HD  3.0")

    # Get the main window
    window = app.window(title="Rosendahl nanosyncs HD  3.0")
    if window:
        click_button(window, "Connect")
        time.sleep(5)
        
        list_element = window.ListBox4
        if list_element:
            for item in list_element.children():
                itemText = item.window_text()
                if not (itemText in targetSDStandards):
                    continue
                if not (itemText in specifiedFormats):
                    continue
                itemIndex = targetSDStandards.index(itemText)

                print("select SD standard:", itemText)
                item.click_input()
                currentGenlockFormat = itemText
                
                #"VIDEO OUT 1-3", "VIDEO OUT 4", "VIDEO OUT 5", "VIDEO OUT 6"
                click_list_item(window.ListBox6, 0)
                click_list_item(window.ListBox7, 0)
                click_list_item(window.ListBox8, 0)
                click_list_item(window.ListBox9, 0)

                time.sleep(3)
                
                
                actualFormat = fetchHitomiFormat(page)
                if(actualFormat == hitomiSDActualStandards[itemIndex]):                    
                    for beFormatObj in backendStandards:
                        changeHitomiSourceFormat(True, beFormatObj) # beFormatObj["value"]
                        changeBEFormat(beFormatObj)
                        restartBE()
                        fetchStatusOnBE()
                        logData(recordDuration)
                        time.sleep(2)
                else:
                    print(f"*** failed *** Hitomi Source:{targetHDStandards[itemIndex]}[{hitomiHDStandardValues[itemIndex]}], Genlock:{currentGenlockFormat}, Hitomi Ref:{actualFormat}, BE:{currentBackendFormat}", )

        list_element = window.ListBox10
        if list_element:
            listItems = list_element.children();
            for item in listItems:
                itemText = item.window_text();
                if not (itemText in targetHDStandards):
                    continue
                if not (itemText in specifiedFormats):
                    continue
                
                itemIndex = targetHDStandards.index(itemText)
                
                print("select HD standard:", itemText)

                hasSwitched = False
                for i in range(5):
                    baseStandardList = targetHDBaseStandards[itemIndex]
                    for baseStandard in baseStandardList:
                        baseItem = findBaseHDStandard(baseStandard, listItems)
                        print("select base standard:", baseStandard)
                        baseItem.click_input()
                        
                        #"VIDEO OUT 1-3", "VIDEO OUT 4", "VIDEO OUT 5", "VIDEO OUT 6"
                        click_list_item(window.ListBox6, 1)
                        click_list_item(window.ListBox7, 1)
                        click_list_item(window.ListBox8, 1)
                        click_list_item(window.ListBox9, 1)
                        
                        time.sleep(1)
                        
                    item.click_input()
                    currentGenlockFormat = itemText
                    
                    #"VIDEO OUT 1-3", "VIDEO OUT 4", "VIDEO OUT 5", "VIDEO OUT 6"
                    click_list_item(window.ListBox6, 1)
                    click_list_item(window.ListBox7, 1)
                    click_list_item(window.ListBox8, 1)
                    click_list_item(window.ListBox9, 1)
                    
                    time.sleep(3)

                    actualFormat = fetchHitomiFormat(page)
                    if(actualFormat == hitomiHDActualStandards[itemIndex]):
                        hasSwitched = True

                        print("select HD standard:", itemText)
                        item.click_input()
                        currentGenlockFormat = itemText
                        break
                    else:
                        print(f"expect format:{hitomiHDActualStandards[itemIndex]}, actual format: {actualFormat}")
                        print("switching failed, retrying...", i+1)
                        time.sleep(1)

                if not hasSwitched:
                    skippedFormats.append(itemText)
                    continue
                
                time.sleep(3)

                for beFormatObj in backendStandards:
                    changeHitomiSourceFormat(False, beFormatObj) # beFormatObj["value"]
                    changeBEFormat(beFormatObj)
                    restartBE()
                    fetchStatusOnBE()
                    logData(recordDuration)
                    time.sleep(2)
                    
        print("Tests finished")        
        if len(skippedFormats) > 0:
            print("Skipped formats:", skippedFormats)
        else:
            print("All formats passed")
    else:
        print("Window not found")

def test():
    # Connect to the MFC app (by title or process ID)
    app = Application(backend="win32").connect(title="Rosendahl nanosyncs HD  3.0")

    # Get the main window
    main_window = app.window(title="Rosendahl nanosyncs HD  3.0")

    # Print all available controls (debugging)
    #main_window.print_control_identifiers()

    # Find the ListBox by control type
    list_box = main_window.ListBox4

    # If the ListBox is found, print its content
    if list_box.exists():
        print("ListBox4 Found!")
        for item in list_box.item_texts():
            print("Item:", item)
    else:
        print("ListBox4 not found")

    list_box = main_window.ListBox6

    # If the ListBox is found, print its content
    if list_box.exists():
        print("ListBox6 Found!")
        for item in list_box.item_texts():
            print("Item:", item)
    else:
        print("ListBox6 not found")

    list_box = main_window.ListBox7

    # If the ListBox is found, print its content
    if list_box.exists():
        print("ListBox7 Found!")
        for item in list_box.item_texts():
            print("Item:", item)
    else:
        print("ListBox7 not found")

    list_box = main_window.ListBox8

    # If the ListBox is found, print its content
    if list_box.exists():
        print("ListBox8 Found!")
        for item in list_box.item_texts():
            print("Item:", item)
    else:
        print("ListBox8 not found")

    list_box = main_window.ListBox9

    # If the ListBox is found, print its content
    if list_box.exists():
        print("ListBox9 Found!")
        for item in list_box.item_texts():
            print("Item:", item)
    else:
        print("ListBox9 not found")

    list_box = main_window.ListBox10

    # If the ListBox is found, print its content
    if list_box.exists():
        print("ListBox10 Found!")
        for item in list_box.item_texts():
            print("Item:", item)
    else:
        print("ListBo106 not found")

def fetchHitomiFormat(page):
    page.goto(hitomi_url)  # Wait for JS to load
    page.wait_for_timeout(1000)

    page.locator("#button-analyser").click()
    page.wait_for_timeout(1000)
    

    # Wait for content to appear
    page.wait_for_selector('[id="xSdiTiming:rxFmt$5"]', timeout=1000)

    # Get content by ID
    content = page.locator('[id="xSdiTiming:rxFmt$5"]').inner_text()

    return content

def changeHitomiSourceFormat(isSDStandard, beFormatObj):
    hitomiFormatValue = beFormatObj["hitomiValue"]
        
    changeUrl= f'{hitomi_source_url}cgi-bin/mbServerSide.ccgi?func=controlChange&name=videoGeneration&value={hitomiFormatValue}&vControl=opFormat4K'
    response = requests.get(changeUrl)
    
    print(f"selected Hitomi source format: {beFormatObj['name']}[{hitomiFormatValue}]")
    time.sleep(1)

def changeBEFormat(beFormatObj):
    global currentBackendFormat
    backend_watchdog_url = backend_url + ":28100"
    response = requests.get(backend_watchdog_url + "/ExportConfig")
    if (response.status_code == 200) :
        data = response.json()
        data["GENERAL_CONFIG_Video_Format"] = beFormatObj["value"]

        response = requests.post(backend_watchdog_url + "/ImportConfig", json=data)
        if (response.status_code == 200) :
            currentBackendFormat = beFormatObj["name"]
            print("Backend format changed to", beFormatObj["name"])
            time.sleep(2)
        else:
            print("Error changing backend format to", beFormatObj["name"], " status code:", response.status_code)
    else:
        print("Error exporting backend config, status code:", response.status_code)

def restartBE():
    backend_watchdog_url = backend_url + ":28100"
    response = requests.get(backend_watchdog_url + "/StopBackend")
    if (response.status_code == 200) :
        time.sleep(15)
        response = requests.get(backend_watchdog_url + "/StartBackend")
        if (response.status_code == 200) :
            time.sleep(15)            
        else:
            print("Error starting backend")
    else:
        print("Error stopping backend")

def fetchStatusOnBE():
    global genlockAverage
    global refStatus
    global mis
    global nov

    url = backend_url + ":2888/genlockstatus"
    response = requests.get(url)
    if (response.status_code == 200) :
        data = response.json()
        genlockAverage = data["average"]
        refStatus = data["status"]
    else:
        print("Error fetching genlockAverage and refstatus")
        
    url = backend_url + ":2888/camerastatus"
    response = requests.get(url)
    if (response.status_code == 200) :
        data = response.json()
        mis = data["cam0"]["miss"]
        nov = data["cam0"]["nov"]
    else:
        print("Error fetching genlockAverage and refstatus")

def logData(duration):
    page.goto(hitomi_url)  # Wait for JS to load
    page.wait_for_timeout(1000)

    page.locator("#button-analyser").click()
    page.wait_for_timeout(1000)
    
    seconds = duration
    
    refOffsetArray = []
    e2eTimingArray = []
    avTimingArray = []

    lastRefOffset = [""] * output_count
    lastE2ETiming = [""] * output_count
    lastAVTiming = [""] * audio_channel_count

    print(f"Record {seconds}s")
    while seconds > 0:
        print(f"{seconds}s left", end='\r')
        timestamp =  time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        
        for i in range(output_count):
            refOffset = page.locator(f'[id="xSdiTiming:transTiming${i}"]').inner_text()
            
            if refOffset != lastRefOffset[i]:
                lastRefOffset[i] = refOffset
                refOffsetArray.append({"cnl": i, "value": refOffset, "timestamp": timestamp})
                #print(f"#{i} Ref Offset:{refOffset}")

            e2eTiming = page.locator(f'[id="xSdiTiming:contTiming${i}"]').inner_text()
            if e2eTiming != lastE2ETiming[i]:
                lastE2ETiming[i] = e2eTiming
                e2eTimingArray.append({"cnl": i, "value": e2eTiming, "timestamp": timestamp})
                #print(f"#{i} E2E timting:{e2eTiming}")

        for i in range(audio_channel_count):
            avTiming = page.locator(f'[id="audioReport:avTiming${i}"]').inner_text()
            if avTiming != lastAVTiming[i]:
                lastAVTiming[i] = avTiming
                avTimingArray.append({"cnl": i, "value": avTiming, "timestamp": timestamp})
                #print(f"#{i} AV timting:{avTiming}")

        seconds -= 1
        time.sleep(1)

    fetchStatusOnBE()

    firstColumnValues = [
        {"name":"Genlock", "value": currentGenlockFormat}, 
        {"name": "Backend", "value": currentBackendFormat},
        {"name": "Hitomi SD1", "value": page.locator(f'[id="xSdiTiming:rxFmt$0"]').inner_text()},
        {"name": "Hitomi SD2", "value": page.locator(f'[id="xSdiTiming:rxFmt$1"]').inner_text()},
        {"name": "Hitomi FR", "value": page.locator(f'[id="xSdiTiming:rxFmt$5"]').inner_text()},
        {"name": "Genlock Average", "value": genlockAverage},
        {"name": "Ref Status", "value": refStatus},
        {"name": "Mis", "value": mis},
        {"name": "Nov", "value": nov},
         ]
        
    print("\nRecording finished")
    print("writting CSV file")

    with open(f"BE-{currentBackendFormat}-Genlock-{currentGenlockFormat}.csv", "w") as f:
        f.write("system,format,,cnl,ref offset,time,,cnl,e2e timing,time,,cnl,av timing,time\n")

        maxRow = max(len(refOffsetArray), len(e2eTimingArray), len(avTimingArray), len(firstColumnValues))
        for i in range(maxRow):
            if i < len(firstColumnValues):
                f.write(f"{firstColumnValues[i]["name"]},{firstColumnValues[i]["value"]},,")
            else:
                f.write(",,,")

            if i < len(refOffsetArray):
                f.write(f"{refOffsetArray[i]['cnl']},{refOffsetArray[i]['value']},{refOffsetArray[i]['timestamp']}")
            else:
                f.write(",,,,")
            
            if i < len(e2eTimingArray):
                f.write(f",,{e2eTimingArray[i]['cnl']},{e2eTimingArray[i]['value']},{e2eTimingArray[i]['timestamp']}")
            else:
                f.write(",,,,")

            if i < len(avTimingArray):
                f.write(f",,{avTimingArray[i]['cnl']},{avTimingArray[i]['value']},{avTimingArray[i]['timestamp']}")
            else:
                f.write(",,,,")

            f.write("\n")

    print("CSV files writting finished")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(str(sys.argv))
        for arg in sys.argv[1:]:
            specifiedFormats.append(arg)
        
        if len(specifiedFormats) == 1:
            format = specifiedFormats[0]
            if format.endswith("-"):
                format = format[:-1]

                if format in targetSDStandards:
                    specifiedFormats.clear()
                    specifiedFormats.extend(targetSDStandards[targetSDStandards.index(format):])
                    specifiedFormats.extend(targetHDStandards)
                elif format in targetHDStandards:
                    specifiedFormats.clear()
                    specifiedFormats.extend(targetHDStandards[targetHDStandards.index(format):])

        print("specified formats: ", specifiedFormats)
    
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    main()
    #test()

    browser.close()
    p.stop()

    print("Script finished")

