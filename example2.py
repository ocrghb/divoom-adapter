#from divoomadapter import divoom_protocol
import divoom_protocol
#from divoomadapter import divoom_device
import divoom_device
#from divoomadapter import divoom__image
import divoom_image

from PIL import Image
import time
import sys
import os
import bluetooth
import urllib, json

def test():

	json_url = urllib.urlopen("https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
	data = json.loads(json_url.read())
	TEXT = u"\u2191 "+str(int(round(float(data["price"]))))
	
	
	img = divoom_image.draw_text_to_image(text=TEXT, color=divoom_image.BMP_YELLOW, size=(70, 10))
	sliced_images = divoom_image.horizontal_slices(img)
	# create divoom packages
	raw_data_packages = []
	# thing.create_off_package() #brightness
	for img in sliced_images:
		raw_data_packages.append(divoom_image.to_divoom_data(img))
	# create BT divoom packages

	pkgs = thing.create_animation_packages(raw_data_packages, 1)
	for i in range(0, len(pkgs)):
		dev.send(pkgs[i])
		

	





if len(sys.argv) != 2:
	sys.exit("please provide the Bluetooth device address")

DIVOMM_ADR = sys.argv[1]
thing = divoom_protocol.DivoomAuraBoxProtocol()
dev = divoom_device.DivoomDevice(DIVOMM_ADR)

dev.connect()

print("test")
test()
time.sleep(10)


dev.disconnect()
