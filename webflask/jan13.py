'''import socket
mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         
host = "192.168.254.254" 
port = 9100   
try:           
	mysocket.connect((host, port)) #connecting to host
	data = "ภัทรพล"
	mysocket.send(b"^XA^FXNow some text^FS^FO20,130^A@N,50,70,R:TH.FNT,20,20^FDtest..."+data+"  ^FS^XZ")#using bytes
	mysocket.close () #closing connection
except:
	print("Error with the connection")

'''

from sbpl import *
from PIL import Image
import io
data = "บีไนท์ครีมอาบน้ำ 180มล.x3 สีเขียว"
ans = ""
aeiou= "ิ,ื,่,้,ั,ี,ึ,ุ,ู,์,็"
for i in range(0,len(data)):
    if data[i] in aeiou:
        ans += data[i]+" "
    else:
        ans += data[i]

json_str =[
            {"host":"10.11.1.15", "port": 9100, "communication": "SG412R_Status5"},
            [
                {"set_label_size": [440, 158]},

                    {"shift_jis": 0},
                    {"rotate_270": 0},   
                    {"comment": "==Material Name=="},
                    {"pos": [157, 200], "expansion": [1530], "ttf_write": ans, "font": "AngsanaNew-Bold.ttf"},                                        
                    {"comment": "==Material Name=="},
                    {"pos": [133, 290], "expansion": [1530], "ttf_write": "301-0478", "font": "CmPrasanmit Bold.ttf"},
                    {"comment": "==barcode=="},
                    {"pos": [105, 250], "itf2of5": ["78851989080054", 1/2, 60]},      
                    {"comment": "== ID =="},
                    {"pos": [51, 235], "expansion": [1700], "ttf_write": "7 885198 908005 4", "font": "CmPrasanmit Bold.ttf"},                             
                    {"rotate_0": 0},          
                    {"print": 3}
                ]
            ]
          

comm = SG412R_Status5()
gen = LabelGenerator()
parser = JsonParser(gen)
parser.parse(json_str)
print(json_str)
parser.post(comm)
