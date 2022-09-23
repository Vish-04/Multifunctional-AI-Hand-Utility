import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(self.mode, self.maxHands, 0, self.detectionCon, self.trackCon)

        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self, img, handNo=0, draw=True):

        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        return self.lmList

    def findFingersUp(self, img, handNo=0):

        finger_index = [0, 0, 0, 0, 0]

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            if self.lmList[4][1] > self.lmList[2][1]:
                finger_index[0] = 1
            if self.lmList[8][2] < self.lmList[6][2]:
                finger_index[1] = 1
            if self.lmList[12][2] < self.lmList[10][2]:
                finger_index[2] = 1
            if self.lmList[16][2] < self.lmList[14][2]:
                finger_index[3] = 1
            if self.lmList[20][2] < self.lmList[18][2]:
                finger_index[4] = 1
        return finger_index


def main():

    # cap is the capture, videocapture specifies which camera to use, 0 being default
    cap = cv2.VideoCapture(0)

    # Used to calculate fps
    pTime = 0
    cTime = 0

    # creating object that detects hands
    detector = handDetector()
    print(detector)

    while True:

        # img is the actual display being put out
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if not len(lmList) == 0:
            print(lmList[4])

        # Calculating the fps
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        # Putting text on screen, (capture to use, text, position of text, text font, size of text, color of text, text
        # thickness)
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,125,125), 3)

        # a method used to display an image to a window
        cv2.imshow("Image", img)
        # displays a window for a certain amount of miliseconds and destroys it
        cv2.waitKey(1)


if __name__ == "__main__":
    main()