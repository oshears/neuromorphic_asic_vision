import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)

while True:
    # get image
    ret, img = cap.read()
    
    if ret:
        # convert to grayscale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # convert to black and white
        (thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        
        # mirror the image
        img = cv2.flip(img, 1)

        # crop the image
        img = img[0:480,0:480]


        results = np.ndarray(16)
	
        ctr = 0

        for row in range(0,480,120):
            for col in range(0,480,120):

                # sum up the white pixels
                totalNumWhite = img[row:row+120,col:col+120].sum() / 255

                # if more than half are white, the sub image is white
                results[ctr] = 1 if totalNumWhite >= 7200 else 0

                # increment counter
                ctr += 1
        
        print(results[0:3])
        print(results[3:6])
        print(results[6:9])
        print("==========")
