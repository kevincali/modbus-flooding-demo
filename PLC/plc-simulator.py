#!/usr/bin/python3
from pymodbus.client.sync import ModbusTcpClient
import time
import sys

# Simulation eines PLCs (Siemens S7-1200) der die gewünschten Werte in einer Frequenz von 0,5Hz (2s) setzt
modbus_ip = '10.0.0.42'
register_values = [1, 1234, 56]

client = ModbusTcpClient(modbus_ip)
if not client.connect():
    print("Der Modbus Server läuft nicht.")
    sys.exit(1)

while True:
    client.write_registers(0, register_values)
    print("[PLC]: Setze die Werte {} auf Register 1 bis 3".format(register_values))
    time.sleep(2)
