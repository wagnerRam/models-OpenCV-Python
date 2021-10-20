import cv2
import numpy as np

cap = cv2.VideoCapture(2)
#= "trackbar window"
cv2.namedWindow("Trackbars")


def OnChange(val):
    return

def conputerTracking(frame, hue, sat, val):

    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

    lower_color = np.array([hue['min'], sat['min'], val['min']])
    upper_color = np.array([hue['max'], sat['max'], val['max']])
    mask = cv2.inRange(hsv_image, lower_color, upper_color)

    result = cv2.bitwise_and(frame, frame, mask = mask)

    gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY) 
    _, thresh_video = cv2.threshold(gray_image, 0,255, cv2.THRESH_BINARY| cv2.THRESH_OTSU )
    contours, hierarquia = cv2.findContours(thresh_video, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
     
    if contours:
        maxArea = cv2.contourArea(contours[0])
        contourMaxAreaId = 0
        i = 0
        
    for cnt in contours:
        
        if maxArea < cv2.contourArea(cnt):
            maxArea = cv2.contourArea(cnt)
            contourMaxAreaId = i
        i += 1
            
        cntMaxArea = contours[contourMaxAreaId]
        x, y, w, h = cv2.boundingRect(cntMaxArea)
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
    cv2.imshow('teste', thresh_video)
    cv2.imshow('frame', frame)
    return result

#função para ajustar as configurações do tracks
def limitesTrackbars():
    hue = {}
    hue["min"] = cv2.getTrackbarPos("Min Hue", "Trackbars")
    hue["max"] = cv2.getTrackbarPos("Max Hue", "Trackbars")

    sat = {}
    sat["min"] = cv2.getTrackbarPos("Min Saturation", "Trackbars")
    sat["max"] = cv2.getTrackbarPos("Max Saturation", "Trackbars")

    val = {}
    val["min"] = cv2.getTrackbarPos("Min Value", "Trackbars")
    val["max"] = cv2.getTrackbarPos("Max Value", "Trackbars")
    
    if hue["min"] > hue["max"]:
        cv2.setTrackbarPos("Max Hue", "Trackbars", hue["min"])
        hue["max"] = cv2.getTrackbarPos("Max Hue", "Trackbars")

    if sat["min"] > sat["max"]:
        cv2.setTrackbarPos("Max Saturation", "Trackbars", sat["min"])
        sat["max"] = cv2.getTrackbarPos("Max Saturation", "Trackbars")

    if val["min"] > val["max"]:
        cv2.setTrackbarPos("Max Value", "Trackbars", val["min"])
        val["max"] = cv2.getTrackbarPos("Max Value", "Trackbars")
    
    return hue, sat, val

    '''
        hue - = 071
        hue + = 100
        sat - = 017
        sat + = 213
        val - = 242
        val + = 255
    '''

#função do track
def trackbars():
    cv2.createTrackbar("Min Hue", "Trackbars", 0, 255, OnChange)
    cv2.createTrackbar("Max Hue", "Trackbars", 255, 255, OnChange)

    cv2.createTrackbar("Min Saturation", "Trackbars", 0, 255, OnChange)
    cv2.createTrackbar("Max Saturation", "Trackbars", 255, 255, OnChange)

    cv2.createTrackbar("Min Value", "Trackbars", 0, 255, OnChange)
    cv2.createTrackbar("Max Value", "Trackbars", 255, 255, OnChange)

    min_Hue = cv2.getTrackbarPos("Min Hue", "Trackbars")
    min_Hue = cv2.getTrackbarPos("Max Hue", "Trackbars")

    min_Sat = cv2.getTrackbarPos("Min Saturation", "Trackbars")
    min_Sat = cv2.getTrackbarPos("Min Saturation", "Trackbars")

    min_Val = cv2.getTrackbarPos("Min Value", "Trackbars")
    min_Val = cv2.getTrackbarPos("Min Value", "Trackbars")

while True:
    _, resizeFrame = cap.read()
    frame = cv2.resize(resizeFrame, (1200, 800))

    hue, sat, val = limitesTrackbars()
    trackbars()
    conputerTracking(frame, hue, sat, val)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
