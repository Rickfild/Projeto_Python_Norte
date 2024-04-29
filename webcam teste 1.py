import cv2
import mediapipe as mp

video = cv2.VideoCapture(0)

hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=2)
mpDraw = mp.solutions.drawing_utils

while True:
    check, img = video.read()
    if not check:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hand.process(imgRGB)
    pontosMaos = results.multi_hand_landmarks
    h,w,_ = img.shape
    pontos = []

    if pontosMaos:
        for landmarks in pontosMaos:
            mpDraw.draw_landmarks(img,landmarks,hand.HAND_CONNECTIONS)
            for id, landmark in enumerate(landmarks.landmark):
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                #cv2.putText(img, str(id),(cx, cy+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
                pontos.append((cx,cy))

        dedos = [8,12,16,20]
        contador=0
        if pontos:
            if pontos[4][0] < pontos[2][0]:
                contador +=1
            for x in dedos:
                if pontos[x][1] < pontos[x-2][1]:
                    contador +=1

        cv2.rectangle(img,(80,10),(200,100),(255,0,0), -1)
        cv2.putText(img, str(contador),(100,100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 0), 5)


    cv2.imshow("teste webcam", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()