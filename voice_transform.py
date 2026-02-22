import sys
import whisper
import speech_recognition as sr
import wave
import io
import numpy as np

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

if __name__ == "__main__":
    wav_file = sys.argv[1]
    print(wav_to_string(wav_file))