# MediaPipePose
import cv2
import mediapipe as mp
import math
import os
import requests

class Point:
    x = 0
    y = 0

#각도가 성공 기준에 들어갈 경우에는, len 값을 올려주어 이 len 값을 기준으로 score를 매길 예정.
ready_success_len = swing_success_len = finish_success_len = 0
#피드백 문구로 넣을 예정.
ready_feedback = swing_feedback = finish_feedback = ""
# 측정하지 못했을 경우에는 1을 return하는 변수
isErrorSwing = isErrorReady = isErrorFinish = 0 #true or false

#p1, p2, p3 세 점을 입력받아 p2 중심으로 각도를 return하는 함수.
def Angle(P1, P2, P3):
    a = math.sqrt(math.pow(P1.x - P2.x, 2) + math.pow(P1.y - P2.y, 2))
    b = math.sqrt(math.pow(P2.x - P3.x, 2) + math.pow(P2.y - P3.y, 2))
    c = math.sqrt(math.pow(P1.x - P3.x, 2) + math.pow(P1.y - P3.y, 2))
    angle = math.acos((a * a + b * b - c * c) / (2 * a * b))
    return (angle * 180) / PI

#p11, p12의 중심점, p2, p3의 각도를 return하는 함수.
def Angle2(P11, P12, P2, P3):
    P1 = Point()
    P1.x = (P11.x + P12.x) / 2
    P1.y = (P11.y + P12.y) / 2
    a = math.sqrt(math.pow(P1.x - P2.x, 2) + math.pow(P1.y - P2.y, 2))
    b = math.sqrt(math.pow(P2.x - P3.x, 2) + math.pow(P2.y - P3.y, 2))
    c = math.sqrt(math.pow(P1.x - P3.x, 2) + math.pow(P1.y - P3.y, 2))
    angle = math.acos((a * a + b * b - c * c) / (2 * a * b))
    return (angle * 180) / PI

#피타코라스 활용 거리 return 함수
def Distance(P1,P2):
    distance = math.sqrt(pow(P1.x-P2.x, 2)+pow(P1.y-P2.y, 2))
    return distance

# 각 각도에 대하여 ox 판별하는 함수. (eval_ready, eval_swing, eval_finish)
# rs : 해당 각도
# skeleton : 각 각도에 대한 한글명
# minNum, maxNum : 스켈레톤에 최솟값, 최댓값
def eval_ready(rs, skeleton, minNum, maxNum):
    global ready_success_len, ready_feedback, isErrorReady
    if skeleton == "keyCheck":
        if rs < 110:
            isErrorReady = 1
            ready_success_len = 0
        return
    if minNum < rs < maxNum:
        ready_success_len += 1
    else:
        if ready_feedback == "":
            ready_feedback = skeleton
        else:
            ready_feedback = ready_feedback + ", " + skeleton


def eval_swing(rs, skeleton, minNum, maxNum):
    global swing_success_len, swing_feedback, isErrorSwing
    if skeleton == "keyCheck":
        if rs < 110:
            isErrorSwing = 1
            swing_success_len = 0
        return
    if minNum < rs < maxNum:
        swing_success_len += 1
    else:
        if swing_feedback == "":
            swing_feedback = skeleton
        else:
            swing_feedback = swing_feedback + ", " + skeleton

def eval_finish(rs, skeleton, minNum, maxNum):
    global finish_success_len, finish_feedback, isErrorFinish
    if skeleton == "keyCheck":
        if rs < 110:
            isErrorFinish = 1
            finish_success_len = 0
        return
    if minNum < rs < maxNum:
        finish_success_len += 1
    else:
        if finish_feedback == "":
            finish_feedback = skeleton
        else:
            finish_feedback = finish_feedback + ", " + skeleton

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
PI = 3.1415926535
num = -1

#프로 자세기반 기준 점수.
BASESCORE_READY = [72.53, 69.72, 72.47, 85.34, 172.4, 173.95]
BASESCORE_SWING = [156.0, 170.63, 169.8, 131.81, 138.6]
BASESCORE_FINISH = [144.31, 162.99]

DATA_DIR = os.getcwd() + "/images"
IMAGE_FILES = os.listdir(DATA_DIR)
IMAGE_FILES.sort()
# print(IMAGE_FILES)
length1 = 0
length2 = 0
length3 = 0

with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=2,
        min_detection_confidence=0.5) as pose:
    for idx, file in enumerate(IMAGE_FILES):
        if (file.find('iron') == -1): continue
        else: num += 1
        file = DATA_DIR + '/' + file
        image = cv2.imread(file)
        image_height, image_width, _ = image.shape

        # Convert the BGR image to RGB before processing.
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.pose_landmarks:
            if(file.find('first') != -1) : isErrorReady = 1
            elif(file.find('second') != -1): isErrorSwing = 1
            elif(file.find('third') != -1): isErrorFinish = 1
            continue
        annotated_image = image.copy()
        ll = [] # 각 번호마다의 위치를 저장하기 위한 임시 배열.

        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = image.shape
            p = Point()
            p.x = int(lm.x * w)
            p.y = int(lm.y * h)
            ll.append(p)
            cv2.putText(annotated_image, str(id), (p.x, p.y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)

        # Draw pose landmarks on the image.
        mp_drawing.draw_landmarks(
            annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)


        cv2.imwrite('images_result/annotated_image' + str(num) + '.png', annotated_image)
        if (file.find('first') != -1):
            one = Angle2(ll[23], ll[24], ll[27], ll[28])
            two = Angle2(ll[23], ll[24], ll[28], ll[27])
            three = Angle(ll[12], ll[11], ll[13])
            four = Angle(ll[11], ll[12], ll[14])
            five = Angle(ll[11], ll[13], ll[15])
            six = Angle(ll[12], ll[14], ll[16])
            length1 = Distance(ll[0], ll[25])
            eval_ready(round(one, 2), "왼발", 65, 89)
            eval_ready(round(two, 2), "오른발", 61, 89)
            eval_ready(round(three, 2), "왼쪽 어깨", 50, 93)
            eval_ready(round(four, 2), "오른쪽 어깨", 60, 92)
            eval_ready(round(five, 2), "왼쪽 팔꿈치", 155, 180)
            eval_ready(round(six, 2), "오른쪽 팔꿈치", 160, 180)
            eval_ready(round(length1, 2), "keyCheck", 0, 0)

        if (file.find('second') != -1):
            ones = Angle(ll[12], ll[24], ll[26])
            twos = Angle(ll[24], ll[26], ll[28])
            threes = Angle(ll[23], ll[25], ll[27])
            fours = Angle(ll[11], ll[12], ll[14])
            fives = Angle(ll[12], ll[14], ll[16])
            length2 = Distance(ll[0], ll[25])
            eval_swing(round(ones, 2), "오른쪽 허리", 140, 180)
            eval_swing(round(twos, 2), "오른쪽 무릎", 167, 180)
            eval_swing(round(threes, 2), "왼쪽 무릎", 165, 180)
            eval_swing(round(fours, 2), "오른쪽 어깨", 110, 175)
            eval_swing(round(fives, 2), "오른쪽 팔꿈치", 70, 155)
            eval_swing(round(length2, 2), "keyCheck", 0, 0)

        if (file.find('third') != -1):
            onef = Angle(ll[24], ll[26], ll[28])
            twof = Angle(ll[12], ll[24], ll[26])
            length3 = Distance(ll[0], ll[25])
            eval_finish(round(onef, 2), "오른쪽 무릎", 125, 180)
            eval_finish(round(twof, 2), "오른쪽 허리", 155, 175)
            eval_finish(round(length3, 2), "keyCheck", 0, 0)

    rDict = {6: 'Perfect', 5: 'Good', 4: 'Good', 3: 'Notbad', 2: 'Fail', 1: 'Fail', 0: 'Fail'}
    sDict = {5: 'Perfect', 4: 'Good', 3: 'Good', 2: 'Notbad', 1: 'Fail', 0: 'Fail'}
    fDict = {2: 'Perfect', 1: 'Notbad', 0: 'Fail'}

    # print('본 프로그램은 아이언에 적용됩니다.')
    # print('---------- 준비 자세 ----------')
    # print('결과 : ', rDict[ready_success_len])
    # print('아쉬운 자세 : ', ready_feedback)
    # print(ready_success_len)
    # print('---------- 스윙 자세 ----------')
    # print('결과 : ', sDict[swing_success_len])
    # print('아쉬운 자세 : ', swing_feedback)
    # print(swing_success_len)
    # print('---------- 피니시 자세 ----------')
    # print('결과 : ', fDict[finish_success_len])
    # print('아쉬운 자세 : ', finish_feedback)
    # print(finish_success_len)

    result = {'ready_result': rDict[ready_success_len], 'ready_feedback': ready_feedback,
              'swing_result': sDict[swing_success_len], 'swing_feedback': swing_feedback,
              'finish_result': fDict[finish_success_len], 'finish_feedback': finish_feedback
              , 'isErrorReady': isErrorReady, 'isErrorSwing' : isErrorSwing, 'isErrorFinish': isErrorFinish
                , 'length1': length1, 'length2': length2, 'length3': length3
              }
    resultText = {"resultText":result}
    res = requests.post('http://localhost:5000/api/feedbackdata', json=resultText)
