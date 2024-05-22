# 完成
from aip import AipSpeech
from os import remove
from os.path import isfile
from wave import open as wopen
import pyaudio
import data

client = AipSpeech(data.VOICE_APP_ID,data.VOICE_API_Key,data.VOICE_Secret_Key)
re = pyaudio.PyAudio()

def exit():
    """退出"""
    global re
    if isfile('temp.wav'):
        remove('temp.wav')
        # 删除临时文件
    re.terminate()

def record(time=5,filename='temp.wav'):
    """录制声音"""
    stream = re.open(format=data.BITDEPTH,channels=data.CHANNELS,rate=data.SAMPLERATE,input=True,frames_per_buffer=data.BUFSIZE)
    redata = []
    for i in range(0,int(time*data.SAMPLERATE*data.CHANNELS/data.BUFSIZE)):
        redata.append(stream.read(data.BUFSIZE))
    stream.stop_stream()
    stream.close()
    file = wopen(filename,'wb')
    file.setframerate(data.SAMPLERATE)
    file.setnchannels(data.CHANNELS)
    file.setsampwidth(2)
    file.writeframes(b''.join(redata))
    file.close()

def recognize_voice():
    """语音识别"""
    #{'corpus_no': '7166479184675531777', 'err_msg': 'success.', 'err_no': 0,'result': ['循环结构是一种十分重要的程序控制结构，其特点是在。'], 'sn': '972307134351668575960'}
    f = open('temp.wav','rb')
    file = f.read()
    f.close()
    remove('temp.wav')
    res = client.asr(file,'wav',data.SAMPLERATE,{'dev_pid':1537,})
#     print(res)
    if res['err_no'] != 0:
        return False
    return res['result'][0]

if __name__ == '__main__':
    ans = data.input('请说话',data.SAY)
    print(ans)
#     print('请说话')
#     record()
#     print(recognize_voice())