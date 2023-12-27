# _*_ coding : utf-8 _*_
# @Time : 2023/9/17 9:58
# @Author : Origami
# @File : voice
# @Project : gptplat
import asrt_sdk
from common.util import read_yaml


stream_asr_text = ""
stream_buffer_text = ""


def handle_voice(file_path):
    text_res = wav2hanzi(file_path)
    return text_res


# 对音频文件做预处理
def pre_process_voice(voice_file):
    return voice_file


def transfer_file(voice_file):
    return voice_file


def wav2hanzi(file_path):
    SUB_PATH = ''
    speech_recognizer = asrt_sdk.get_speech_recognizer(
        read_yaml('asrt.host'), str(read_yaml('asrt.port')), read_yaml('asrt.protocol'))
    speech_recognizer.sub_path = SUB_PATH
    print("file_path: " + file_path)
    result = speech_recognizer.recognite_file(file_path)
    for index in range(0, len(result)):
        item = result[index]
        # print("第", index, "段:", item.result)
    wave_data = asrt_sdk.read_wav_datas(file_path)
    result = speech_recognizer.recognite_speech(wave_data.str_data,
                                                wave_data.sample_rate,
                                                wave_data.channels,
                                                wave_data.byte_width)
    result = speech_recognizer.recognite_language(result.result)
    text_res = result.result
    return text_res
