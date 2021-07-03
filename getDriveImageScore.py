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
#가장 오차가 심한 점수를 알아내기 위한 최대 오차 확인용 변수
maxDiff_ready = maxDiff_swing = maxDiff_finish = 0
isErrorSwing = isErrorReady = isErrorFinish = 0 #true or false

def Angle(P1, P2, P3):
    a = math.sqrt(math.pow(P1.x - P2.x, 2) + math.pow(P1.y - P2.y, 2))
    b = math.sqrt(math.pow(P2.x - P3.x, 2) + math.pow(P2.y - P3.y, 2))
    c = math.sqrt(math.pow(P1.x - P3.x, 2) + math.pow(P1.y - P3.y, 2))
    angle = math.acos((a * a + b * b - c * c) / (2 * a * b))
    return (angle * 180) / PI

def Angle2(P11, P12, P2, P3):
    P1 = Point()
    P1.x = (P11.x + P12.x) / 2
    P1.y = (P11.y + P12.y) / 2
    a = math.sqrt(math.pow(P1.x - P2.x, 2) + math.pow(P1.y - P2.y, 2))
    b = math.sqrt(math.pow(P2.x - P3.x, 2) + math.pow(P2.y - P3.y, 2))
    c = math.sqrt(math.pow(P1.x - P3.x, 2) + math.pow(P1.y - P3.y, 2))
    angle = math.acos((a * a + b * b - c * c) / (2 * a * b))
    return (angle * 180) / PI

# 인수 설명
# diff : 기준 각도와의 절댓값 차이
# num : 각도 idx
# skeleton : 각 각도에 대한 한글명
def eval_ready(diff, num, skeleton):
    global ready_success_len, maxDiff_ready, ready_feedback
    if num == 1:
        if diff < 10: ready_success_len += 1
        elif diff > maxDiff_ready :
            maxDiff_ready = diff
            ready_feedback = skeleton
    if num == 2:
        if diff < 10: ready_success_len += 1
        elif diff > maxDiff_ready :
            maxDiff_ready = diff
            ready_feedback = skeleton
    if num == 3:
        if diff < 10: ready_success_len += 1
        elif diff > maxDiff_ready :
            maxDiff_ready = diff
            ready_feedback = skeleton
    if num == 4:
        if diff < 10: ready_success_len += 1
        elif diff > maxDiff_ready :
            maxDiff_ready = diff
            ready_feedback = skeleton
    if num == 5:
        if diff < 10: ready_success_len += 1
        elif diff > maxDiff_ready :
            maxDiff_ready = diff
            ready_feedback = skeleton
    if num == 6:
        if diff < 10: ready_success_len += 1
        elif diff > maxDiff_ready :
            maxDiff_ready = diff
            ready_feedback = skeleton

# 인수 설명
# diff : 기준 각도와의 절댓값 차이
# num : 각도 idx
# skeleton : 각 각도에 대한 한글명
def eval_swing(diff, num, skeleton):
    global swing_success_len, maxDiff_swing, swing_feedback
    if num == 1:
        if diff < 10: swing_success_len += 1
        elif diff >= maxDiff_swing :
            maxDiff_swing = diff
            swing_feedback = skeleton
    if num == 2:
        if diff < 10: swing_success_len += 1
        elif diff >= maxDiff_swing :
            maxDiff_swing = diff
            swing_feedback = skeleton
    if num == 3:
        if diff < 10: swing_success_len += 1
        elif diff >= maxDiff_swing :
            maxDiff_swing = diff
            swing_feedback = skeleton
    if num == 4:
        if diff < 10: swing_success_len += 1
        elif diff >= maxDiff_swing :
            maxDiff_swing = diff
            swing_feedback = skeleton
    if num == 5:
        if diff < 10: swing_success_len += 1
        elif diff >= maxDiff_swing :
            maxDiff_swing = diff
            swing_feedback = skeleton

# 인수 설명
# diff : 기준 각도와의 절댓값 차이
# num : 각도 idx
# skeleton : 각 각도에 대한 한글명
def eval_finish(diff, num, skeleton):
    global finish_success_len, maxDiff_finish, finish_feedback
    if num == 1:
        if diff < 10: finish_success_len += 1
        elif diff >= maxDiff_finish :
            maxDiff_finish = diff
            finish_feedback = skeleton
    if num == 2:
        if diff < 10: finish_success_len += 1
        elif diff >= maxDiff_finish :
            maxDiff_finish = diff
            finish_feedback = skeleton

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
PI = 3.1415926535

#프로 자세기반 기준 점수.
BASESCORE_READY = [72.53, 69.72, 72.47, 85.34, 172.4, 173.95]
BASESCORE_SWING = [156.0, 170.63, 169.8, 131.81, 138.6]
BASESCORE_FINISH = [144.31, 162.99]

DATA_DIR = os.getcwd() + "/images"
IMAGE_FILES = os.listdir(DATA_DIR)
# print(IMAGE_FILES)

with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=2,
        min_detection_confidence=0.5) as pose:
    for idx, file in enumerate(IMAGE_FILES):
        if (file == '.DS_Store'): continue
        file = DATA_DIR + '/' + file
        image = cv2.imread(file)
        image_height, image_width, _ = image.shape

        # Convert the BGR image to RGB before processing.
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.pose_landmarks:
            if(idx == 0) : isErrorReady = 1
            elif(idx == 1): isErrorSwing = 1
            elif(idx == 2): isErrorFinish = 1
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
        cv2.imwrite('images_result/annotated_image' + str(idx) + '.png', annotated_image)
        if (file.find('first') != -1):
            one = Angle2(ll[23], ll[24], ll[27], ll[28])
            two = Angle2(ll[23], ll[24], ll[27], ll[28])
            three = Angle(ll[12], ll[11], ll[13])
            four = Angle(ll[11], ll[12], ll[14])
            five = Angle(ll[11], ll[13], ll[15])
            six = Angle(ll[12], ll[14], ll[16])

            eval_ready(abs(round(one, 2) - BASESCORE_READY[0]), 0, "왼발")
            eval_ready(abs(round(two, 2) - BASESCORE_READY[1]), 1, "오른발")
            eval_ready(abs(round(three, 2) - BASESCORE_READY[2]), 2, "왼쪽어깨")
            eval_ready(abs(round(four, 2) - BASESCORE_READY[3]), 3, "오른쪽어깨")
            eval_ready(abs(round(five, 2) - BASESCORE_READY[4]), 4, "왼쪽팔꿈치")
            eval_ready(abs(round(six, 2) - BASESCORE_READY[5]), 5, "오른쪽팔꿈치")

        if (file.find('second') != -1):
            ones = Angle(ll[12], ll[24], ll[26])
            twos = Angle(ll[24], ll[26], ll[28])
            threes = Angle(ll[23], ll[25], ll[27])
            fours = Angle(ll[11], ll[12], ll[14])
            fives = Angle(ll[12], ll[14], ll[16])

            eval_swing(abs(round(ones, 2) - BASESCORE_SWING[0]), 0, "오른쪽 허리")
            eval_swing(abs(round(twos, 2) - BASESCORE_SWING[1]), 1, "오른쪽 무릎")
            eval_swing(abs(round(threes, 2) - BASESCORE_SWING[2]), 2, "왼쪽 무릎")
            eval_swing(abs(round(fours, 2) - BASESCORE_SWING[3]), 3, "오른쪽 어깨")
            eval_swing(abs(round(fives, 2) - BASESCORE_SWING[4]), 4, "오른쪽 팔꿈치")

        if (file.find('third') != -1):
            onef = Angle(ll[24], ll[26], ll[28])
            twof = Angle(ll[12], ll[24], ll[26])
            eval_finish(abs(round(onef, 2) - BASESCORE_FINISH[0]), 0, "오른쪽 무릎")
            eval_finish(abs(round(twof, 2) - BASESCORE_FINISH[1]), 1, "오른쪽 허리")

    rDict = {6:'Excellent', 5: 'Excellent', 4: 'Perfect', 3: 'Perfect', 2: 'Good', 1: 'Good', 0: 'Fail'}
    sDict = {5: 'Excellent', 4: 'Excellent', 3: 'Perfect', 2: 'Good', 1: 'Good', 0: 'Fail'}
    fDict = {2: 'Excellent', 1: 'Perfect', 0: 'Good'}

    # print('본 프로그램은 아이언, 드라이브 모두에 적용됩니다.')
    # print('---------- 준비 자세 ----------')
    # print('결과 : ',rDict[ready_success_len])
    # print('아쉬운 자세 : ', ready_feedback)
    # print('---------- 스윙 자세 ----------')
    # print('결과 : ', sDict[swing_success_len])
    # print('아쉬운 자세 : ', swing_feedback)
    # print('---------- 피니시 자세 ----------')
    # print('결과 : ', fDict[finish_success_len])
    # print('아쉬운 자세 : ', finish_feedback)

    result = {'ready_result': rDict[ready_success_len], 'ready_feedback': ready_feedback,
              'swing_result': sDict[swing_success_len], 'swing_feedback': swing_feedback,
              'finish_result': fDict[finish_success_len], 'finish_feedback': finish_feedback
              , 'isErrorReady': isErrorReady, 'isErrorSwing' : isErrorSwing, 'isErrorFinish': isErrorFinish
              }
    # resultText = json.dumps(result)
    resultText = {"resultText":result}
    res = requests.post('http://localhost:5000/api/feedbackdata', json=resultText)
    # print(resultText)
