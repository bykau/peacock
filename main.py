import cv2


OVAL_COLOR = [0, 255, 255]
OVAL_RADIUS = 4
FRAME_COL = 0
X_COOR_COL = 5
Y_COOR_COL = 6
MAX_X = 480
MAX_Y = 480
work_dir = '../02/'


def draw_oval(img, oval_radius, oval_center, oval_color):
    '''
    Draws a yellow oval at the given coordinates.
    :param img:
    :param oval_radius:
    :param oval_center:
    :param oval_color:
    :return:
    '''
    for x in range(oval_center[0]-oval_radius, oval_center[0]+oval_radius):
        for y in range(oval_center[1]-oval_radius, oval_center[1]+oval_radius):
            if (x-oval_center[0])*(x-oval_center[0]) + (y-oval_center[1])*(y-oval_center[1]) <= oval_radius*oval_radius:
                if x < MAX_X and y < MAX_Y:
                    img[x, y] = oval_color


def load_coordinates(input_path):
    '''
    Loads the corrdinates of the yellow dot

    :param input_path:
    :return: a dict where the key is frame num and values are corresponding coordinates
    '''
    res = {}
    with open(input_path, 'rb') as input_file:
        lines = input_file.readlines()
        # scaling
        Xs = []
        Ys = []
        for i in range(7, len(lines)):
            line = lines[i]
            vals = line.split(' ')
            Xs.append(float(vals[X_COOR_COL]))
            Ys.append(float(vals[Y_COOR_COL]))
        minX = min(Xs)
        maxX = max(Xs)
        minY = min(Ys)
        maxY = max(Ys)
        for i in range(7, len(lines)):
            line = lines[i]
            vals = line.split(' ')
            res[int(vals[FRAME_COL])] = (int((float(vals[X_COOR_COL]) - minX)*(MAX_X-1)/(maxX-minX)), int((float(vals[Y_COOR_COL]) - minY)*(MAX_Y-1)/(maxY-minY)))
    return res

coors = load_coordinates(work_dir+'05-19-12_No53_363301_Cop.txt')

vidcap = cv2.VideoCapture(work_dir+'05-19-12_No53_363301_Cop.mov')
frame_num = 1
success, image = vidcap.read()

# init the video writer
height, width, layers = image.shape
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
output = cv2.VideoWriter(work_dir+'output.avi', fourcc, 60, (width, height))

while success:
    # if there are coordinates then draw the yellow dot, otherwise just output a plain images
    if frame_num in coors:
        x, y = coors[frame_num]
        # do you calculations here
        draw_oval(image, OVAL_RADIUS, (x, y), OVAL_COLOR)
    output.write(image)
    frame_num += 1
    success, image = vidcap.read()

output.release()
cv2.destroyAllWindows()
