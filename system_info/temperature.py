import psutil


class Temperature:
    POSSIBLE_TEMPERATURE_KEYS = ["k10temp", "coretemp"]

    def read_temperature(self):
        computer_temperatures = psutil.sensors_temperatures()
        for key in self.POSSIBLE_TEMPERATURE_KEYS:
            if key in computer_temperatures:
                return computer_temperatures[key][0].current

        raise Exception("No temperature found for the current computer.")
