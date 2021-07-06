# MediaPipePose
import cv2
import mediapipe as mp
import math
import os
import requests

class Point:
    x = 0
    y = 0

# 각도가 성공 기준에 들어갈 경우에는, len 값을 올려주어 이 len 값을 기준으로 score를 매길 예정.
ready_success_len = swing_success_len = finish_success_len = 0
# 피드백 문구로 넣을 예정.
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

#피타코라스 활용 거리 return 함수
def Distance(P1,P2):
    distance = math.sqrt(pow(P1.x-P2.x, 2)+pow(P1.y-P2.y, 2))
    return distance

# 각 각도에 대하여 ox 판별하는 함수. (eval_ready, eval_swing, eval_finish)
# rs : 해당 각도
# skeleton : 각 각도에 대한 한글명
# minNum, maxNum : 스켈레톤에 최솟값, 최댓값
def eval_ready(rs, skeleton, minNum, maxNum):
    global ready_success_len, ready_feedback
    if skeleton == "keyCheck":
        if rs < 150:
            ready_feedback = ""
        return
    if minNum < rs < maxNum:
        ready_success_len += 1
    else:
        if ready_feedback == "":
            ready_feedback = skeleton
        else:
            ready_feedback = ready_feedback + ", " + skeleton

def eval_swing(rs, skeleton, minNum, maxNum):
    global swing_success_len, swing_feedback
    if skeleton == "keyCheck":
        if rs < 150:
            swing_feedback = ""
        return
    if minNum < rs < maxNum:
        swing_success_len += 1
    else:
        if swing_feedback == "":
            swing_feedback = skeleton
        else:
            swing_feedback = swing_feedback + ", " + skeleton

def eval_finish(rs, skeleton, minNum, maxNum):
    global finish_success_len, finish_feedback
    if skeleton == "keyCheck":
        if rs < 150:
            finish_feedback = ""
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
PUTTER_READY = [84.54, 80.82, 86.69, 89.11]
PUTTER_SWING = [84.75, 83.92, 89.84, 86.19]
PUTTER_FINISH = [80.02, 86.35, 85.74, 90.31]

DATA_DIR = os.getcwd() + "/images"
IMAGE_FILES = os.listdir(DATA_DIR)
IMAGE_FILES.sort()
# print(IMAGE_FILES)

with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=2,
        min_detection_confidence=0.5) as pose:
    for idx, file in enumerate(IMAGE_FILES):
        if (file.find('putter') == -1): continue
        else: num += 1
        file = DATA_DIR + '/' + file
        image = cv2.imread(file)
        image_height, image_width, _ = image.shape
        # Convert the BGR image to RGB before processing.
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.pose_landmarks:
            if (file.find('first') != -1): isErrorReady = 1
            elif (file.find('second') != -1): isErrorSwing = 1
            elif (file.find('third') != -1): isErrorFinish = 1
            continue
        annotated_image = image.copy()
        ll = []

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
            one = Angle(ll[11], ll[12], ll[14])
            two = Angle(ll[12], ll[11], ll[13])
            three = Angle(ll[26], ll[28], ll[27])
            four = Angle(ll[25], ll[27], ll[28])
            length1 = Distance(ll[0], ll[27])
            eval_ready(round(one, 2), "오른쪽 어깨", 60, 92)
            eval_ready(round(two, 2), "왼쪽 어깨", 50, 93)
            eval_ready(round(three, 2), "오른쪽 발", 61, 89)
            eval_ready(round(four, 2), "왼쪽 발", 65, 89)
            eval_ready(round(length1, 2), "keyCheck", 0, 0)

        if (file.find('second') != -1):
            ones = Angle(ll[11], ll[12], ll[14])
            twos = Angle(ll[12], ll[11], ll[13])
            threes = Angle(ll[26], ll[28], ll[27])
            fours = Angle(ll[25], ll[27], ll[28])
            length2 = Distance(ll[0], ll[27])
            eval_swing(round(one, 2), "오른쪽 어깨", 60, 92)
            eval_swing(round(two, 2), "왼쪽 어깨", 50, 93)
            eval_swing(round(three, 2), "오른쪽 발", 61, 89)
            eval_swing(round(four, 2), "왼쪽 발", 65, 89)
            eval_swing(round(length2, 2), "keyCheck", 0, 0)


        if (file.find('third') != -1):
            onef = Angle(ll[11], ll[12], ll[14])
            twof = Angle(ll[12], ll[11], ll[13])
            threef = Angle(ll[26], ll[28], ll[27])
            fourf = Angle(ll[25], ll[27], ll[28])
            length3 = Distance(ll[0], ll[27])
            eval_finish(round(one, 2), "오른쪽 어깨", 60, 92)
            eval_finish(round(two, 2), "왼쪽 어깨", 50, 93)
            eval_finish(round(three, 2), "오른쪽 발", 61, 89)
            eval_finish(round(four, 2), "왼쪽 발", 65, 89)
            eval_finish(round(length3, 2), "keyCheck", 0, 0)

    dict = {4: 'Perfect', 3: 'Good', 2: 'Notbad', 1: 'Fail', 0: 'Fail'}

    print('본 프로그램은 퍼터에 적용됩니다.')
    print('---------- 준비 자세 ----------')
    print('결과 : ', dict[ready_success_len])
    print('아쉬운 자세 : ', ready_feedback)
    print(ready_success_len)
    print('---------- 스윙 자세 ----------')
    print('결과 : ', dict[swing_success_len])
    print('아쉬운 자세 : ', swing_feedback)
    print(swing_success_len)
    print('---------- 피니시 자세 ----------')
    print('결과 : ', dict[finish_success_len])
    print('아쉬운 자세 : ', finish_feedback)
    print(finish_success_len)

    result = {'ready_result': dict[ready_success_len], 'ready_feedback': ready_feedback,
              'swing_result': dict[swing_success_len], 'swing_feedback': swing_feedback,
              'finish_result': dict[finish_success_len], 'finish_feedback': finish_feedback,
             'isErrorReady': isErrorReady, 'isErrorSwing': isErrorSwing, 'isErrorFinish': isErrorFinish
    }
    resultText = {"resultText": result}
    res = requests.post('http://localhost:5000/api/feedbackdata', json=resultText)