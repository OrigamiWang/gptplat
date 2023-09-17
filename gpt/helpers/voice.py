# _*_ coding : utf-8 _*_
# @Time : 2023/9/17 9:58
# @Author : Origami
# @File : voice
# @Project : gptplat
import asrt_sdk
import os
from common.util import read_yaml

# from app import root_path

stream_asr_text = ""
stream_buffer_text = ""


def handle_voice(voice_file):
    # voice_file = pre_process_voice(voice_file)
    # wave_data = transfer_file(voice_file)
    wave_data = ''
    text_res = wav2hanzi(wave_data)
    return text_res


# 对音频文件做预处理
def pre_process_voice(voice_file):
    return voice_file


def transfer_file(voice_file):
    return voice_file


def wav2hanzi(wave_data):
    SUB_PATH = ''
    speech_recognizer = asrt_sdk.get_speech_recognizer(
        read_yaml('asrt.host'), str(read_yaml('asrt.port')), read_yaml('asrt.protocol'))
    speech_recognizer.sub_path = SUB_PATH
    FILENAME = 'test1.wav'
    result = speech_recognizer.recognite_file(FILENAME)
    for index in range(0, len(result)):
        item = result[index]
        # print("第", index, "段:", item.result)
    wave_data = asrt_sdk.read_wav_datas(FILENAME)
    result = speech_recognizer.recognite_speech(wave_data.str_data,
                                                wave_data.sample_rate,
                                                wave_data.channels,
                                                wave_data.byte_width)
    result = speech_recognizer.recognite_language(result.result)
    text_res = result.result
    return text_res
