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
data = "บีไนซ์ครีมอาบนำ้  แอนตี้.แบคทีเรีย 180 มล.x3 สีเขียว"
ans_Material = ""
aeiou=  "ิ,ื,่,ี,ึ,ุ,ู,็"
for i in range(0,len(data)):
    if data[i] in aeiou:
        ans_Material += data[i]+" "
    elif data[i] == "ั" or data[i] == "์":
        ans_Material += data[i]+"."
    else : 
        ans_Material += data[i]
        
json_str = [
              {"host":"10.11.1.16", "port": 9100, "communication": "SG412R_Status5"},
              [
                  {"set_label_size": [440, 176]},
                  {"shift_jis": 0},
                  {"rotate_270": 0},   
                  {"comment": "==Material Name=="},
                  {"pos": [175, 205], "expansion": [1400], "ttf_write": ans_Material, "font": "AngsanaNew-Bold.ttf"},                                        
                  {"comment": "==Material Name=="},
                  {"pos": [155, 280], "expansion": [1800], "ttf_write": "032-0478", "font": "CmPrasanmit Bold.ttf"},
                  {"comment": "==barcode=="},
                  {"pos": [120, 200], "itf2of5": ["78851989080054", 2, 45]},   
                  {"comment": "== ID =="},
                  {"pos": [75, 230], "expansion": [1700], "ttf_write": "7 8851989 08005 4", "font": "CmPrasanmit Bold.ttf"},                             
                  {"rotate_0": 0},      
                  {"print": 5}
              ]
          ]
          

comm = SG412R_Status5()
gen = LabelGenerator()
parser = JsonParser(gen)
parser.parse(json_str)
print(json_str)
parser.post(comm)
