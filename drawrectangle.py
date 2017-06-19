# import the necessary packages
import argparse
import cv2
import numpy as np
from sys import argv

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
refcount = 0
idcount = 0
target = open('lot.yml', 'w')

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, refcount, target, idcount

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))
        refcount += 1
        print refcount
        print (x, y)

        if refcount >= 4:
            # cv2.line(image, refPt[0], refPt[1], (255, 0, 0), 1)
            # cv2.line(image, refPt[1], refPt[2], (255, 0, 0), 1)
            cv2.line(image, refPt[2], refPt[3], (255, 0, 0), 1)
            cv2.line(image, refPt[3], refPt[0], (255, 0, 0), 1)
            refcount = 0
            print("-\n     id: " + str(idcount) + "\n          points: ["+
                  "[" + str(refPt[0][0]) + ","+str(refPt[0][1])+"],"+
                  "[" + str(refPt[1][0]) + ","+str(refPt[1][1])+"],"+
                  "[" + str(refPt[2][0]) + "," + str(refPt[2][1]) + "],"+
                  "[" + str(refPt[3][0]) + "," + str(refPt[3][1]) + "]]\n")
            target.write("-\n          id: " + str(idcount) + "\n          points: ["+
                  "[" + str(refPt[0][0]) + ","+str(refPt[0][1])+"],"+
                  "[" + str(refPt[1][0]) + ","+str(refPt[1][1])+"],"+
                  "[" + str(refPt[2][0]) + "," + str(refPt[2][1]) + "],"+
                  "[" + str(refPt[3][0]) + "," + str(refPt[3][1]) + "]]\n")
            points = np.array(refPt)
            # if parking_status[ind]:
            #     color = (0, 255, 0)
            # else:
            #     color = (0, 0, 255)
            cv2.drawContours(image, [points], contourIdx=-1,
                             color=(0, 0, 255), thickness=2, lineType=cv2.LINE_8)
            moments = cv2.moments(points)
            centroid = (int(moments['m10'] / moments['m00']) - 3, int(moments['m01'] / moments['m00']) + 3)
            cv2.putText(image, str(idcount), (centroid[0] + 1, centroid[1] + 1), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, str(idcount), (centroid[0] - 1, centroid[1] - 1), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, str(idcount), (centroid[0] + 1, centroid[1] - 1), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, str(idcount), (centroid[0] - 1, centroid[1] + 1), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, str(idcount), centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)






            refPt.pop()
            refPt.pop()
            refPt.pop()
            refPt.pop()
            idcount += 1
        elif refcount > 1:
            cv2.line(image, refPt[-2], refPt[-1], (255, 0, 0), 1)

        # print refPt[0]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        # refPt.append((x, y))
        cropping = False



    # draw a rectangle around the region of interest
    # cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
    cv2.imshow("image", image)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())






# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"])

clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
    cv2.imshow("image", image)
    # key = cv2.waitKey(1) & 0xFF
    res = cv2.waitKey(0)
    print 'You pressed %d (0x%x), 2LSB: %d (%s)' % (res, res, res % 2 ** 16,
                                                    repr(chr(res % 256)) if res % 256 < 128 else '?')
    # if the 'r' key is pressed, reset the cropping region
    if res == ord("r"):
        image = clone.copy()

    # if the 'c' key is pressed, break from the loop
    elif res == ord("c"):
        break

# if there are two reference points, then crop the region of interest
# from teh image and display it
# if len(refPt) == 2:
# 	roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
# 	cv2.imshow("ROI", roi)
# 	cv2.waitKey(0)

# close all open windows
cv2.destroyAllWindows()