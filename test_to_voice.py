import pyttsx3

def text_to_speech(text, rate=150, volume=1.0):
    # 初始化语音引擎
    engine = pyttsx3.init()
    # 设置语速
    engine.setProperty('rate', rate)
    # 设置音量
    engine.setProperty('volume', volume)
    # 朗读文字
    engine.say(text)
    # 等待朗读完成
    engine.runAndWait()

if __name__ == "__main__":
    while True:
        # 输入要朗读的文字
        text = input("请输入要朗读的文字（输入'q'退出）：")
        if text.lower() == 'q':
            break
        try:
            # 输入语速
            rate = int(input("请输入语速（范围 0-200，默认 150）："))
        except ValueError:
            rate = 150
        try:
            # 输入音量
            volume = float(input("请输入音量（范围 0.0-1.0，默认 1.0）："))
        except ValueError:
            volume = 1.0
        # 调用函数进行朗读
        text_to_speech(text, rate, volume)