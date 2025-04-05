
    
from pywinauto import Application
import time

genlockSDStandardMap=[
    {"nanotext":"NTSC" ,"hitomitext":"525i29","framerate":29.97},
    {"nanotext":"PAL 25" ,"hitomitext":"625i25","framerate":25},
]
genlockHDStandardMap=[
    {"nanotext":"1080i 50" ,"hitomitext":"1080i25","framerate":25},
    {"nanotext":"1080i 59.94" ,"hitomitext":"1080i29","framerate":29.97},
    {"nanotext":"1080p 23.98" ,"hitomitext":"1080p23","framerate":23.98},
    {"nanotext":"1080p 24" ,"hitomitext":"1080p24","framerate":24},
    {"nanotext":"1080p 25" ,"hitomitext":"1080p25","framerate":25},
    {"nanotext":"1080p 29.97" ,"hitomitext":"1080p29","framerate":29.97},
    {"nanotext":"1080p 50" ,"hitomitext":"1080p25","framerate":50},
    {"nanotext":"1080p 59.94" ,"hitomitext":"1080p29","framerate":59.94},
    {"nanotext":"720p 23.98" ,"hitomitext":"720p23","framerate":23.98},
    {"nanotext":"720p 24" ,"hitomitext":"720p24","framerate":24},
    {"nanotext":"720p 25" ,"hitomitext":"720p25","framerate":25},
    {"nanotext":"720p 29.97" ,"hitomitext":"720p29","framerate":29.97},
    {"nanotext":"720p 50" ,"hitomitext":"720p25","framerate":50},
    {"nanotext":"720p 59.94" ,"hitomitext":"720p29","framerate":59.94},
]
def findHDStandard(findNanoText):
    for idx, value in enumerate(genlockHDStandardMap):
        if value['nanotext'] == findNanoText:
            return value,idx
    return None,None


def findSDStandard(findNanoText):
    for idx, value in enumerate(genlockSDStandardMap):
        if value['nanotext'] == findNanoText:
            return value,idx
    return None,None
             
XtargetSDStandards = [
    "NTSC",
    "PAL 25",
]
XtargetHDStandards = [
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

class NanoAPP():
    def __init__(self):
        app = Application(backend="uia").connect(
            title="Rosendahl nanosyncs HD  3.0")

        # Get the main window
        self.window = app.window(title="Rosendahl nanosyncs HD  3.0")
        if self.window:
            click_button(self.window, "Connect")
            time.sleep(1)

            self.SD_list_element = self.window.ListBox4
            self.HD_list_element = self.window.ListBox10

    def __click_6789(self,SD=True):
        # "VIDEO OUT 1-3", "VIDEO OUT 4", "VIDEO OUT 5", "VIDEO OUT 6"
        value = 0 if SD else 1
        click_list_item(self.window.ListBox6, value)
        click_list_item(self.window.ListBox7, value)
        click_list_item(self.window.ListBox8, value)
        click_list_item(self.window.ListBox9, value)

    def Active(self):
        # 激活窗口并置顶
        self.window.set_focus()       # 获取焦点
        #self.window.set_foreground()  # 强制置顶（可能需要管理员权限）

    def switchtoSD(self,standardName='ALL'):
        if not  self.SD_list_element :
            return 
        
        self.Active()
        for item in self.SD_list_element.children():
            itemText = item.window_text()
            if standardName!= 'ALL' and standardName!= itemText:
                continue
            print(f"select SD standard: {itemText}")
            
            self.Active()
            item.click_input()
            currentGenlockFormat = itemText

            self.__click_6789(True)

            time.sleep(1)
            
    def switchtoHD(self,standardName='ALL'):    
        if not self.HD_list_element :
            return
        self.Active()
        listItems = self.HD_list_element.children()
        for item in listItems:
            itemText = item.window_text()
            if standardName!='ALL' and  standardName!= itemText:
                continue
           
            s,itemIndex = findHDStandard(itemText)
            if s==None:
                continue

            print(f"select HD standard: {itemText}")

            
            baseStandardList = targetHDBaseStandards[itemIndex]
            for baseStandard in baseStandardList:
                baseItem = findBaseHDStandard(baseStandard, listItems)
                #print("select base standard:", baseStandard)
                self.Active()
                baseItem.click_input()

                # "VIDEO OUT 1-3", "VIDEO OUT 4", "VIDEO OUT 5", "VIDEO OUT 6"
                self.__click_6789(False)

                time.sleep(1)
                #print("hitomi:",httpApi.getGenlockFormatFromHitomi())

            self.Active()
            item.click_input()
            currentGenlockFormat = itemText

            # "VIDEO OUT 1-3", "VIDEO OUT 4", "VIDEO OUT 5", "VIDEO OUT 6"
            self.__click_6789(False)

            time.sleep(1)
            
            

if __name__=="__main__":
    na=NanoAPP()
    na.switchtoSD()
    na.switchtoHD('1080i 50')
    #na.runSD('NTSC')
    #na.runSD('PAL 25')
    