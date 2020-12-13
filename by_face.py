import cv2
from imutils import build_montages
from time import sleep
import numpy as np
import os
import imutils
import dlib
from skimage import io
from scipy.spatial import distance

cwd = os.getcwd()
print(cwd)

# construct the argument parser and parse the arguments
prototxt = "MobileNetSSD_deploy.prototxt"
model = "MobileNetSSD_deploy.caffemodel"
min_confidence = 0.8
montageW = 1
montageH = 1

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
CONSIDER = set(["dog", "person", "cat", "bird"])
objCount = {obj: 0 for obj in CONSIDER}
frameDict = {}
net = cv2.dnn.readNetFromCaffe(prototxt, model)

list_of_persons = ["Ира", "Ольга"]
#https://github.com/sozykin/dlpython_course/blob/master/computer_vision/foto_comparison/foto_verification.ipynb
sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()
list_of_descriptors = []
for p in list_of_persons:
    img_name = "foto//Фото " + p + ".jpg"
    img = io.imread(img_name)
    dets = detector(img, 1)
    d =dets[0]
    shape = sp(img, d)
    face_descriptor = facerec.compute_face_descriptor(img, shape)
    list_of_descriptors.append(face_descriptor)
print(len(list_of_descriptors))

video_capture = cv2.VideoCapture(0)
anterior = 0

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    frame = imutils.resize(frame, width=800)
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                 0.007843, (300, 300), 127.5)
    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    # reset the object count for each object in the CONSIDER set
    objCount = {obj: 0 for obj in CONSIDER}
    # loop over the detections

    confidence = detections[0, 0, 0, 2]

    # filter out weak detections by ensuring the confidence is
    # greater than the minimum confidence
    if confidence > min_confidence:
        # extract the index of the class label from the
        # detections
        idx = int(detections[0, 0, 0, 1])
        # check to see if the predicted class is in the set of
        # classes that need to be considered
        if CLASSES[idx] in CONSIDER:
            # increment the count of the particular object
            objCount[CLASSES[idx]] += 1

            # compute the (x, y)-coordinates of the bounding box
            # for the object
            box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            if CLASSES[idx] != "person":
                object_name = CLASSES[idx]
            else:
                object_name = "person"
                width = endX-startX
                # cut image part with person's face
                #cv2.imwrite("frame%d.jpg" , frame)
                img = frame[startY:(startY+width), startX:(startX+width) ].copy()
                #cv2.imwrite("frame%pers_frame.jpg" , pers_frame)

                # get discriptor of the face
                dets = detector(img, 1)
                if len(dets)==1:
                    d = dets[0]
                    shape = sp(img, d)
                    # upper lip
                    xul = shape.part(51).x+startX
                    yul = shape.part(51).y+startY
                    #cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)
                    # lower lip
                    xll = shape.part(57).x+startX
                    yll = shape.part(57).y+startY
                    #cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)
                    print("length between lips " + str(np.sqrt(np.square(xul-xll)+np.sqrt(np.square(yul-yll))) ))

                    face_descriptor = facerec.compute_face_descriptor(img, shape)
                    for k, descriptor in enumerate(list_of_descriptors):
                        a = distance.euclidean(face_descriptor, descriptor)
                        if a < 0.60:
                            object_name = list_of_persons[k] +"   descriptor = "+str(a)
                if object_name == "person":
                    object_name = "unknown person"


                # detected in the frame
            #print("confidence " + str(confidence) + "  " + object_name)
            cv2.putText(frame, object_name, (startX, startY-3), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)

            # draw the bounding box around the detected object on
            # the frame
            cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)


    rpiName = 'camera'
    # draw the sending device name on the frame
    cv2.putText(frame, rpiName, (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # draw the object count on the frame
    label = ", ".join("{}: {}".format(obj, count) for (obj, count) in
                      objCount.items())
    cv2.putText(frame, label, (10, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # update the new frame in the frame dictionary
    frameDict[rpiName] = frame

    # build a montage using images in the frame dictionary
    montages = build_montages(frameDict.values(), (w, h), (montageW, montageH))

    # display the montage(s) on the screen
    for (i, montage) in enumerate(montages):
        cv2.imshow("Home pet location monitor ({})".format(i),
                   montage)


    # detect any kepresses
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
#cv2.destroyAllWindows()

