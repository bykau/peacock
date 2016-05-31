import cv2


OVAL_COLOR = [0, 255, 255]
OVAL_RADIUS = 4
FRAME_COL = 0
X_COOR_COL = 0
Y_COOR_COL = 1
N_SKIPPED_LINES = 0
COOR_FILE = 'FinalGazeCoordinates.csv'
SCALE = False
SEPARATOR = ','
work_dir = '../02/'


def draw_oval(img, oval_radius, oval_center, oval_color, height, width):
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
                if x < height and y < width:
                    img[x, y] = oval_color


def load_coordinates(input_path, height, width):
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
        for i in range(N_SKIPPED_LINES, len(lines)):
            line = lines[i]
            vals = line.split(SEPARATOR)
            Xs.append(float(vals[X_COOR_COL]))
            Ys.append(float(vals[Y_COOR_COL]))
        minX = min(Xs)
        maxX = max(Xs)
        minY = min(Ys)
        maxY = max(Ys)
        for i in range(N_SKIPPED_LINES, len(lines)):
            line = lines[i]
            vals = line.split(SEPARATOR)
            if SCALE:
                res[int(vals[FRAME_COL])] = (int((float(vals[X_COOR_COL]) - minX)*(height-1)/(maxX-minX)), int((float(vals[Y_COOR_COL]) - minY)*(width-1)/(maxY-minY)))
            else:
                res[i+1] = (int(float(vals[X_COOR_COL])), int(float(vals[Y_COOR_COL])))
    return res



vidcap = cv2.VideoCapture(work_dir+'05-19-12_No53_363301_Cop.mov')
frame_num = 1
success, image = vidcap.read()

# init the video writer
height, width, layers = image.shape
coors = load_coordinates(work_dir+COOR_FILE, height, width)
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
output = cv2.VideoWriter(work_dir+'output.avi', fourcc, 60, (width, height))

while success:
    # if there are coordinates then draw the yellow dot, otherwise just output a plain images
    if frame_num in coors:
        x, y = coors[frame_num]
        # do you calculations here
        draw_oval(image, OVAL_RADIUS, (x, y), OVAL_COLOR, height, width)
    output.write(image)
    frame_num += 1
    success, image = vidcap.read()

output.release()
cv2.destroyAllWindows()
