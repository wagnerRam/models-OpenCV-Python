import cv2 
import numpy as np

color = (255, 255, 255)
borda = 2

startPointA = (225,110)
endPointA = (225, 400)

startPointB = (350, 110)
endPointB = (350, 400)

startPointC = (80, 250)
endPointC = (490, 250)

# posLinhaA = 
# posLinhaB =
# posLinhaC = 
# posLinhaD = 
# posLinhaE = 
# poslinhaF = 

video = cv2.VideoCapture(2)

while True:
    
    _, frame = video.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    

    #cria linhas da imagem
    cv2.line(frame, startPointA, endPointA, color, borda)
    cv2.line(frame, startPointB, endPointB, color, borda)
    cv2.line(frame, startPointC, endPointC, color, borda)

    #define os paramentros low e high de (matiz, saturação e valor do objeto botão verde)
    low_button_green = np.array([71, 12, 242])
    high_button_green = np.array([100, 213, 255])
    #aplica uma mask no frame hsv

    mask = cv2.inRange(hsv_frame, low_button_green, high_button_green)        
    button_green = cv2.bitwise_and(frame, frame, mask = mask)
    
    #define os paramentros de cor, niveis low e high de (matiz, saturação e valor do objeto botão stop)
    low_stop = np.array([91, 9, 231])
    high_stop = np.array([255, 124, 250]) 
    #aplica uma mask no frame hsv
    mask_stop = cv2.inRange(hsv_frame, low_stop, high_stop)
    button_stop = cv2.bitwise_and(frame, frame, mask = mask_stop)

    gray_button_green = cv2.cvtColor(button_green, cv2.COLOR_BGR2GRAY)
    #cria uma matriz para aplicar preenchimento e limpeza de ruidos
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    #morph_close preenche o objeto detectado, deixando-o mais forte e com maior area
    preenchimentoGreen = cv2.morphologyEx(gray_button_green, cv2.MORPH_CLOSE, kernel)
    #morph_open, apliaca um filtro para eliminar ruidos na imagem
    ruido = cv2.morphologyEx(preenchimentoGreen, cv2.MORPH_OPEN, kernel, 1)
    #transforma a imagem em binaria de 0 a 255
    _, thresh_Green = cv2.threshold(ruido, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #aplica contorno no pixel
    contours_green, _ = cv2.findContours(thresh_Green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #--------------------------------------------------------------------------------------------------------------

    gray_button_stop = cv2.cvtColor(button_stop, cv2.COLOR_BGR2GRAY)
    #preenche a area do pixel do botão stop
    #cria uma matriz para aplicar preenchimento e limpeza de ruidos
    kernel_stop = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    #morph_close preenche o objeto detectado, deixando-o mais forte e com maior area
    preenchimento_stop = cv2.morphologyEx(gray_button_stop, cv2.MORPH_CLOSE, kernel)
    #transforma o preenchimento do stop em frame binario    #morph_open, apliaca um filtro para eliminar ruidos na imagem
    ruido_stop = cv2.morphologyEx(preenchimento_stop, cv2.MORPH_OPEN, kernel, 2)

    _, thresh_Stop = cv2.threshold(ruido_stop, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours_stop, _ = cv2.findContours(thresh_Stop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    
    #contorno e detecção da maior area dos botoes verdes
    if contours_green:
        maxAreaGrenn = cv2.contourArea(contours_green[0])
        contourMaxAreaId = 0
        i = 0
        
    for cnt in contours_green:
        if maxAreaGrenn < cv2.contourArea(cnt):
            maxAreaGrenn = cv2.contourArea(cnt)
            contourMaxAreaId = i
        i += 1
            
        cntMaxAreaGrenn = contours_green[contourMaxAreaId]
        x, y, w, h = cv2.boundingRect(cntMaxAreaGrenn)

        if maxAreaGrenn > 400:
            position_green = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            #print('X = ', x, 'Y = ', y, 'W = ', w, 'H = ', h)
            print("botao verde", maxAreaGrenn)   

    #contorno e detecção da maior area do botão stop 
    if contours_stop:
         maxAreaStop = cv2.contourArea(contours_stop[0])
         contourMaxAreaId = 0
         i = 0
        
    for cnt in contours_stop:
        if maxAreaStop < cv2.contourArea(cnt):
           maxAreaStop = cv2.contourArea(cnt)
           contourMaxAreaId = i
           i += 1
            
           cntMaxAreaStop = contours_stop[contourMaxAreaId]
           x, y, w, h = cv2.boundingRect(cntMaxAreaStop)

        if maxAreaStop < 2300:
            if maxAreaStop > 1000:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                #print("botao stop", maxAreaStop)   
    
    #abre os frames da camera com os filtros ou normal
    cv2.imshow('frame', frame)
    cv2.imshow('botao stop', thresh_Stop)
    cv2.imshow('thresh', thresh_Green)
    

    if cv2.waitKey(1) == (27): 
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
