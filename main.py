from machine import Pin, ADC
from time import sleep
import dht
import socket

led = Pin(2, Pin.OUT)
sensor = dht.DHT22(Pin(14))
pot=ADC(0)

led_state = "OFF"

def read_sensor():
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    pot_value = pot.read()
    print('Temperature: %3.1f C' %temp)
    print('Luminosity:', pot_value)
    print('Humidity: %3.1f %%' %hum)
    return temp, hum, pot_value

def web_page():
    result_sensor = read_sensor()
    html = """<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Prueba</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
      </head>
    
  <body>
  <div class="container">
    <header class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom">
        <img src="https://cdn1.iconfinder.com/data/icons/smart-home-156/128/07_-_Home_Monitoring-256.png" alt="" style="width: 7%;">
        
        <ul class="nav col-12 col-md-auto mb-2 justify-content-center mb-md-0">
          <li><a href="#" class="nav-link px-2 link-secondary">Brandon Jesus Santana Gudiño</a></li>
          <li><a href="#" class="nav-link px-2 link-dark">G2146006</a></li>
        </ul>
  
        <div class="col-md-3 text-end">
          <a href=\"?led_on" class="btn btn-outline-success">ON</a>
          <a href=\"?led_off" class="btn btn-outline-danger">OFF</a>
        </div>
      </header>
      <h2>Plataforma para el monitoreo de la humedad, temperatura y luminosidad via remota</h2><br><br>

      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div class="col">
          <div class="card">
            <img src="https://cdn3.iconfinder.com/data/icons/ballicons-reloaded-free/512/icon-59-256.png" class="rounded mx-auto d-block" alt="...">
            <div class="card-body">
              <h5 class="text-center">Temperatura</h5>
              <h5 class="text-center">""" + str(result_sensor[0]) + """</h5>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card">
            <img src="https://cdn4.iconfinder.com/data/icons/the-weather-is-nice-today/64/weather_44-256.png" class="rounded mx-auto d-block" alt="...">
            <div class="card-body">
              <h5 class="text-center">Humedad</h5>
              <h5 class="text-center">""" + str(result_sensor[1]) + """</h5>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card">
            <img src="https://cdn1.iconfinder.com/data/icons/smart-home-157/128/17_-_Smart_Light_Bulb-256.png" class="rounded mx-auto d-block" alt="...">
            <div class="card-body">
              <h5 class="text-center">Luminosidad</h5>
              <h5 class="text-center">""" + str(result_sensor[2]) + """</h5>
            </div>
          </div>
        </div>
      </div>

  </div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" 
integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" 
crossorigin="anonymous"></script>
  </body>
</html>"""
    return html

                        


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('GET Rquest Content = %s' % request)
        led_on = request.find('/?led_on')
        led_off = request.find('/?led_off')
        if led_on == 6:
            print('LED ON -> GPIO2')
            led_state = "ON"
            led.on()
        if led_off == 6:
            print('LED OFF -> GPIO2')
            led_state = "OFF"
            led.off()
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')
