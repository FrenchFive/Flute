from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
import subprocess
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


def convert_midi_to_audio(midi_path, soundfont_path, wav_path):
    subprocess.run([
        "fluidsynth",
        "-ni",
        "-F", wav_path,
        "-r", "44100",
        soundfont_path,
        midi_path
    ])


convert_midi_to_audio(
    os.path.join(script_path, "outputs", "audio_basic_pitch.mid"),
    os.path.join(script_path, "soundfont", "flute4.sf2"),
    os.path.join(script_path, "final.wav")
)
