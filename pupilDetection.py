import cv2
import numpy as np
import dlib

detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector_params.minThreshold = 10
blob_detector = cv2.SimpleBlobDetector_create(detector_params)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


def blob_process(img, threshold, side):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)    
    img = cv2.erode(img, None, iterations=1)
    img = cv2.dilate(img, None, iterations=1)
    # img = cv2.medianBlur(img, 5)
    keypoints = blob_detector.detect(img)

    if side == "l":
        cv2.imshow("left eye", img)
    else:
        cv2.imshow("right eye", img)
    
    return keypoints


def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def nothing(x):
    pass

def main():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('frame')
    cv2.createTrackbar('Left threshold', 'frame', 0, 255, nothing)
    cv2.createTrackbar('Right threshold', 'frame', 0, 255, nothing)
    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            x, y = face.left(), face.top()
            x1, y1 = face.right(), face.bottom()
            landmarks = predictor(gray, face)

            # left eye on screen
            left_point = (landmarks.part(36).x, landmarks.part(36).y)
            right_point = (landmarks.part(39).x, landmarks.part(39).y)

            center_top = midpoint(landmarks.part(37), landmarks.part(38))
            center_bottom = midpoint(landmarks.part(41), landmarks.part(40))

          
            width = 5
            #cv2.rectangle(frame, (landmarks.part(36).x - width, center_top[1] - width), (landmarks.part(39).x + width , center_bottom[1] + width),(0,225,255),1)
            eye = frame[center_top[1]-width: center_bottom[1] + width, landmarks.part(36).x - width : landmarks.part(39).x + width]
            
            threshold = r = cv2.getTrackbarPos('Left threshold', 'frame')
            keypoints = blob_process(eye, threshold, "l" )
        
            if len(keypoints) >=1:
                frame = cv2.circle(frame, (int(keypoints[0].pt[0] + landmarks.part(36).x - width ), center_top[1]-width+ int(keypoints[0].pt[1])), 1, (0, 255, 255), 5 )
  
            left_dot  = cv2.circle(frame, (landmarks.part(36).x, landmarks.part(36).y), 1, (0, 0, 255), -1 )
            right_dot = cv2.circle(frame,(landmarks.part(39).x, landmarks.part(39).y), 1, (0, 0, 255), -1 )

            # right eye on screen
            left_point = (landmarks.part(42).x, landmarks.part(42).y)
            right_point = (landmarks.part(45).x, landmarks.part(45).y)

            center_top = midpoint(landmarks.part(43), landmarks.part(44))
            center_bottom = midpoint(landmarks.part(47), landmarks.part(46))

           

            width = 5
            #cv2.rectangle(frame, (left_point[0] - width, center_top[1] - width), (right_point[0] + width , center_bottom[1] + width),(0,225,255),1)
            eye = frame[center_top[1] - width : center_bottom[1] + width, left_point[0] - width : right_point[0] + width]
            threshold = r = cv2.getTrackbarPos('Right threshold', 'frame')
            keypoints = blob_process(eye, threshold, "r" )
        
            if len(keypoints) >=1:
                frame = cv2.circle(frame, (int(keypoints[0].pt[0] + left_point[0] - width ), center_top[1] - width + int(keypoints[0].pt[1])), 1, (0, 255, 255), 5 )
            
            left_dot  = cv2.circle(frame, (landmarks.part(42).x, landmarks.part(42).y), 1, (0, 0, 255), -1 )
            right_dot = cv2.circle(frame,(landmarks.part(45).x, landmarks.part(45).y), 1, (0, 0, 255), -1 )
        
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

main()