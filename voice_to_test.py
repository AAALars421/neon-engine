import whisper
import speech_recognition as sr
import wave
import io
import numpy as np

def check_microphones():
    """检查并列出可用麦克风"""
    try:
        mic_list = sr.Microphone.list_microphone_names()
        print("\n【可用麦克风设备列表】")
        for i, name in enumerate(mic_list):
            print(f"  设备{i}：{name}")
        return len(mic_list) > 0
    except Exception as e:
        print(f"检测麦克风失败：{str(e)}")
        return False

def record_audio_to_memory(duration=10, mic_index=1):
    """录制音频到内存（不生成磁盘文件）"""
    recognizer = sr.Recognizer()

    try:
        mic = sr.Microphone(sample_rate=16000, device_index=mic_index)
        with mic as source:
            print(f"\n请开始说话（将录制{duration}秒）...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source, duration=duration)
            print("录音完成，正在处理音频数据...")

            # 保存为内存WAV
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(audio_data.get_raw_data())

            wav_buffer.seek(0)
            print("音频已存入内存（无磁盘文件）")
            return wav_buffer

    except OSError as e:
        print(f"麦克风访问错误：{str(e)}（可能被其他程序占用）")
        return None
    except Exception as e:
        print(f"录音出错：{str(e)}")
        return None


def wav_to_numpy(wav_buffer):
    """将内存WAV转为Whisper支持的numpy数组"""
    with wave.open(wav_buffer, 'rb') as wf:
        raw_data = wf.readframes(wf.getnframes())
    audio_np = np.frombuffer(raw_data, dtype=np.int16)
    audio_np = (audio_np / 32768.0).astype(np.float32)
    return audio_np

def whisper_recognize(audio_np):
    """Whisper识别（适配float32数据）"""
    try:
        print("\n正在加载Whisper模型...")
        model = whisper.load_model("base")
        print("模型加载完成，开始识别...")
        result = model.transcribe(
            audio_np,
            fp16=False
        )
        return result["text"]

    except Exception as e:
        return f"识别出错：{str(e)}"

def wav_to_string(wav_buffer):
    audio_np = wav_to_numpy(audio_buffer)
    if audio_np.size == 0:
        print("音频数据为空，程序终止")
        return

    # 4. 识别并输出
    result = whisper_recognize(audio_np)
    return result

def main():
    print("===== 【Whisper语音转文字工具】 =====")

    # 1. 检查麦克风
    if not check_microphones():
        print("无可用麦克风，程序终止")
        return

    # 2. 录制音频（用设备1）
    audio_buffer = record_audio_to_memory(duration=10, mic_index=1)
    if not audio_buffer:
        return

    # 3. 格式转换
    audio_np = wav_to_numpy(audio_buffer)
    if audio_np.size == 0:
        print("音频数据为空，程序终止")
        return

    # 4. 识别并输出
    result = whisper_recognize(audio_np)
    print("\n===== 【识别结果】 =====")
    print(result)

if __name__ == "__main__":
    main()