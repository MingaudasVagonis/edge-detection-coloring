import numpy as np
import random
import sys
import math
import cv2
EPSILON = sys.float_info.epsilon

peers_indexes = (0, -1) , (0, 1), (-1, 0), (1, 0)

diagonal_peers_indexes = (-1, -1), (-1, 1), (1, 1), (1, -1)

def strokekernel(stroke):
	"""Creates a stroke kernel to help thicken the edge.
		E. g.    x
				xxx
			   xx xx
			   	xxx
			   	 x
    Parameters
    ----------
    stroke : int
        Stroke size.

    Returns
    -------
    list
        A list of tuples of (y,x) which defines the relative pixels to color.
    """
	stroke_indexes = []

	# Perpendicular directions
	for dis in range(stroke, 0, -1):
		for peer in peers_indexes: 
			stroke_indexes.append((peer[0] * dis, peer[1] * dis))

	# Diagonal directinos
	for dir in diagonal_peers_indexes:
		for x in range(1, stroke):
			# In order not to make a square shape.
			for y in range(1, stroke - x + 1):
				stroke_indexes.append(( y * dir[0], x * dir[1]))

	return stroke_indexes

def applycolor(data, angles, stroke = 0):
	"""Applies color to the edge according to it's direction.
		
    Parameters
    ----------
    data : np.ndarray
        All the pixels.
	angles: np.adarray
		Edge directions.
	stroke: int
		The size of the edge.

    Returns
    -------
    np.ndarray
        3 channel colored image data.
    """
	print("\033[96;1mC\033[95;1mo\033[94;1ml\033[93;1mo\033[92;1mr\033[91;1mi\033[96;1m\033[95;1mn\033[94;1mg\033[97;1m the image\033[0m")

	# Empty array with 3 channels
	output = np.zeros(data.shape + (3,))

	height, width = data.shape

	whites = np.argwhere(data == 255)

	# Normally angles range from -PI radians to PI radians
	angles = np.rad2deg(angles)
	angles += 180

	if not stroke == 0:
		stroke_kernel = strokekernel(stroke)

	colors = [255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 0, 0]

	for white in whites:
		y, x = white

		angle = angles[y, x]

		rgb = convert_to_rgb(0, 360, angle, colors)

		output[y, x] = rgb

		if stroke == 0:
			continue

		# Thickening the edge
		for peer in stroke_kernel:
			if (0 <= y + peer[0] < height) and (0 <= x + peer[1] < width):
				if data[y + peer[0], x + peer[1]] == 0:
					output[y + peer[0], x + peer[1]] = rgb

	return output

# Taken from https://stackoverflow.com/a/20793850
def convert_to_rgb(minval, maxval, val, colors):
	i_f = float(val-minval) / float(maxval-minval) * (len(colors)-1)
	i, f = int(i_f // 1), i_f % 1 
    
	if f < EPSILON:
		return colors[i]
	else:  
		(r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
		return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))
