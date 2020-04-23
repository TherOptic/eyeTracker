'''
Code demonstrating eyetracking using OpenCV

To run: python3 pupilDetection.py

Press q to quit  

Some code modified from:
https://medium.com/@stepanfilonov/tracking-your-eyes-with-python-3952e66194a6
https://pysource.com/2019/01/04/eye-motion-tracking-opencv-with-python/
'''

import cv2
import numpy as np
import dlib, time, random

detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector_params.minThreshold = 10
blob_detector = cv2.SimpleBlobDetector_create(detector_params)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


def blob_process(img, threshold, side):
    '''
    Returns keyspoints where the pupils are
    '''
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
    _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)    
    img = cv2.erode(img, None, iterations=1)
    img = cv2.dilate(img, None, iterations=1)
    # img = cv2.medianBlur(img, 5)
    keypoints = blob_detector.detect(img)
    
    return keypoints


def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)


def nothing(x):
    pass


def main():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('frame', 0)

    side = True

    cv2.createTrackbar('Left threshold', 'frame', 0, 255, nothing)
    cv2.createTrackbar('Right threshold', 'frame', 0, 255, nothing)
    start = time.time()

    cv2.resizeWindow('frame', 1080,1920)
    dotx = random.randint(0, 500)
    doty = random.randint(0, 500)
    oldcoordleft = False
    oldcoordright = False
    while True:

        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)


        for face in faces:
            x, y = face.left(), face.top()
            x1, y1 = face.right(), face.bottom()
            landmarks = predictor(gray, face)

            # Process Left eye
            left_point = (landmarks.part(36).x, landmarks.part(36).y)
            right_point = (landmarks.part(39).x, landmarks.part(39).y)

            center_top = midpoint(landmarks.part(37), landmarks.part(38))
            center_bottom = midpoint(landmarks.part(41), landmarks.part(40))
          
            width = 5 # padding width of eye frame
            eye = frame[center_top[1] - width: center_bottom[1] + width, landmarks.part(36).x - width : landmarks.part(39).x + width] # frame containing left eye
            
            threshold = r = cv2.getTrackbarPos('Left threshold', 'frame')
            keypoints = blob_process(eye, threshold, "l" )
        
            
            if len(keypoints) >= 1 :
                oldcoordleft =  (int(keypoints[0].pt[0] + landmarks.part(36).x - width ), center_top[1]-width+ int(keypoints[0].pt[1]))
                frame = cv2.circle(frame, oldcoordleft, 1, (0, 255, 255), 5 )
            else:
                if oldcoordleft != False:
                    frame = cv2.circle(frame, oldcoordleft, 1, (0, 255, 255), 5 )


            # Draw dots showing corners of left eye
            left_dot  = cv2.circle(frame, (landmarks.part(36).x, landmarks.part(36).y), 1, (0, 0, 255), -1 )
            right_dot = cv2.circle(frame,(landmarks.part(39).x, landmarks.part(39).y), 1, (0, 0, 255), -1 )

            # Process right eye
            left_point = (landmarks.part(42).x, landmarks.part(42).y)
            right_point = (landmarks.part(45).x, landmarks.part(45).y)

            center_top = midpoint(landmarks.part(43), landmarks.part(44))
            center_bottom = midpoint(landmarks.part(47), landmarks.part(46))

            eye = frame[center_top[1] - width : center_bottom[1] + width, left_point[0] - width : right_point[0] + width]

            threshold = r = cv2.getTrackbarPos('Right threshold', 'frame')
            keypoints = blob_process(eye, threshold, "r" )
        
            if len(keypoints) >= 1 :
                oldcoordright = (int(keypoints[0].pt[0] + left_point[0] - width ), center_top[1] - width + int(keypoints[0].pt[1]))
                frame = cv2.circle(frame, oldcoordright, 1, (0, 255, 255), 5 )
            else:
                if oldcoordright != False:
                    frame = cv2.circle(frame, oldcoordright, 1, (0, 255, 255), 5 )

            # Draw dots showing corners of right eye
            left_dot  = cv2.circle(frame, (landmarks.part(42).x, landmarks.part(42).y), 1, (0, 0, 255), -1 )
            right_dot = cv2.circle(frame,(landmarks.part(45).x, landmarks.part(45).y), 1, (0, 0, 255), -1 )
        

        now = time.time()

        if now - start > 2:
            if side == True:
                dotx = random.randint(0, 100) 
                side = False
            else:
                dotx = random.randint(400, 500) 
                side = True
            doty = random.randint(0, 500) 
            start = time.time()

        frame  = cv2.flip(frame, 1)

        dot = cv2.circle(frame, (dotx, doty), 5, (0, 255, 0), 5 )
        
        cv2.imshow("frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()

main()