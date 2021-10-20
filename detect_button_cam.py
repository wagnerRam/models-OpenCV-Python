import cv2
import numpy as np


video = cv2.VideoCapture(0)

def detect_button():

    start_button = 0
    pause_button = 0 
    move_to_scan = 0
    stop = 0
    pc = 0

    print(start_button, pause_button, stop, move_to_scan, pc)

    while True:

        _, frame = video.read()
        
        #recorte dos botoes 
        start  = frame [130 : 200, 140 : 220]
        pause = frame [130 : 200, 235 : 310]
        stop_scan = frame [140 : 210, 340 : 420]
        move_to_scan = frame [200 : 290, 130 : 230 ]
        inclinacao = frame [200 : 300, 340 : 430 ]

        # transformando os recortes em hsv
        hsv_start = cv2.cvtColor(start, cv2.COLOR_BGR2HSV)
        hsv_pause = cv2.cvtColor(pause, cv2.COLOR_BGR2HSV)
        hsv_stop = cv2.cvtColor(stop_scan, cv2.COLOR_BGR2HSV)
        hsv_move = cv2.cvtColor(move_to_scan, cv2.COLOR_BGR2HSV)
        hsv_stMove = cv2.cvtColor(inclinacao, cv2.COLOR_BGR2HSV)

        #abrindo a camera dos recortes
        cv2.imshow('start', start)
        cv2.imshow('pause', pause)
        cv2.imshow('stop', stop_scan)
        cv2.imshow('mover', move_to_scan)
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
        button_start = cv2.bitwise_and(start, start, mask = mask_start)

        mask_pause = cv2.inRange(hsv_pause, low_button_pause, high_button_pause)
        button_pause = cv2.bitwise_and(pause, pause, mask = mask_pause)
        
        mask_stop = cv2.inRange(hsv_stop, low_button_stop, high_button_stop)
        button_stop = cv2.bitwise_and(stop_scan, stop_scan, mask = mask_stop)
        
        mask_move = cv2.inRange(hsv_move, low_button_move, high_button_move)
        button_move = cv2.bitwise_and(move_to_scan, move_to_scan, mask = mask_move)

        mask_incli = cv2.inRange(hsv_stMove, low_button_incli, high_button_incli)
        button_incli = cv2.bitwise_and(inclinacao, inclinacao, mask = mask_incli)


        
        #-----------------APLICANDO FILTROS--------------------------------------------------------------------
        #start
        gray_button_start = cv2.cvtColor(button_start, cv2.COLOR_BGR2GRAY)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        preenchimentoStart = cv2.morphologyEx(gray_button_start, cv2.MORPH_CLOSE, kernel)
        ruidoStart = cv2.morphologyEx(preenchimentoStart, cv2.MORPH_OPEN, kernel, 1)
        _, thresh_Green_Start = cv2.threshold(ruidoStart, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        contours_start, _ = cv2.findContours(thresh_Green_Start, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        #------------------------------------------------------------------------------------
        #pause
        gray_button_pause = cv2.cvtColor(button_pause, cv2.COLOR_BGR2GRAY)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        preenchimentoPause = cv2.morphologyEx(gray_button_pause, cv2.MORPH_CLOSE, kernel)
        ruido_pause = cv2.morphologyEx(preenchimentoPause, cv2.MORPH_OPEN, kernel, 1)
        _, thresh_Green_pause = cv2.threshold(ruido_pause, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        contours_pause, _ = cv2.findContours(thresh_Green_pause, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        #----------------------------------------------------------------------------------
        #stop
        gray_button_stop = cv2.cvtColor(button_stop, cv2.COLOR_BGR2GRAY)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        preenchimento_stop = cv2.morphologyEx(gray_button_stop, cv2.MORPH_CLOSE, kernel)
        ruido_stop = cv2.morphologyEx(preenchimento_stop, cv2.MORPH_OPEN, kernel, 0)
        _, thresh_Green_stop = cv2.threshold(ruido_stop, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        contours_stop, _ = cv2.findContours(thresh_Green_stop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        #------------------------------------------------------------------------------------
        #move
        gray_button_move = cv2.cvtColor(button_move, cv2.COLOR_BGR2GRAY)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        preenchimento_move = cv2.morphologyEx(gray_button_move, cv2.MORPH_CLOSE, kernel)
        ruido_move = cv2.morphologyEx(preenchimento_move, cv2.MORPH_OPEN, kernel, 1)
        _, thresh_Green_move = cv2.threshold(ruido_move, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        contours_move, _ = cv2.findContours(thresh_Green_move, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        #------------------------------------------------------------------------------------
        #incli
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
            cv2.rectangle(frame, (150, 140), (150 + 70, 130 + 65), (0, 0, 255), 2)
            start_button = 1
            print('start')


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
            cv2.rectangle(frame, (251, 142), (325, 200), (0, 0, 255), 2)
            pause_button = 1
            print('pause')

            
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
            if maxAreaGrenn > 300:
                cv2.rectangle(frame, (355, 140), (428, 210), (0, 0, 255), 2)
                stop = 1
                print('stop')


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
            cv2.rectangle(frame, (125, 290), (220, 200), (0, 0, 255), 2)
            move = 1
            print('mover')


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
            if maxAreaGrenn > 550:
                cv2.rectangle(frame, (435, 290), (350, 210), (0, 0, 255), 2)
                pc = 1
                print("PC On")
        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) == (27):
            break

    
def main():

    detect_button()
    


    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()
