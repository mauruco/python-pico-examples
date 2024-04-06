from machine import UART
import utime,time

SSID='***********'
password = '*********'
Port = '8080'

esp_uart = UART(0, 115200)

def esp_sendCMD(cmd,ack,timeout=2000):
    esp_uart.write(cmd+'\r\n')
    i_t = utime.ticks_ms()
    while (utime.ticks_ms() - i_t) < timeout:
        s_get=esp_uart.read()
        if(s_get != None):
            s_get=s_get.decode()
            print(s_get)
            if(s_get.find(ack) >= 0):
                return True
    return False

def esp_sendData(ID,data):
    esp_sendCMD('AT+CIPSEND='+str(ID)+','+str(len(data)),'>')
    esp_uart.write(data)

def esp_ReceiveData():
    s_get=esp_uart.read()
    if(s_get != None):
        s_get=s_get.decode()
        print(s_get)
        if(s_get.find('+IPD') >= 0):
            n1=s_get.find('+IPD,')
            n2=s_get.find(',',n1+5)
            ID=int(s_get[n1+5:n2])
            n3=s_get.find(':')
            s_get=s_get[n3+1:]
            return ID,s_get
    return None,None

# start
esp_uart.write('+++')
time.sleep(1)
if(esp_uart.any()>0):
    esp_uart.read()
esp_sendCMD("AT","OK")
esp_sendCMD("AT+CWMODE=3","OK")
esp_sendCMD("AT+CWJAP=\""+SSID+"\",\""+password+"\"","OK",20000)
esp_sendCMD("AT+CIPMUX=1","OK")
esp_sendCMD("AT+CIPSERVER=1,"+Port,"OK")
esp_sendCMD("AT+CIFSR","OK")

while True:
    ID,s_get=esp_ReceiveData() 
    if(ID != None):
        esp_sendData(ID,s_get)
