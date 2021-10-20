import cv2
import numpy as np
from paho.mqtt import client
from Mqtt import MQTT
import time

class Detect():

    def __init__(self, mqttClient:MQTT, video = cv2.VideoCapture(2)):
        self.__sourceVideo = video
        self.__mqtt = mqttClient
        self.__video()


    def __video(self,):

        buttons = {
            "startScan": False,
            "pauseScan": False,
            "stopScan" : False,
            "moveScan" : False,
            "pc": False,
        }

        while True:
            _, resizeFrame = self.__sourceVideo.read(0)
            frame = cv2.resize(resizeFrame, (1200, 800))

            #recorte dos botoes 
            startScan  = frame       [200 : 350, 230 : 400]
            pauseScan = frame        [200 : 350, 430 : 600]
            stopScan = frame    [200 : 350, 640 : 820]
            moveScan = frame [400 : 600, 230 : 400]
            inclinacao = frame   [380 : 600, 640 : 820]


            # transformando os recortes em hsv
            hsv_start = cv2.cvtColor(startScan, cv2.COLOR_BGR2HSV)
            hsv_pause = cv2.cvtColor(pauseScan, cv2.COLOR_BGR2HSV)
            hsv_stop = cv2.cvtColor(stopScan, cv2.COLOR_BGR2HSV)
            hsv_move = cv2.cvtColor(moveScan, cv2.COLOR_BGR2HSV)
            hsv_stMove = cv2.cvtColor(inclinacao, cv2.COLOR_BGR2HSV)


            #abrindo a camera dos recortes

            cv2.imshow('start', startScan)
            cv2.imshow('pause', pauseScan)
            cv2.imshow('stop',  stopScan)
            cv2.imshow('mover', moveScan)
            cv2.imshow('pc', inclinacao)


            #Niveis de cores dos botoes (matiz, saturação e valor) min ao max
            low_button_start = np.array([71, 12, 242])
            high_button_start = np.array([100, 213, 255])

            low_button_pause = np.array([71, 12, 242])
            high_button_pause = np.array([100, 213, 255])

            low_button_stop = np.array([0, 0, 224])
            high_button_stop = np.array([187, 63, 255])

            low_button_move = np.array([71, 12, 242])
            high_button_move = np.array([100, 213, 255])

            low_button_incli = np.array([15, 16, 207])
            high_button_incli = np.array([255, 207, 255])


            #aplicando mascara nos botoes
            mask_start = cv2.inRange(hsv_start, low_button_start, high_button_start)
            button_start = cv2.bitwise_and(startScan, startScan, mask = mask_start)

            mask_pause = cv2.inRange(hsv_pause, low_button_pause, high_button_pause)
            button_pause = cv2.bitwise_and(pauseScan, pauseScan, mask = mask_pause)
            
            mask_stop = cv2.inRange(hsv_stop, low_button_stop, high_button_stop)
            button_stop = cv2.bitwise_and(stopScan, stopScan, mask = mask_stop)
            
            mask_move = cv2.inRange(hsv_move, low_button_move, high_button_move)
            button_move = cv2.bitwise_and(moveScan, moveScan, mask = mask_move)

            mask_incli = cv2.inRange(hsv_stMove, low_button_incli, high_button_incli)
            button_incli = cv2.bitwise_and(inclinacao, inclinacao, mask = mask_incli)


            
            #-----------------APLICANDO FILTROS--------------------------------------------------------------------
            #Start
            gray_button_start = cv2.cvtColor(button_start, cv2.COLOR_BGR2GRAY)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
            preenchimentoStart = cv2.morphologyEx(gray_button_start, cv2.MORPH_CLOSE, kernel)
            ruidoStart = cv2.morphologyEx(preenchimentoStart, cv2.MORPH_OPEN, kernel, 1)
            _, thresh_Green_Start = cv2.threshold(ruidoStart, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            contours_start, _ = cv2.findContours(thresh_Green_Start, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


            #------------------------------------------------------------------------------------
            #Pause
            gray_button_pause = cv2.cvtColor(button_pause, cv2.COLOR_BGR2GRAY)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
            preenchimentoPause = cv2.morphologyEx(gray_button_pause, cv2.MORPH_CLOSE, kernel)
            ruido_pause = cv2.morphologyEx(preenchimentoPause, cv2.MORPH_OPEN, kernel, 1)
            _, thresh_Green_pause = cv2.threshold(ruido_pause, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            contours_pause, _ = cv2.findContours(thresh_Green_pause, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


            #----------------------------------------------------------------------------------
            #Stop
            gray_button_stop = cv2.cvtColor(button_stop, cv2.COLOR_BGR2GRAY)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            preenchimento_stop = cv2.morphologyEx(gray_button_stop, cv2.MORPH_CLOSE, kernel)
            ruido_stop = cv2.morphologyEx(preenchimento_stop, cv2.MORPH_OPEN, kernel, 0)
            _, thresh_Green_stop = cv2.threshold(ruido_stop, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            contours_stop, _ = cv2.findContours(thresh_Green_stop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


            #------------------------------------------------------------------------------------
            #Mover
            gray_button_move = cv2.cvtColor(button_move, cv2.COLOR_BGR2GRAY)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
            preenchimento_move = cv2.morphologyEx(gray_button_move, cv2.MORPH_CLOSE, kernel)
            ruido_move = cv2.morphologyEx(preenchimento_move, cv2.MORPH_OPEN, kernel, 1)
            _, thresh_Green_move = cv2.threshold(ruido_move, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            contours_move, _ = cv2.findContours(thresh_Green_move, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


            #------------------------------------------------------------------------------------
            #inclinação
            gray_button_incli = cv2.cvtColor(button_incli, cv2.COLOR_BGR2GRAY)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
            preenchimento_incli = cv2.morphologyEx(gray_button_incli, cv2.MORPH_CLOSE, kernel)
            ruido_incli = cv2.morphologyEx(preenchimento_incli, cv2.MORPH_OPEN, kernel, 0)
            _, thresh_Green_incli = cv2.threshold(ruido_incli, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            contours_incli, _ = cv2.findContours(thresh_Green_incli, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


            #contorno e detecção da maior area dos botoes
            if contours_start:
                maxAreaGrenn = cv2.contourArea(contours_start[0])
                contourMaxAreaId = 0
                i = 0

            for cnt in contours_start:
                if maxAreaGrenn < cv2.contourArea(cnt):
                    maxAreaGrenn = cv2.contourArea(cnt)
                    contourMaxAreaId = i
                i += 1

                cntMaxAreaGrenn = contours_start[contourMaxAreaId]
                x, y, w, h = cv2.boundingRect(cntMaxAreaGrenn)
                if maxAreaGrenn > 290:
                    #cv2.rectangle(frame, (255, 220), (375, 325), (0, 0, 255), 2)
                    buttons.update({"startScan": True})
                else: 
                    buttons.update({"startScan": False})
                    

                # PAUSE -------------------------------------------------------------------------------
            if contours_pause:
                maxAreaGrenn = cv2.contourArea(contours_pause[0])
                contourMaxAreaId = 0
                i = 0

            for cnt in contours_pause:
                if maxAreaGrenn < cv2.contourArea(cnt):
                    maxAreaGrenn = cv2.contourArea(cnt)
                    contourMaxAreaId = i
                i += 1

                cntMaxAreaGrenn = contours_pause[contourMaxAreaId]
                x, y, w, h = cv2.boundingRect(cntMaxAreaGrenn)
                if maxAreaGrenn > 500:
                    #cv2.rectangle(frame, (455, 220), (575, 325), (0, 0, 255), 2)
                    buttons["pauseScan"] = True
                else: 
                    buttons["pauseScan"] = False

                #STOP---------------------------------------------------------------------------------
            if contours_stop:
                maxAreaGrenn = cv2.contourArea(contours_stop[0])
                contourMaxAreaId = 0
                i = 0

            for cnt in contours_stop:
                if maxAreaGrenn < cv2.contourArea(cnt):
                    maxAreaGrenn = cv2.contourArea(cnt)
                    contourMaxAreaId = i
                i += 1

                cntMaxAreaGrenn = contours_stop[contourMaxAreaId]
                x, y, w, h = cv2.boundingRect(cntMaxAreaGrenn)
                if maxAreaGrenn > 3200:
                    #cv2.rectangle(frame, (660, 220), (770, 325), (0, 0, 255), 2)    
                    buttons["stopScan"] = True
                else:
                    buttons["stopScan"] = False


                #MOVE-------------------------------------------------------------------------------------
            if contours_move:
                maxAreaGrenn = cv2.contourArea(contours_move[0])
                contourMaxAreaId = 0
                i = 0

            for cnt in contours_move:
                if maxAreaGrenn < cv2.contourArea(cnt):
                    maxAreaGrenn = cv2.contourArea(cnt)
                    contourMaxAreaId = i
                i += 1

                cntMaxAreaGrenn = contours_move[contourMaxAreaId]
                x, y, w, h = cv2.boundingRect(cntMaxAreaGrenn)
                if maxAreaGrenn > 500:
                    #cv2.rectangle(frame, (255, 420), (375, 525), (0, 0, 255), 2)
                    buttons["moveScan"] = True
                else: 
                    buttons["moveScan"] = False


                #STOP MOVE-------------------------------------------------------------------------------------
            if contours_incli:
                maxAreaGrenn = cv2.contourArea(contours_incli[0])
                contourMaxAreaId = 0
                i = 0

            for cnt in contours_incli:
                if maxAreaGrenn < cv2.contourArea(cnt):
                    maxAreaGrenn = cv2.contourArea(cnt)
                    contourMaxAreaId = i
                i += 1

                cntMaxAreaGrenn = contours_incli[contourMaxAreaId]
                x, y, w, h = cv2.boundingRect(cntMaxAreaGrenn)
                if maxAreaGrenn > 2550:
                    #cv2.rectangle(frame, (655, 380), (780, 500), (0, 0, 255), 2)                 
                    buttons["pc"] = True
                else:
                    buttons["pc"] = False

            
            self.__mqtt.publish_data('botoes', buttons)
            #print(buttons)
                    
            cv2.imshow('frame', frame)
            print(buttons)
            
            if cv2.waitKey(1) == (27):
                break

        cv2.waitKey(0)
        cv2.destroyAllWindows()

