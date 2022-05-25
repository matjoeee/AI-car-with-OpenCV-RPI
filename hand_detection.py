# a code by "https://github.com/mohammadreza-sharifi"
# used in the Practice Enterprice project of Raul Lopez & Matthew Wuyts
# students at Thomas More, Belgium

import cv2
import mediapipe as mp
import time
import paho.mqtt.publish as publish
 
#raspberry pi ip address
MQTT_SERVER = "192.168.0.4"
MQTT_PATH = "test_channel"

mp_draw=mp.solutions.drawing_utils
mp_hand=mp.solutions.hands

tipIds=[4,8,12,16,20]

#camera gebruiken voor de hand detectie
cap = cv2.VideoCapture(0)
mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands()
mpDraw = mp.solutions.drawing_utils
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4,2)


with mp_hand.Hands(min_detection_confidence=0.5,
               min_tracking_confidence=0.5) as handen:
    while True:
        success, image = cap.read()
        RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(RGB_image)
        multiLandMarks = results.multi_hand_landmarks
        if multiLandMarks:
            handList = []
            for handLms in multiLandMarks:
                mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
                for idx, lm in enumerate(handLms.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    handList.append((cx, cy))
                for point in handList:
                    cv2.circle(image, point, 10, (255, 255, 0), cv2.FILLED)
                    upCount = 0
                    for coordinate in finger_Coord:
                        if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
                            upCount += 1
                        if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
                            upCount += 1
                    cv2.putText(image, str(upCount), (150,150), cv2.FONT_HERSHEY_PLAIN, 12, (0,255,0), 12)
                            #print(upCount)
                            
                    publish.single(MQTT_PATH, upCount, hostname=MQTT_SERVER)        #data naar de Raspberry sturen
                    if upCount == 8:
                        cv2.putText(image, 'Forward', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4) #5 vingers = vooruit

                    elif upCount == 4:
                        cv2.putText(image, 'Backward', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4) #4 vingers = achteruit

                    elif upCount == 0:
                        cv2.putText(image, 'Stop', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4) #0 vingers = stoppen

                    elif upCount == 2:
                        cv2.putText(image, 'Right', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4) #2 vingers = rechts draaien

                    elif upCount == 1:
                        cv2.putText(image, 'Left', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4) #1 vingers = links draaien

        cv2.imshow("result",image)      #venster openen met de camerabeeld
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

cap.release()
cv2.cv2.destroyAllWindows()
