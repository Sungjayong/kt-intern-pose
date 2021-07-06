#MediaPipePose
#프로들의 skeleton 각도 추출 및 표준편차 확인용.

import cv2
import mediapipe as mp
import math
import os
import numpy

class Point:
  x = 0
  y = 0

#3개의 point에 대하여 각도 추출 함수
def Angle(P1,P2,P3):
  a = math.sqrt(math.pow(P1.x - P2.x, 2) + math.pow(P1.y - P2.y, 2))
  b = math.sqrt(math.pow(P2.x - P3.x, 2) + math.pow(P2.y - P3.y, 2))
  c = math.sqrt(math.pow(P1.x - P3.x, 2) + math.pow(P1.y - P3.y, 2))
  angle = math.acos((a*a + b*b - c*c) / (2 * a * b))
  return (angle * 180) / PI

#p11, p12의 중심을 한 점으로 사용해서 각도 추출
def Angle2(P11,P12,P2,P3):
  P1 = Point()
  P1.x = (P11.x + P12.x) / 2
  P1.y = (P11.y + P12.y) / 2
  a = math.sqrt(math.pow(P1.x - P2.x, 2) + math.pow(P1.y - P2.y, 2))
  b = math.sqrt(math.pow(P2.x - P3.x, 2) + math.pow(P2.y - P3.y, 2))
  c = math.sqrt(math.pow(P1.x - P3.x, 2) + math.pow(P1.y - P3.y, 2))
  angle = math.acos((a*a + b*b - c*c) / (2 * a * b))
  return (angle * 180) / PI

#각도에 대하여 절사 평균값 return 함수
def getCutAvg (list):
  list.sort()
  #list.pop()
  #list.pop(0)
  return sum(list)/len(list)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
PI = 3.1415926535
DATA_DIR = os.getcwd() + '/data/drive'
# For static images:
IMAGE_FILES = os.listdir(DATA_DIR)
IMAGE_FILES.sort()
print(IMAGE_FILES)

#준비 자세 각도 배열
r_list_1 = []
r_list_2 = []
r_list_3 = []
r_list_4 = []
r_list_5 = []
r_list_6 = []

#스윙 자세 각도 배열
s_list_1 = []
s_list_2 = []
s_list_3 = []
s_list_4 = []
s_list_5 = []

#피니쉬 자세 각도 배열
f_list_1 = []
f_list_2 = []
with mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    min_detection_confidence=0.5) as pose:
  for idx, file in enumerate(IMAGE_FILES):
    if(file == '.DS_Store'): continue
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
      h,w,c = image.shape
      # print(id)
      p = Point()
      cx, cy = int(lm.x * w), int(lm.y * h)
      p.x = cx
      p.y = cy
      ll.append(p)
      cv2.putText(annotated_image, str(id), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,0), 1)

    # Draw pose landmarks on the image.
    mp_drawing.draw_landmarks(
      annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imwrite('result/annotated_image' + str(idx) + '.png', annotated_image)
    if(file.find('first') != -1):
      one = Angle2(ll[23], ll[24], ll[27], ll[28])
      two = Angle2(ll[23], ll[24], ll[28], ll[27])
      three = Angle(ll[12], ll[11], ll[13])
      four = Angle(ll[11], ll[12], ll[14])
      five = Angle(ll[11], ll[13], ll[15])
      six = Angle(ll[12], ll[14], ll[16])

      r_list_1.append(round(one, 2))
      r_list_2.append(round(two, 2))
      r_list_3.append(round(three, 2))
      r_list_4.append(round(four, 2))
      r_list_5.append(round(five, 2))
      r_list_6.append(round(six, 2))

    if (file.find('second') != -1):
      ones = Angle(ll[12], ll[24], ll[26])
      twos = Angle(ll[24], ll[26], ll[28])
      threes = Angle(ll[23], ll[25], ll[27])
      fours = Angle(ll[11], ll[12], ll[14])
      fives = Angle(ll[12], ll[14], ll[16])

      s_list_1.append(round(ones, 2))
      s_list_2.append(round(twos, 2))
      s_list_3.append(round(threes, 2))
      s_list_4.append(round(fours, 2))
      s_list_5.append(round(fives, 2))

    if (file.find('third') != -1):
      onef = Angle(ll[24], ll[26], ll[28])
      twof = Angle(ll[12], ll[24], ll[26])

      f_list_1.append(round(onef, 2))
      f_list_2.append(round(twof, 2))

    # Plot pose world landmarks.
    # mp_drawing.plot_landmarks(
    #     results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

  print("---------- 준비 자세 ----------")
  print('표본의 갯수: ', len(r_list_1))
  print('평균: ', round(getCutAvg(r_list_1),2))
  print(r_list_1)
  print('표준편차 ', numpy.std(r_list_1))
  print('평균: ', round(getCutAvg(r_list_2),2))
  print(r_list_2)
  print('표준편차 ', numpy.std(r_list_2))
  print('평균: ', round(getCutAvg(r_list_3),2))
  print(r_list_3)
  print('표준편차 ', numpy.std(r_list_3))
  print('평균: ', round(getCutAvg(r_list_4),2))
  print(r_list_4)
  print('표준편차 ', numpy.std(r_list_4))
  print('평균: ', round(getCutAvg(r_list_5),2))
  print(r_list_5)
  print('표준편차 ', numpy.std(r_list_5))
  print('평균: ', round(getCutAvg(r_list_6),2))
  print(r_list_6)
  print('표준편차 ', numpy.std(r_list_6))

  print("---------- 스윙 자세 ----------")
  print('표본의 갯수: ', len(s_list_1))
  print('평균: ', round(getCutAvg(s_list_1), 2))
  print(s_list_1)
  print('표준편차 ', numpy.std(s_list_1))
  print('평균: ', round(getCutAvg(s_list_2), 2))
  print(s_list_2)
  print('표준편차 ', numpy.std(s_list_2))
  print('평균: ', round(getCutAvg(s_list_3), 2))
  print(s_list_3)
  print('표준편차 ', numpy.std(s_list_3))
  print('평균: ', round(getCutAvg(s_list_4), 2))
  print(s_list_4)
  print('표준편차 ', numpy.std(s_list_4))
  print('평균: ', round(getCutAvg(s_list_5), 2))
  print(s_list_5)
  print('표준편차 ', numpy.std(s_list_5))

  print("---------- 피니시 자세 ----------")
  print('표본의 갯수: ', len(f_list_1))
  print('평균: ', round(getCutAvg(f_list_1), 2))
  print(f_list_1)
  print('표준편차 ', numpy.std(f_list_1))
  print('평균: ', round(getCutAvg(f_list_2), 2))
  print(f_list_2)
  print('표준편차 ', numpy.std(f_list_2))

# '키, 몸무게, 체형 => "분류 모델"'
# "필드모드 => 홈, 모드, 사진 찍는거"