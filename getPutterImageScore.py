# MediaPipePose

import cv2
import mediapipe as mp
import math
import os
import json


class Point:
    x = 0
    y = 0


# 각도가 성공 기준에 들어갈 경우에는, len 값을 올려주어 이 len 값을 기준으로 score를 매길 예정.
ready_success_len = swing_success_len = finish_success_len = 0
# 피드백 문구로 넣을 예정.
ready_feedback = swing_feedback = finish_feedback = ""
# 가장 오차가 심한 점수를 알아내기 위한 최대 오차 확인용 변수
maxDiff_ready = maxDiff_swing = maxDiff_finish = 0


def Angle(P1, P2, P3):
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
        if diff < 10:
            ready_success_len += 1
        elif diff > maxDiff_ready:
            maxDiff_ready = diff
            ready_feedback = skeleton
    if num == 2:
        if diff < 10:
            ready_success_len += 1
        elif diff > maxDiff_ready:
            maxDiff_ready = diff
            ready_feedback = skeleton
    if num == 3:
        if diff < 10:
            ready_success_len += 1
        elif diff > maxDiff_ready:
            maxDiff_ready = diff
            ready_feedback = skeleton
    if num == 4:
        if diff < 10:
            ready_success_len += 1
        elif diff > maxDiff_ready:
            maxDiff_ready = diff
            ready_feedback = skeleton


# 인수 설명
# diff : 기준 각도와의 절댓값 차이
# num : 각도 idx
# skeleton : 각 각도에 대한 한글명
def eval_swing(diff, num, skeleton):
    global swing_success_len, maxDiff_swing, swing_feedback
    if num == 1:
        if diff < 10:
            swing_success_len += 1
        elif diff >= maxDiff_swing:
            maxDiff_swing = diff
            swing_feedback = skeleton
    if num == 2:
        if diff < 10:
            swing_success_len += 1
        elif diff >= maxDiff_swing:
            maxDiff_swing = diff
            swing_feedback = skeleton
    if num == 3:
        if diff < 10:
            swing_success_len += 1
        elif diff >= maxDiff_swing:
            maxDiff_swing = diff
            swing_feedback = skeleton
    if num == 4:
        if diff < 10:
            swing_success_len += 1
        elif diff >= maxDiff_swing:
            maxDiff_swing = diff
            swing_feedback = skeleton


# 인수 설명
# diff : 기준 각도와의 절댓값 차이
# num : 각도 idx
# skeleton : 각 각도에 대한 한글명
def eval_finish(diff, num, skeleton):
    global finish_success_len, maxDiff_finish, finish_feedback
    if num == 1:
        if diff < 10:
            finish_success_len += 1
        elif diff >= maxDiff_finish:
            maxDiff_finish = diff
            finish_feedback = skeleton
    if num == 2:
        if diff < 10:
            finish_success_len += 1
        elif diff >= maxDiff_finish:
            maxDiff_finish = diff
            finish_feedback = skeleton
    if num == 3:
        if diff < 10:
            finish_success_len += 1
        elif diff >= maxDiff_finish:
            maxDiff_finish = diff
            finish_feedback = skeleton
    if num == 4:
        if diff < 10:
            finish_success_len += 1
        elif diff >= maxDiff_finish:
            maxDiff_finish = diff
            finish_feedback = skeleton


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
PI = 3.1415926535
PUTTER_READY = [84.54, 80.82, 86.69, 89.11]
PUTTER_SWING = [84.75, 83.92, 89.84, 86.19]
PUTTER_FINISH = [80.02, 86.35, 85.74, 90.31]
DATA_DIR = os.getcwd() + "/web"
# For static images:
IMAGE_FILES = os.listdir(DATA_DIR)
print(IMAGE_FILES)

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
            continue

        annotated_image = image.copy()
        ll = []

        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = image.shape
            # print(id)
            p = Point()
            cx, cy = int(lm.x * w), int(lm.y * h)
            p.x = cx
            p.y = cy
            ll.append(p)
            cv2.putText(annotated_image, str(id), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)

        # Draw pose landmarks on the image.
        mp_drawing.draw_landmarks(
            annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imwrite('web_result/annotated_image' + str(idx) + '.png', annotated_image)
        if (file.find('ready') != -1):
            one = Angle(ll[11], ll[12], ll[14])
            two = Angle(ll[12], ll[11], ll[13])
            three = Angle(ll[26], ll[28], ll[27])
            four = Angle(ll[25], ll[27], ll[28])

            eval_ready(abs(round(one, 2) - PUTTER_READY[0]), 0, "오른쪽 어깨")
            eval_ready(abs(round(two, 2) - PUTTER_READY[1]), 1, "왼쪽 어깨")
            eval_ready(abs(round(three, 2) - PUTTER_READY[2]), 2, "오른쪽 발")
            eval_ready(abs(round(four, 2) - PUTTER_READY[3]), 3, "왼쪽 발")

        if (file.find('swing') != -1):
            ones = Angle(ll[11], ll[12], ll[14])
            twos = Angle(ll[12], ll[11], ll[13])
            threes = Angle(ll[26], ll[28], ll[27])
            fours = Angle(ll[25], ll[27], ll[28])

            eval_swing(abs(round(one, 2) - PUTTER_SWING[0]), 0, "오른쪽 어깨")
            eval_swing(abs(round(two, 2) - PUTTER_SWING[1]), 1, "왼쪽 어깨")
            eval_swing(abs(round(three, 2) - PUTTER_SWING[2]), 2, "오른쪽 발")
            eval_swing(abs(round(four, 2) - PUTTER_SWING[3]), 3, "왼쪽 발")

        if (file.find('finish') != -1):
            onef = Angle(ll[11], ll[12], ll[14])
            twof = Angle(ll[12], ll[11], ll[13])
            threef = Angle(ll[26], ll[28], ll[27])
            fourf = Angle(ll[25], ll[27], ll[28])

            eval_finish(abs(round(onef, 2) - PUTTER_FINISH[0]), 0, "오른쪽 어깨")
            eval_finish(abs(round(twof, 2) - PUTTER_FINISH[1]), 1, "왼쪽 어깨")
            eval_finish(abs(round(threef, 2) - PUTTER_FINISH[2]), 2, "오른쪽 발")
            eval_finish(abs(round(fourf, 2) - PUTTER_FINISH[3]), 3, "왼쪽 발")
    print('본 프로그램은 퍼터에 적용됩니다.')

    dict = {4: 'Excellent', 3: 'Excellent', 2: 'Great', 1: 'Good', 0: 'Fail'}
    print('---------- 준비 자세 ----------')
    print('결과 : ', dict[ready_success_len])
    print('아쉬운 자세 : ', ready_feedback)
    print('---------- 스윙 자세 ----------')
    print('결과 : ', dict[swing_success_len])
    print('아쉬운 자세 : ', swing_feedback)
    print('---------- 피니시 자세 ----------')
    print('결과 : ', dict[finish_success_len])
    print('아쉬운 자세 : ', finish_feedback)

    result = {'ready_result': dict[ready_success_len], 'ready_feedback': ready_feedback,
              'swing_result': dict[swing_success_len], 'swing_feedback': swing_feedback,
              'finish_result': dict[finish_success_len], 'finish_feedback': finish_feedback
              }
    jsonResult = json.dumps(result)
    print(jsonResult)