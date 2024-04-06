import network
import socket

## how to use
# accessPoint = ACCESSPOINT()
# accessPoint.app_mode('PICO-AP', 'password')

class ACCESSPOINT:
  def __init__(self):
    self.config = None

  def page(self):
    text = "Hello, World!"
    # max 6400 caracteres
    html = f"""<html>
  <head>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  </head>
  <body>
  <h1>{text}</h1>
  </body>
</html>"""
    return html

  def app_mode(self, ssid, password):
    # Start the Access Point
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    # IP configuration
    ap.active(True)
    # ap.ifconfig(('192.168.77.1', '255.255.255.0', '192.168.77.1', '0.0.0.0')) # does not work
    
    while ap.active() == False:
      pass
    
    print('PICO Is Now In Access Point Mode')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
    s.bind(('', 80))
    s.listen(5)

    while True:
      # receive request
      conn, addr = s.accept()
      print('Got a connection from %s' % str(addr))
      request = conn.recv(1024)
      request = str(request)
      # send page
      conn.send(self.page()) # max 6400 caracteres
      conn.close()