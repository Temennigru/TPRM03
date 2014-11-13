import numpy as np
import cv2
from matplotlib import pyplot as plt
import math


def rotationMatrix(theta):
    return ((math.cos(theta), -math.sin(theta)),(math.sin(theta), math.cos(theta)))

def drawCircle(img, x, y, radius):
    out = img.copy()

    # Draw a small circle at both co-ordinates
    # radius 4
    # colour blue
    # thickness = 1
    cv2.circle(out, (int(x),int(y)), radius, (0, 255, 0), radius/2)

    return out

def matMult(mat1, mat2):
    return (mat1[0][0]*mat2[0] + mat1[0][1]*mat2[1], mat1[1][0]*mat2[0] + mat1[1][1]*mat2[1])

def rotate(mat, theta):
    return matMult(rotationMatrix(theta), mat)

def drawDrone(img, x, y, theta):
    theta2 = theta + math.pi/2
    radius = 5

    # Define circle centers and front identifier on static reference
    circle1 = (radius, radius)
    circle2 = (-radius, radius)
    circle3 = (-radius, -radius)
    circle4 = (radius, -radius)
    front = (2, 0)

    # Rotate drone in theta
    circle1 = rotate(circle1, theta2)
    circle2 = rotate(circle2, theta2)
    circle3 = rotate(circle3, theta2)
    circle4 = rotate(circle4, theta2)
    front = rotate(front, theta2)

    # Translate to correct coordinates
    circle1 = (circle1[0] + x, circle1[1] + y)
    circle2 = (circle2[0] + x, circle2[1] + y)
    circle3 = (circle3[0] + x, circle3[1] + y)
    circle4 = (circle4[0] + x, circle4[1] + y)
    front = (front[0] + x, front[1] + y)

    # Draw
    out = drawCircle(img, circle1[0], circle1[1], radius)
    out = drawCircle(out, circle2[0], circle2[1], radius)
    out = drawCircle(out, circle3[0], circle3[1], radius)
    out = drawCircle(out, circle4[0], circle4[1], radius)
    cv2.line(out, (int(x),int(y)), (int(front[0]),int(front[1])), (0, 255, 0), 1)

    return out


def drawMatches(img1, kp1, img2, kp2, matches):
    """
    My own implementation of cv2.drawMatches as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated
    keypoints, as well as a list of DMatch data structure (matches)
    that contains which keypoints matched in which images.

    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1,:] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:cols1+cols2,:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them

    if isinstance(matches, list):
        for i in matches:
            for mat in i:

                # Get the matching keypoints for each of the images
                img1_idx = mat.queryIdx
                img2_idx = mat.trainIdx

                # x - columns
                # y - rows
                (x1,y1) = kp1[img1_idx].pt
                (x2,y2) = kp2[img2_idx].pt

                # Draw a small circle at both co-ordinates
                # radius 4
                # colour blue
                # thickness = 1
                cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)
                cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

                # Draw a line in between the two points
                # thickness = 1
                # colour blue
                cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)



    else:

        for mat in matches:

            # Get the matching keypoints for each of the images
            img1_idx = mat.queryIdx
            img2_idx = mat.trainIdx

            # x - columns
            # y - rows
            (x1,y1) = kp1[img1_idx].pt
            (x2,y2) = kp2[img2_idx].pt

            # Draw a small circle at both co-ordinates
            # radius 4
            # colour blue
            # thickness = 1
            cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)
            cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

            # Draw a line in between the two points
            # thickness = 1
            # colour blue
            cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


    return out


def calcDeltaTheta(mapx1, mapy1, mapx2, mapy2, datax1, datay1, datax2, datay2):

    # Special cases
    if datax1 - datax2 == 0:
        if datay1 > datay2:
            angledata = math.pi/2
        else:
            angledata = math.pi*1.5
    elif datay1 - datay2 == 0:
        if datax1 > datax2:
            angledata = 0
        else:
            angledata = math.pi
    else:
        angledata = math.atan((datax1 - datax2) / (datay1 - datay2))


    if mapx1 - mapx2 == 0:
        if mapy1 > mapy2:
            anglemap = math.pi/2
        else:
            anglemap = math.pi*1.5
    elif mapy1 - mapy2 == 0:
        if mapx1 > mapx2:
            anglemap = 0
        else:
            anglemap = math.pi
    else:
        anglemap = math.atan((mapx1 - mapx2) / (mapy1 - mapy2))


    # Angle from data - angle from map = delta theta. By adding 2pi
    # then modding 2pi we guarantee that the result will be positive.
    return ((2*math.pi) + angledata - anglemap) % (math.pi)


# Warning: Assumes that images have not been rescaled or warped
def calcScale(mapx1, mapy1, mapx2, mapy2, datax1, datay1, datax2, datay2):
    return math.sqrt((datax1-datax2)**2 + (datay1-datay2)**2) / math.sqrt((mapx1-mapx2)**2 + (mapy1-mapy2)**2)


img1 = cv2.imread('map.png',0)          # queryImage
img2 = cv2.imread('data.png',0) # trainImage

# Initiate SIFT detector
sift = cv2.SIFT()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)

# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.2*n.distance:
        good.append([m])

# cv2.drawMatchesKnn expects list of lists as matches.
img3 = drawMatches(img1,kp1,img2,kp2,good)

# Calculate each delta for each pair of points and compare them to calculate theta.
# x11 = map x from point 1
# x12 = data x from point 1
# x21 = map x from point 2
# x22 = data x from point 2
# Same for y
theta = 0
scale = 0
dronex = 0
droney = 0
num = 0
for i in good:
    for mat in i:
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx
        (x11,y11) = kp1[img1_idx].pt
        (x12,y12) = kp2[img2_idx].pt

        for j in good:
            for mat2 in j:
                if j == i: continue # Dont calculate for equal points
                img1_idx = mat2.queryIdx
                img2_idx = mat2.trainIdx
                (x21,y21) = kp1[img1_idx].pt
                (x22,y22) = kp2[img2_idx].pt

                # TODO: Switch to medium element
                theta += calcDeltaTheta(x11, y11, x21, y21, x12, y12, x22, y22)
                scale += calcScale(x11, y11, x21, y21, x12, y12, x22, y22)
                #print 'Theta: ' + str(theta) + ' Angledata: ' + str(angledata) + ' Anglemap: ' + str(anglemap)
                num += 1

# Get average
theta /= num
scale /= num

# Get center of data image:
datacentery = img2.shape[0]/2
datacenterx = img2.shape[1]/2

num = 0
for i in good:
    for mat in i:
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx
        (mapx,mapy) = kp1[img1_idx].pt
        (datax,datay) = kp2[img2_idx].pt

        # Translate points by center of image
        datax -= datacenterx
        datay -= datacentery

        # Rotate points by theta
        dataxline = (datax*math.cos(-theta)) - (datay*math.sin(-theta))
        datayline = (datax*math.sin(-theta)) + (datay*math.cos(-theta))

        # Get negative vector to center adjusted by scale
        dataxline = -dataxline/scale
        datayline = -datayline/scale

        # Apply vector to original image
        dronex += mapx + dataxline
        droney += mapy + datayline

        num += 1

dronex /= num
droney /= num



print 'Theta: ' + str(theta)
print 'Scale: ' + str(scale)
print 'X: ' + str(dronex)
print 'Y: ' + str(droney)

drone = drawDrone(img1, dronex, droney, theta)

#plt.imshow(drone),plt.show()

#plt.imshow(img3),plt.show()


cv2.imwrite('res.png',img3)
cv2.imwrite('drone.png',drone)

