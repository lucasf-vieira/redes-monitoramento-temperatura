import paho.mqtt.client as mqtt
import time
from flask import Flask, request

# Configurações do cliente MQTT
broker_ip = "SEU_BROKER_IP"  # Defina o endereço IP do servidor MQTT
broker_port = 1883  # Defina a porta MQTT
client = mqtt.Client()
client.connect(broker_ip, broker_port, 60)

# Variáveis de controle
temperatura_lista = []
X = 60  # Tempo em segundos para enviar a média para o servidor
Y = 10  # Tempo em segundos para enviar a leitura da temperatura


# Função para enviar a média da lista para o servidor
def enviar_media_temp():
    if temperatura_lista:
        media = sum(temperatura_lista) / len(temperatura_lista)
        client.publish("temperatura", f"Média de temperatura: {media:.2f}")
        temperatura_lista.clear()


# Função para enviar a temperatura atual
def enviar_temperatura_atual():
    # Simule a leitura da temperatura do dispositivo (substitua com sua lógica real)
    temperatura_atual = 25.5  # Exemplo de temperatura em graus Celsius
    client.publish("temperatura", f"Temperatura atual: {temperatura_atual:.2f}")
    temperatura_lista.append(temperatura_atual)


# Configurar o servidor web Flask
app = Flask(__name__)


@app.route("/setup", methods=["POST"])
def setup():
    global broker_ip, broker_port
    broker_ip = request.form.get("ip")
    broker_port = int(request.form.get("porta"))
    client.disconnect()
    client.connect(broker_ip, broker_port, 60)
    return "Configuração atualizada com sucesso!"


@app.route("/set_x", methods=["POST"])
def set_x():
    global X
    X = int(request.form.get("X"))
    return f"Valor de X definido para {X}"


@app.route("/set_y", methods=["POST"])
def set_y():
    global Y
    Y = int(request.form.get("Y"))  # type: ignore
    return f"Valor de Y definido para {Y}"


@app.route("/reset", methods=["POST"])
def reset():
    temperatura_lista.clear()
    return "Lista de leitura reiniciada!"


# Loop principal
client.loop_start()
while True:
    enviar_temperatura_atual()
    time.sleep(Y)
    if len(temperatura_lista) >= X:
        enviar_media_temp()
    time.sleep(1)  # Aguarde 1 segundo

# Quando você deseja encerrar a conexão MQTT:
# client.disconnect()
