# USAGE
# python detect_faces.py --face haarcascade_frontalface_default.xml --eye haarcascade_eyes_default.xml --image face_n_eyes.png

# import the necessary packages
import argparse
import cv2
import imutils

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required=True, help="Path to where the face cascade resides")
ap.add_argument("-e", "--eye" , required =True , help = "Path to where the eye cascade is located")
ap.add_argument("-i", "--image", required=True, help="Path to where the image file resides")
args = vars(ap.parse_args())

# load the image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# load the face detector and detect faces in the image
detector = cv2.CascadeClassifier(args["face"])
eye_detector=cv2.CascadeClassifier(args["eye"])
# handle face detection for OpenCV 2.4
if imutils.is_cv2():
	faceRects = detector.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5,
		minSize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

# otherwise handle face detection for OpenCV 3+
else:
	faceRects = detector.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5,
		minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

print("I found {} face(s)".format(len(faceRects)))

# loop over the faces and draw a rectangle around each
for (x, y, w, h) in faceRects:
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
	roi_gray= gray[y:y+h ,x:x+w]
	roi_color= image[y:y+h ,x:x+w]

# handle eye detection for OpenCV 2.4
if imutils.is_cv2():
	eyeRects = eye_detector.detectMultiScale(roi_gray, scaleFactor=1.05, minNeighbors=5,
		minSize=(3, 3), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

# otherwise handle eye detection for OpenCV 3+
else:
	eyeRects = eye_detector.detectMultiScale(roi_gray, scaleFactor=1.05, minNeighbors=5,
		minSize=(3, 3), flags=cv2.CASCADE_SCALE_IMAGE)

#loop over the eyes and draw rectangle around each

for (x,y,w,h) in eyeRects:
	cv2.rectangle(roi_color, (x, y), (x + w, y + h), (255, 0, 0), 2)
# show the detected faces
cv2.imshow("Faces and eyes", image)
cv2.waitKey(0)
cv2.imwrite('Face_n_eyes.png' , image)

