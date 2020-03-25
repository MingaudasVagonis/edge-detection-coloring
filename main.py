from kernel import Kernel, SOBEL_X, SOBEL_Y, GAUSSIAN
import cv2
import numpy as np
import canny
import color
import sys
from argparse import ArgumentParser

def start(args):
	"""Starting the program.
        
	    Parameters
	    ----------
	    args : dict
	        Command line arguments.
	  	Returns
	    -------
	    None
	"""
	image = cv2.imread(args["image"])

	if image is None:
		print("\033[91;1mImage not found\033[0m")
		return

	# Converting the image to 1 channel grayscale ndarray.
	image  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		
	# Applying gaussian filter.
	print("\033[97;1mApplying \033[93;1mGaussian filter\033[0m")
	data = Kernel(GAUSSIAN).roll(image)

	# Applying sobel operator.
	print("\033[97;1mApplying \033[93;1mSobel operator\033[0m")
	data_x, data_y = [ Kernel(model).roll(data) for model in [SOBEL_X, SOBEL_Y]]

	gradient = np.sqrt( np.square(data_x) + np.square(data_y) )

	angles = np.arctan2(data_y, data_x)

	# Starting canny edge detection.
	img = canny.start(gradient, angles, *args["threshold"])

	# Applying color.
	if args["colored"]:
		colored = color.applycolor(img, angles, args["stroke"])
	else: colored = cv2.merge((img, img, img))

	output_name = f"{args['image'].split('.')[0]}_output.png"
	cv2.imwrite(output_name, colored)

	print("\033[92;1mDone\033[0m")

if __name__ == '__main__':

	parser = ArgumentParser()
	parser.add_argument("image", type=str, help="Path to an image")
	parser.add_argument("--colored", "-c", action='store_true', help="Color the edges according to their direction")
	parser.add_argument("--stroke", "-s", type=int, default=0, help="Additional stroke of the edge")
	parser.add_argument("--threshold", "-t", nargs='+', type=int, default=[7, 20])
	args = vars(parser.parse_args())

	start(args)