from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math
import os
import sys

# bmp 16bit palette to divoom palett ...
# bmp pallett
BMP_BLACK = 0
BMP_DARK_RED = 1
BMP_DARK_GREEN = 2
BMP_YELLOW_OCHRE = 3
BMP_GREEN = 6
BMP_PINK = 7
BMP_LIGHT_PINK = 8
BMP_RED = 9
BMP_ANOTHER_GREEN = 10
BMP_YELLOW = 11
BMP_BLUE = 12
BMP_LIGHT_BLUE = 14
BMP_WHITE = 15

# divoom palette
# 0 = black
# 1 = red
# 2 = green
# 3 = yellow
# 4 = blue
# 5 = pink
# 6 = light blue
# 7 = white

REPLACER = {BMP_DARK_GREEN:2, BMP_BLACK:0, BMP_YELLOW_OCHRE:11, 5:5, BMP_GREEN:2, BMP_PINK:5, BMP_LIGHT_PINK:5, BMP_RED:1, BMP_DARK_RED:1, BMP_ANOTHER_GREEN:2, BMP_YELLOW:3, BMP_BLUE:4, BMP_LIGHT_BLUE:6, BMP_WHITE:7}

def pretty_print(image):
	n = 0
	for c in im.getdata():
		n=n+1
		print ("number" + str(n))
		print ("color" + str(c))
		
def to_(a, b):
	'''Convert from 16bit palette to divoom color.'''
	upper = REPLACER[b] << 4
	lower = REPLACER[a]
	val =  upper + lower
	return val
	
def from_(val):
	'''Convert back from divoom to an image.'''
	a = val % 16
	b = val / 16
	for k, v in REPLACER.items():
		if (v == a):
			a = k
			break;
	for k, v in REPLACER.items():
		if (v == b):
			b = k
			break;
			
	return (a, b)
		
def to_divoom_data(image):
	'''Gets an image and returns divoom raw data.'''
	# TODO check image is 10x10

	result = []
	# we now have 100 values and need to have 50 bytes
	it = iter(image.getdata())
	for i in it:
		val = to_(i, next(it))
		result.append(val)
		
	return result

def image_to_divoom(imagename):
	'''Gets a path to a .bmp and returns divoom raw data.'''
	im = Image.open(imagename)
	return to_divoom_data(im)
	
def divoom_to_image(data):
	'''Given divoom raw data reeturns an image from this.'''
	im = create_default_image((10,10))
	
	img_data = []
	for d in data:
		a, b = from_(d)
		img_data.append(a)
		img_data.append(b)
	
	im.putdata(img_data)
	return im
	
# way:
# 1 horizontal from left to right
# 2 vertical from upper to lower
# 3 horizontal from right to left
# 4 vertical from lower to upper
def _slices(image, way=1, slice_size=10):
	'''Create 10x10 images from a bigger image e.g. 10x40.'''
	width, height = image.size
	# calculate slice size:
	slices = 1
	if (way == 1) or (way == 3):
		slices = width - slice_size
	elif (way == 2)  or (way == 4):
		slices = height - slice_size
	
	result_images = []
	
	if (way == 1):
		for slice in range(slices):
			new_box = (slice, 0, slice+slice_size, height)
			new_img = image.crop(new_box)
			result_images.append(new_img)
	elif (way == 2):
		for slice in range(slices):
			new_box = (0, slice, width, slice+slice_size)
			new_img = image.crop(new_box)
			result_images.append(new_img)
	elif (way == 3):
		for slice in range(slices,-1,-1):
			new_box = (slice, 0, slice+slice_size, height)
			new_img = image.crop(new_box)
			result_images.append(new_img)
	elif (way == 4):
		for slice in range(slices,-1,-1):
			new_box = (0, slice, width, slice+slice_size)
			new_img = image.crop(new_box)
			result_images.append(new_img)
		
	return result_images
	
# ways
# 1 horizontal from left to right
# 2 vertical from upper to lower
# 3 horizontal from right to left
# 4 vertical from lower to upper
def scroll_between(old_img, new_img, way=1):
	'''Does a scroll between the old and the new image and returns all images in between.'''
	img = None
	if (way == 1):
		img = concatenate(old_img, new_img, 1)
	elif (way == 2):
		img = concatenate(old_img, new_img, 2)
	elif (way == 3):
		img = concatenate(new_img, old_img, 1)
	elif (way == 4):
		img = concatenate(new_img, old_img, 2)	
	sliced_images = _slices(img, way)
	sliced_images.append(new_img)
	return sliced_images
	
def concatenate(image1, image2, way=1):
	'''Concatenates the sencond image to the first'''
	if (way == 1):
		result_img = create_default_image((20, 10))
		result_img.paste(image1, (0, 0))
		result_img.paste(image2, (10, 0))
	if (way == 2):
		result_img = create_default_image((10, 20))
		result_img.paste(image1, (0, 0))
		result_img.paste(image2, (0, 10))
	return result_img
	

	
def horizontal_slices(image, slice_size=10):
	'''Create 10x10 images from a bigger image e.g. 10x40.'''
	return _slices(image=image, way=1, slice_size=slice_size)
	
def image_horizontal_slices(image_path, slice_size=10):
	'''Create 10x10 images from a bigger image given as path.'''
	img = Image.open(image_path)
	return horizontal_slices(img, slice_size)
	
def create_default_image(size):
	'''Create an image with the correct palette'''
	# make use of the black image to copy the palette over
	proto = Image.open(os.path.join(os.path.dirname(__file__), "images/black.bmp"))
	im = Image.new("P", size)
	im.putpalette(proto.palette.getdata()[1])
	return im

def draw_text_to_image(text, color=BMP_RED, size=(40,10)):
	'''Draws the string in given color to an image and returns this iamge'''
	im = create_default_image(size)
	draw = ImageDraw.Draw(im)
	# fn = ImageFont.load(os.path.join(os.path.dirname(__file__),'fonts/slkscr.pil'))
	fn = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'fonts/DejaVuSans.ttf'))
	draw.text((0,0), text, font=fn, fill=color)
	del draw
	return im
