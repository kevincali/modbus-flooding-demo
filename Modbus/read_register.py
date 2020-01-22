#!/usr/bin/python3
from pymodbus.client.sync import ModbusTcpClient
from run_attack import find_modbus_server
import sys
import time
import requests

# Nichts tun wenn kein Parameter angegeben wird
if len(sys.argv) != 2:
    print("Bitte das gewünschte Register angeben.")
else:
    modbus_ip = find_modbus_server()
    client = ModbusTcpClient(modbus_ip)
    # Überprüfen ob der Modbus Server läuft
    if not client.connect():
        print("Der Modbus Server läuft nicht.")
    else:
        chosen_register = int(sys.argv[1])
        try:
            # Während der Modbus Server läuft, im 100ms Intervall
            # den aktuellen Register Wert auslesen und ausgeben
            while requests.get('http://127.0.0.1:5000/isUp').text == "up":
                response = client.read_holding_registers(chosen_register)
                print(response.registers[0])
                time.sleep(0.1)
        except requests.exceptions.ConnectionError:
            print("Der Webserver läuft nicht.")
