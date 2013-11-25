from PIL import Image
from math import ceil

#strips divides the image into vertical strips
def get_white_pixels_per_strip(image, strips):
	im = Image.open(image)
	im = im.convert("1")
	im_pixels = list(im.getdata())
	val_list = []

	bucket_size = int(ceil(image.size[0]*image.size[1]/float(strips)))

	for i in range(strips):
		try:
			im_pixels_height = im_pixels[i*bucket_size:(i+1)*bucket_size]
		except:
			im_pixels_height = im_pixels[i*bucket_size:]

		val_list.append(sum(im_pixels_height)/255.0)

	val_list.reverse()
	return val_list