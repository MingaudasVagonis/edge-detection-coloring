import numpy as np

step = 22.5 # PI / 8

directions = ((0, step), (15 * step, 16 * step), (0, -1), (0, +1)), ((step, 3 * step), (9 * step, 11 * step), (1, -1), (-1, 1)),((3 * step, 5 * step), (11 * step, 13 * step), (-1, 0), (1, 0))

hyster_directions = (1, 1),(-1, -1),(1, -1),(-1, 1)

weak_edge = 50

def start(gradient, angles, low = 7, high = 20):
    """Performs canny edge detection.
        
    Parameters
    ----------
    gradient : np.ndarray
        Sobel data.
    angles: np.adarray
        Edge directions.
    low: int
        Lower threshold.
    high: int
        Higher threshold.

    Returns
    -------
    np.ndarray
        1 channel image data of 0s and 255s.
    """

    print("\033[97;1mPerforming \033[93;1mCanny edge detection\033[0m")

    # Streching sobel values in the range of [0, 255]
    px_bottom = gradient.min()
    px_top = gradient.max() - px_bottom
    gradient -= px_bottom
    gradient *= (255 / px_top)

    # Normally angles range from -PI radians to PI radians
    angles = np.rad2deg(angles)
    angles += 180

    data = findedges(gradient, angles)
 
    data = applythreshold(data, low, high)
 
    data = hysteresis(data)

    return data

def matchdirection(d, angle):
    """Whether the angle falls in direction interval.
        
    Parameters
    ----------
    d : list
        List of tuples with intervals..
    angle: float
        Angle value in degrees.

    Returns
    -------
    bool
        Whether the angle falls in direction interval. 
    """
    return (d[0][0] <= angle < d[0][1]) or (d[1][0] <= angle < d[1][1])

def findedges(gradient, angles):
    """Creates an array of the edges according 
        to it's closest pixels and direction.
        
    Parameters
    ----------
    gradient : np.ndarray
        Sobel data.
    angles: np.adarray
        Edge directions.

    Returns
    -------
    np.ndarray
        Array of the edges according to it's 
        closest pixels and direction.
    """
    
    height, width = gradient.shape

    output = np.zeros(gradient.shape)

    for y in range(1, height - 1):

        for x in range(1, width - 1):

            dir = next(((d[2], d[3]) for d in directions if matchdirection(d, angles[y, x])), ((-1, -1), (1, 1)))

            # Getting pixels closest to the current one according to direction.
            peer_0 = gradient[y + dir[0][0], x + dir[0][1]]
            peer_1 = gradient[y + dir[1][0], x + dir[1][1]]

            # If it's value is the highest mark it as an edge.
            if gradient[y,x] == max(gradient[y,x] , peer_0, peer_1):
                output[y, x] = gradient[y, x]

    return output
 
def hysteresis(data):
    """Creates an array of the edges after checking whether the
        weak edges are just noise or are they connected to a strong edge.
        
    Parameters
    ----------
    data : np.ndarray
        Edges after applying threshold.

    Returns
    -------
    np.ndarray
        Final result of canny edge detection.
    """
    height, width = data.shape

    copies = []

    # Tracking edges in t2b, b2t, l2r, r2l directions
    for hyster_direction in hyster_directions:

        copy = data.copy()

        # Ranges in which 3x3 grid that respects image boundaries.
        range_y = range(1, height) if hyster_direction[0] == 1 else range(height - 1, 0, -1)
        range_x = range(1, width)  if hyster_direction[1] == 1 else range(width - 1, 0, -1)

        for y in range_y:
            for x in range_x: 

                if not copy[y, x] == weak_edge:
                    continue

                grid = copy[ y - 1 : y + 1 , x - 1 : x + 1]
 
                # Checking whether the edge has a strong edge neighbour
                copy[y, x] = 255 if 255 in grid else 0

        copies.append(copy)

    new_data = sum(copies)
 
    new_data[new_data > 255] = 255
 
    return new_data

def applythreshold(data, low, high):
    """Creates an array of the strongest and weak edges after 
        checking it against upper and lower thresholds.
        
    Parameters
    ----------
    data : np.ndarray
        Strongest edges after max-suppresion.
    low: int
        Lower threshold.
    high: int
        Higher threshold.

    Returns
    -------
    np.ndarray
        Aarray of the strongest and weak edges after 
        checking it against upper and lower thresholds.
    """
    output = np.zeros(data.shape)
 
    strong_y, strong_x = np.where(data >= high)
    weak_y, weak_x = np.where((data <= high) & (data >= low))
 
    output[strong_y, strong_x] = 255
    output[weak_y, weak_x] = weak_edge
 
    return output
 
 