# -*- coding: utf-8 -*-

import os ,sys
from platform import machine

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask.sessions import NullSession
from PIL import Image

import io

from sbpl import *
from paho.mqtt import client as mqtt_client

import random
import time


import time 

broker = '10.11.1.1'
port = 1883

client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'plc1'
password = 'plc@2021'


app = Flask('MyService')

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client,Material,Mat_Name,Code_Type,Barcode,Amount,topic):
    msg_count = '{"version":0.1,"Code":0,"index":' + Amount + ',"barcode":' + Barcode +',"code_type":"' +Code_Type+'"}'
   
    msg = f'{msg_count}'
    result = client.publish(topic, msg)

    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

    time.sleep(1)

    msg_count1 = '{"version":0.1,"Code":3,"index":' + Amount + ',"barcode":' + Barcode +',"code_type":"' +Code_Type+'"}'
   
    msg1 = f'{msg_count1}'
    result1 = client.publish(topic, msg1)

    status1 = result1[0]
    if status1 == 0:
        print(f"Send `{msg}` to topic `{topic}`")
        count = 1
    else:
        print(f"Failed to send message to topic {topic}")
    count = 0
    # result: [0, 1]
    return count

def subscribe(client: mqtt_client,topic):
    def on_message(client, userdata, msg):
        d = json.loads(msg.payload)
        print("code : " + str(d["Code"]))

        if str(d["Code"]) == "5" :
            print("ok")
            client.disconnect()
            
    client.subscribe(topic)
    client.on_message = on_message
    
'''
def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

    #subscribe(client)
    #client.loop_forever()
'''

@app.route('/re', methods=["GET", "POST"])
def re():  
    if request.method == "POST":
        time.sleep(2)
        os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
        
    
    return render_template("re.html") 

@app.route('/error1', methods=["GET", "POST"])
def error1():  
    if request.method == "POST":
        time.sleep(1)
        os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
        
    
    data = "Error : Connect PLC or MQTT Faill"
   
    return render_template("error.html",data = data) 

@app.route('/error2', methods=["GET", "POST"])
def error2():  
    if request.method == "POST":
        time.sleep(1)
        os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
        
    
    data = "Error : Connect Printer Faill"
   
    return render_template("error.html",data = data) 
    

@app.route('/ok')
def ok():  
    return render_template("noPrinter.html")
    

def stop():
    import requests
    resp = requests.get('http://localhost:5001/shutdown')

@app.route('/index', methods=["GET", "POST"])
def test():

    if request.method == "POST":
        
        Material = request.form['Material']
        Mat_Name = request.form['Mat_Name']
        machineSec = request.form['machineSec']
        Barcode = request.form['Barcode']
        Amount = request.form['Amount']
        Number = request.form['Number']

        try:
            client = connect_mqtt()
            client.loop_start()
            hostasd = None
          
        except:
            return redirect(url_for('error1'))

        if machineSec == "Robotic_5":
            publish(client,Material,Mat_Name,"ean",Barcode,Amount,"/line/1/send")
            hostasd = "10.11.1.15"
        elif machineSec == "Robotic_4":
            publish(client,Material,Mat_Name,"itf",Barcode,Amount,"/line/2/send")
            hostasd = "10.11.1.16"
            print("ok 16 1")

   
        if machineSec == "Robotic_5":
            counterMaterial = 0
            data = Material
            ans_Material = ""
            aeiou= "ิ,ื,่,้,ี,ึ,ุ,ู,็"
            for i in range(0,len(data)):
                if data[i] in aeiou:
                    ans_Material += data[i]+" "
                elif data[i] == "ั" or data[i] == "์":
                    ans_Material += data[i]+"."
                else : 
                    ans_Material += data[i]
                    counterMaterial+=1
            
                    
            data = Mat_Name
            counterMat_Name = 0 
            ans_Mat_Name = ""
            aeiou= "ิ,ื,่,้,ี,ึ,ุ,ู,็"
            for i in range(0,len(data)):
                if data[i] in aeiou:
                    ans_Mat_Name += data[i]+" "
                elif data[i] == "ั" or data[i] == "์":
                    ans_Mat_Name += data[i]+"."
                else : 
                    ans_Mat_Name += data[i]
                    counterMat_Name+=1
                    
            countBarcode = 0
            textBarcode = ""
            for i in Barcode:
                countBarcode+=1
                if countBarcode == 2 :
                    textBarcode+= " " + i
                elif countBarcode == 8 :
                    textBarcode+= " " + i
                elif countBarcode == 13:
                    textBarcode+= " " + i
                else:
                    textBarcode+=i
                    
            print(ans_Material + " : " +str(counterMaterial))
            print(ans_Mat_Name + " : " +str(counterMat_Name))
            
            print(hostasd)
            client.loop_stop()
            
            if counterMaterial < 12 :
                yMaterial = 230
            elif counterMaterial > 20 :
                yMaterial = 178
            else :
                yMaterial = 190
                
            if counterMat_Name < 12 :
                yMat_Name = 230
            elif counterMat_Name > 22 :
                yMat_Name = 160
            else :
                yMat_Name = 200


            json_str =[
                {"host":"10.11.1.15", "port": 9100, "communication": "SG412R_Status5"},
                [
                    {"set_label_size": [440, 158]},

                        {"shift_jis": 0},
                        {"rotate_270": 0},   
                        {"comment": "==Material Name=="},
                        {"pos": [157, yMaterial], "expansion": [1400], "ttf_write": ans_Material, "font": "AngsanaNew-Bold.ttf"},                                        
                        {"comment": "==Material Name=="},
                        {"pos": [135, yMat_Name], "expansion": [1400], "ttf_write": ans_Mat_Name, "font": "AngsanaNew-Bold.ttf"},
                        {"comment": "==barcode=="},
                        {"pos": [108, 135], "jan_13": [Barcode, 3, 55]},   
                        {"comment": "== ID =="},
                        {"pos": [57, 190], "expansion": [1700], "ttf_write": textBarcode, "font": "CmPrasanmit Bold.ttf"},                             
                        {"rotate_0": 0},          
                        {"print": int(Amount)}
                    ]
                ]
                
            comm = SG412R_Status5()
            gen = LabelGenerator()
            parser = JsonParser(gen)
            parser.parse(json_str)
            print(json_str)
            parser.post(comm)
                    
            client = connect_mqtt()
            subscribe(client,"/line/1/receipt")
            
        elif machineSec == "Robotic_4":
            print("ok 16 2")
            counterMaterial = 0
            data = Material
            ans_Material = ""
            aeiou= "ิ,ื,่,้,ี,ึ,ุ,ู,็"
            for i in range(0,len(data)):
                if data[i] in aeiou:
                    ans_Material += data[i]+" "
                elif data[i] == "ั" or data[i] == "์":
                    ans_Material += data[i]+"."
                else : 
                    ans_Material += data[i]
                    counterMaterial+=1
            
                    
            data = Mat_Name
            counterMat_Name = 0 
            ans_Mat_Name = ""
            aeiou= "ิ,ื,่,้,ี,ึ,ุ,ู,็"
            for i in range(0,len(data)):
                if data[i] in aeiou:
                    ans_Mat_Name += data[i]+" "
                elif data[i] == "ั" or data[i] == "์":
                    ans_Mat_Name += data[i]+"."
                else : 
                    ans_Mat_Name += data[i]
                    counterMat_Name+=1
                    
            countBarcode = 0
            textBarcode = ""
            for i in Barcode:
                countBarcode+=1
                if countBarcode == 2 :
                    textBarcode+= " " + i
                elif countBarcode == 8 :
                    textBarcode+= " " + i
                elif countBarcode == 14:
                    textBarcode+= " " + i
                else:
                    textBarcode+=i
                    
            print(ans_Material + " : " +str(counterMaterial))
            print(ans_Mat_Name + " : " +str(counterMat_Name))
            
            print(hostasd)
            client.loop_stop()
            
            if counterMaterial < 12 :
                yMaterial = 240
            elif counterMaterial > 34 :
                yMaterial = 130
            elif counterMaterial > 27 :
                yMaterial = 170
            elif counterMaterial > 20 :
                yMaterial = 185
          
                
            if counterMat_Name < 12 :
                yMat_Name = 270
            elif counterMat_Name > 23 :
                yMat_Name = 210
            else :
                yMat_Name = 240


            json_str =[
                {"host":"10.11.1.16", "port": 9100, "communication": "SG412R_Status5"},
                [
                    {"set_label_size": [440, 158]},

                        {"shift_jis": 0},
                        {"rotate_270": 0},   
                        {"comment": "==Material Name=="},
                        {"pos": [135, yMaterial], "expansion": [1400], "ttf_write": ans_Material, "font": "AngsanaNew-Bold.ttf"},                                        
                        {"comment": "==Material Name=="},
                        {"pos": [115, 240], "expansion": [2000], "ttf_write": Number, "font": "CmPrasanmit Bold.ttf"},
                        {"comment": "==barcode=="},
                        {"pos": [80, 150], "itf2of5": [Barcode, 2, 55]},   
                        {"comment": "== ID =="},
                        {"pos": [30, 190], "expansion": [1700], "ttf_write": textBarcode, "font": "CmPrasanmit Bold.ttf"},                             
                        {"rotate_0": 0},          
                        {"print": int(Amount)}
                    ]
                ]
                
            comm = SG412R_Status5()
            gen = LabelGenerator()
            parser = JsonParser(gen)
            parser.parse(json_str)
            print(json_str)
            parser.post(comm)
                    
            client = connect_mqtt()
            subscribe(client,"/line/2/receipt")

        client.loop_forever()
        
        return redirect(url_for('re'))
        
            
        

    time.sleep(3)
    return render_template("test.html")

#-------------------- Country --------------------------------------
def start():
    app.run(host='0.0.0.0',debug=True,use_reloader=True, port=5000)

count = 0
slp = 1
if __name__ == "__main__":
    slp = 1
    
    start()
