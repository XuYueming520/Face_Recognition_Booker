# 完成
from aip import AipFace
from os import remove
from os.path import isfile
from base64 import b64encode
import cv2
import data
import time

client = AipFace(data.APP_ID,data.API_Key,data.Secret_Key)
facer = cv2.CascadeClassifier(cv2.data.haarcascades+r'\haarcascade_frontalface_default.xml')

def exit():
    """退出"""
    if isfile('temp.jpg'):
        remove('temp.jpg')
        # 删除临时文件
    cv2.destroyAllWindows()  # 关闭所有窗口
    cap = cv2.VideoCapture(0)
    cap.release()  # 释放摄像头

def get_face():
    """捕获人脸"""
    cap = cv2.VideoCapture(0)  # 摄像头
    face_time = None
    
    while 1:
        res,frame = cap.read()  # 读取摄像头
        cap_screen = frame
        have_face = 0  # 判断摄像头中是否识别到人脸
        
        faces = facer.detectMultiScale(frame,scaleFactor=1.3,minNeighbors=5,minSize=(64,64))  # 所有人脸
        for (x1,y1,w1,h1) in faces:  # 遍历所有人脸
            have_face += 1  # 有脸
            face = frame[y1:y1+h1,x1:x1+w1]
            cv2.imshow('face',face)
            frame = cv2.rectangle(frame,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)  # 画框s
        
#         cv2.putText(frame, 'Please press "Q" to continue', (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
        if have_face == 1:
            if face_time is not None:
                if time.time() - face_time >= 3:
                    break
#                 print(int(3-(time.time() - face_time)))
                cv2.putText(frame, str(int(3-(time.time() - face_time))+1)+'s', (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
            else:
                face_time = time.time()
        else:
            face_time = None
        cv2.imshow('frame',frame)
        cv2.waitKey(1)
#         k = cv2.waitKey(1) & 0xFF  # 按下的按键
#         if k == ord("q") and have_face:  # 用户退出
#             break
    
    cap.release()  # 释放摄像头
    cv2.destroyAllWindows()  #关闭所有窗口
    
    return face, cap_screen  # 返回识别到的灰度人脸和摄像头捕捉的画面

def recognize_face(face):
    """识别人脸"""
    try:
        cv2.imwrite('temp.jpg',face)
        f = open('temp.jpg','rb')
        d = f.read()
        f.close()
        remove('temp.jpg')
        # 重新读取画面，转换成百度AIP接口的类型
        
        my_data = b64encode(d)
        image = my_data.decode()
        # 转换类型
        
        result = client.search(image,'BASE64',data.Group_name)
        # 调用AIP

        # print(result)
        if result["error_msg"] in "SUCCESS":  # 成功
            max_score = 0
            user_id = 0
            for dic in result["result"]["user_list"]:
                if dic["score"] > max_score:
                    max_score = dic["score"]
                    user_id = dic["user_id"]
            if max_score < 80:
                return False
            return user_id
        return False
    except:
        return False

def add_user(face,name):
    """添加用户"""
    cv2.imwrite('temp.jpg',face)
    f = open('temp.jpg','rb')
    d = f.read()
    f.close()
    remove('temp.jpg')
    # 重新读取画面，转换成百度AIP接口的类型
    
    my_data = b64encode(d)
    image = my_data.decode()
    # 转换类型
    
    client.addUser(image,'BASE64',data.Group_name,name)

if __name__ == '__main__':
    print('开始!')
    userf, cap_screen = get_face()
    res = recognize_face(userf)
    print(res)
    print('结束!')
    exit()