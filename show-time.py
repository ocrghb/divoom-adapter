import sys
import time
import divoom_protocol
import divoom_device


if len(sys.argv) != 2:
	sys.exit("please provide the Bluetooth device address")

# create time
hour12 = time.strftime('%H')
minute = time.strftime('%M')
second = time.strftime('%S')

DIVOMM_ADR = sys.argv[1]
thing = divoom_protocol.DivoomAuraBoxProtocol()
dev = divoom_device.DivoomDevice(DIVOMM_ADR)

dev.connect()
print("setting time to "  + hour12 + ":" + minute + ":" + second)
dev.send(thing.create_set_time_package(hour12, minute, second))
print("showing time")
dev.send(thing.create_time_package())
time.sleep(10)
dev.disconnect()
