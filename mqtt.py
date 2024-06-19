import paho.mqtt.client as mqtt
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.devices import DHT
import json


CounterFitConnection.init('localhost', 5000)


sensor = DHT('11', 0)


broker_address = "test.mosquitto.org"  
client = mqtt.Client("SensorSimulator")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker")
    else:
        print("Error en la Conexión del código", rc)

client.on_connect = on_connect

client.connect(broker_address)

client.loop_start()

try:
    while True:
        # Leer valores del sensor simulados
        sensor.read()
        temperature = sensor.temperature
        humidity = sensor.humidity

        # Crear el payload

        payload = {
            'temperature': temperature,
            'humidity': humidity
        }
        payload_str = json.dumps(payload)

        # Publicar los datos  MQTT

        client.publish("sensor/temperature", temperature)
        client.publish("sensor/humidity", humidity)

        print(f"La Temperatura es: {temperature} y la Humedad es: {humidity}")

        time.sleep(5)

except KeyboardInterrupt:
    print("Simulación Detenida")
finally:
    client.loop_stop()
    client.disconnect()

