import os
import cv2
import time
from capture import capture
from detect_face_travelcode import send_image
from speak import espeak_chinese
from motor import move
from thermo import MLX90614
from weather import report_weather
thermo_detect = MLX90614()
from human_detect import detect_human



#report_weather()
while (1):

    detect_human()
    espeak_chinese("您好！欢迎使用智慧疫情防控系统，请出示大数据行程卡！")
    time.sleep(2)
    image = capture()
    travel_code_condition = send_image(image, 2)
    print("travel code")
    print(travel_code_condition)
    while (travel_code_condition == -1):
        espeak_chinese("未检测到大数据行程卡，请虫新出示大数据行程卡！")
        time.sleep(2)
        image = capture()
        travel_code_condition = send_image(image, 2)
    if (travel_code_condition == 1):
        espeak_chinese("大数据行程卡黄码，行程码异常，禁止入内！")
        continue
    elif (travel_code_condition == 2):
        espeak_chinese("大数据行程卡红码，行程码异常，禁止入内！")
        continue
    elif (travel_code_condition == 0):
        espeak_chinese("大数据行程码绿码，准备检测体温！")
        time.sleep(1)
        espeak_chinese("准备识别人脸，请靠近摄像头！")
        image = capture()
        face_detected = send_image(image,1)
        while (face_detected == -1):
            espeak_chinese("未检测到人脸，请靠近摄像头！")
            time.sleep(2)
            espeak_chinese("准备识别人脸！")
            image = capture()
            face_detected = send_image(image,1)
            
        if(face_detected<0.3):
            espeak_chinese("请您往左站，准备检测体温！")
            print(face_detected)
            #move(face_detected)
        elif(face_detected>0.7):
            espeak_chinese("请您往右站，准备检测体温！")
                
        temperature = str(round(thermo_detect.get_obj_temp(),1))
        temp_int = str(int(temperature.split('.')[0]))
        temp_decimal = temperature.split('.')[1]
        temp = temp_int +"点"+temp_decimal
        if(float(temperature) > 37):
            espeak_chinese("您的体温是{}度，体温异常，禁止进入！".format(temp))
            continue
        else:
            espeak_chinese("您的体温是{}度，正常，请进！！".format(temp))
            move(1)
            move(0)
