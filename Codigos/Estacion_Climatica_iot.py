#Estacion Climatica Remota SMS IoT
'''Autor: Daniel Hernandez Hernandez
Este codigo muestra el uso del microcontrolador 
Raspberry Pi Pico W para el envio de datos de Temperatura y Humedad
a traves de broker MQTT y la comunicacion con Arduino para el envio 
de mensajes SMS con Arduino GSM Shield 2'''

#Librerias necesarias
from umqtt.simple import MQTTClient
import ujson
from time import sleep
import network
from machine import Pin, UART, PWM
from dht import DHT11

#Comunicacion Serial con Arduino 
sms = UART(0, baudrate= 9600, tx= Pin(0), rx=Pin(1))

#Sensor DHT11
sensor = DHT11(Pin(15))

#Servo motor
servo=PWM(Pin(16))
servo.freq(50)

#Led interno de RPPW
led_int = Pin("LED",Pin.OUT)

# Conexión Wifi
wf = network.WLAN(network.STA_IF)
wf.active(True)
wf.connect('Red', "contraseña")
while not wf.isconnected():
    led_int.toggle()
    sleep(1)
print(f"Conectado: {wf.ifconfig()[0]}")
led_int.value(1)
sleep(1)

#Conexion a MQTT
name = "RppW"
addr = "Ingresa_IP_Nueva"
topic = b'clima/iot'
topic2 = b'clima/iot/ventilador'
mqtt = MQTTClient(name, addr , keepalive=60)
mqtt.connect()

def Estacion_Climatica():
    
    temp= sensor.temperature()   
    hum= sensor.humidity()
   
    msg_clima= ujson.dumps({"temp": temp, "zn":"tu_zona","hum":hum})
    
    return msg_clima 

def Ventilador (topic2,msg):
    if msg.decode() == "open":
        servo.duty_u16(1311)
        sleep(2)
    else:
        servo.duty_u16(7864)
        sleep(2)

mqtt.set_callback(Ventilador)
mqtt.subscribe(topic2)


while True:
    mqtt.check_msg()
    sensor.measure()
    
    temp_sms= sensor.temperature()
    if temp_sms >= 35:
        sms.write("1")
        sleep(2)
        
    mqtt.publish(topic, Estacion_Climatica())
    sleep(4)

