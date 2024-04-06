from machine import UART
import utime

SSID='***********'
password = '*********'
ServerIP = '192.168.100.14'
Port = '8080'

esp_uart = UART(0, 115200)

def esp_sendCMD(cmd,ack,timeout=2000):
    esp_uart.write(cmd+'\r\n')
    i_t = utime.ticks_ms()
    while (utime.ticks_ms() - i_t) < timeout:
        s_get = esp_uart.read()
        if(s_get != None):
            s_get=s_get.decode()
            print(s_get)
            if(s_get.find(ack) >= 0):
                return True
    return False

# start
esp_uart.write('+++')
if(esp_uart.any()>0):
    esp_uart.read()
esp_sendCMD("AT","OK")
esp_sendCMD("AT+CWMODE=3","OK")
esp_sendCMD("AT+CWJAP=\""+SSID+"\",\""+password+"\"","OK",20000)
esp_sendCMD("AT+CIFSR","OK")
esp_sendCMD("AT+CIPSTART=\"TCP\",\""+ServerIP+"\","+Port,"OK",10000)
esp_sendCMD("AT+CIPMODE=1","OK")
esp_sendCMD("AT+CIPSEND",">")

esp_uart.write('Hello makerobo !!!\r\n') 
esp_uart.write('RP2040-W TCP Client\r\n') 

while True:
    i_s=esp_uart.read()
    if(i_s != None):
        i_s=i_s.decode()
        print(i_s)
