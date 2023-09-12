import psutil


class Temperature:
    def read_temperature(self):
        cpu_temperature = psutil.sensors_temperatures()['k10temp'][0].current
        return cpu_temperature
