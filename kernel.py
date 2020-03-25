import numpy as np

class Kernel:
	"""
    A class used to represent a Kernel.

    Attributes
    ----------
    model : np.ndarray
        Kernel model.
    padding : int
        Distance between the side and the center of the kernel.
   
    Methods
    -------
    apply(grid, xs, ys)
        Convoluting image grid with the kernel.
	roll(image)
		Applying kernel convolutions to the image.
    """
	def __init__(self, model):
		"""
	    Parameters
	    ----------
	    model : list
	        2D kernel.
	    """

		self.model = np.array(model)

		kernel_width, kernel_height = self.model.shape

		self.padding = int( ( kernel_width - 1 ) / 2 )


	def apply(self, grid, xs, ys):
		"""Convoluting image grid with the kernel.
        
	    Parameters
	    ----------
	    grid : np.ndarray
	        Pixel grid.
	    xs: tuple
	        Indexes in x direction.
	    ys: tuple
	        Indexses in y direction.

	    Returns
	    -------
	    int
	        Value after convoluting and dividing pixels with the kernel.
	    """

	    # Cropping the kernel according to the pixel grid.
		model = self.model[ys, xs]

		convolution = grid * model

		# Adding up all the kernel values
		divisor = max(np.sum(model, axis=(0,1)), 1)

		avg = np.sum(convolution, axis = (0,1)) / divisor
		
		return int(avg)

	def roll(self, image): 
		"""Applying kernel convolutions to the image.
        
	    Parameters
	    ----------
	    image : np.ndarray
	        Image data.

	    Returns
	    -------
	    np.ndarray
	        1 channel image data after applying kernel convolutions.
	    """

		output = np.zeros(image.shape)

		height, width = image.shape

		for y in range(height):

			# Getting available neighbour indexes in y direction.
			delta_y_0 = abs(min(y - self.padding, 0))
			delta_y_1 = min( height - 1 - y, self.padding) + self.padding + 1

			for x in range(width):

				# Getting available neighbour indexes in x direction.
				delta_x_0 = abs( min(x - self.padding, 0)) 
				delta_x_1 = min( width - 1 - x, self.padding) + self.padding + 1

				# Taking a grid of pixels from the image.
				grid = image[ 
					y - (self.padding - delta_y_0) : y + (delta_y_1 - self.padding),
					x - (self.padding - delta_x_0) : x + (delta_x_1 - self.padding)
				]

				pixel = self.apply(grid, slice(delta_x_0, delta_x_1 ), slice(delta_y_0,delta_y_1))
				
				output[y, x] = pixel

		return output

SOBEL_X = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]

SOBEL_Y = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

GAUSSIAN = [
	[0.16901332, 0.24935221, 0.32919299, 0.38889556, 0.41111229, 0.38889556, 0.32919299, 0.24935221, 0.16901332],
	[0.24935221, 0.36787944, 0.48567179, 0.57375342, 0.60653066, 0.57375342, 0.48567179, 0.36787944, 0.24935221],
	[0.32919299, 0.48567179, 0.64118039, 0.75746513, 0.8007374,  0.75746513, 0.64118039, 0.48567179, 0.32919299],
	[0.38889556, 0.57375342, 0.75746513, 0.89483932, 0.94595947, 0.89483932, 0.75746513, 0.57375342, 0.38889556],
	[0.41111229, 0.60653066, 0.8007374,  0.94595947, 1,          0.94595947, 0.8007374,  0.60653066, 0.41111229],
	[0.38889556, 0.57375342, 0.75746513, 0.89483932, 0.94595947, 0.89483932, 0.75746513, 0.57375342, 0.38889556],
	[0.32919299, 0.48567179, 0.64118039, 0.75746513, 0.8007374,  0.75746513, 0.64118039, 0.48567179, 0.32919299],
	[0.24935221, 0.36787944, 0.48567179, 0.57375342, 0.60653066, 0.57375342, 0.48567179, 0.36787944, 0.24935221],
	[0.16901332, 0.24935221, 0.32919299, 0.38889556, 0.41111229, 0.38889556, 0.32919299, 0.24935221, 0.16901332]
]
