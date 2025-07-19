from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
import os

script_path = os.path.dirname(os.path.abspath(__file__))
audio_path  = os.path.join(script_path, "audio.mp3")

predict_and_save(
    [audio_path],             # 1) list of input files
    "outputs",                # 2) output directory
    True,                     # 3) save MIDI
    False,                    # 4) sonify MIDI (WAV) — off
    False,                    # 5) save raw model outputs — off
    False,                    # 6) save notes CSV — off
    ICASSP_2022_MODEL_PATH    # 7) model path
)
