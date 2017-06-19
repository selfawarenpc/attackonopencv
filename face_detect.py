import cv2
import sys

# Get user supplied values
# imagePath = sys.argv[1]
imagePath = 'lot4.jpg'
cascPath = "cars.xml"

# Create the haar cascade
car_cascade = cv2.CascadeClassifier(cascPath)

# Read the image
img = cv2.imread(imagePath)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cars = car_cascade.detectMultiScale(gray, 1.1, 1)

for (x, y, w, h) in cars:
    # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 8)
    cv2.imshow("Objects found", img)
    # cv2.waitKey(0)
    # img = cv2.imread(imagePath)

cv2.waitKey(0)

