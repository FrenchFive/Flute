from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
import subprocess
import os
import mido


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

def clean_midi(midi_path):
    mid = mido.MidiFile(midi_path)
    for track in mid.tracks:
        for msg in track:
            #remove if velocity is below 10
            if msg.type == 'note_on' and msg.velocity < 5:
                msg.velocity = 0
            #remove if note is too low pitch
            if msg.type == 'note_on' and msg.note < 10:
                msg.velocity = 0
    mid.save(midi_path)


def convert_midi_to_audio(midi_path, soundfont_path, wav_path):
    subprocess.run([
        "fluidsynth",
        "-ni",
        "-F", wav_path,
        "-r", "44100",
        "-g", "4.0",
        soundfont_path,
        midi_path
    ])

def convert_wav_to_mp3(wav_path, mp3_path):
    subprocess.run([
        "ffmpeg",
        "-i", wav_path,
        "-filter:a", "loudnorm",
        "-codec:a", "libmp3lame",
        "-qscale:a", "2",
        mp3_path
    ])

midi_path = os.path.join(script_path, "outputs", "audio_basic_pitch.mid")
wav_path = os.path.join(script_path, "final.wav")

clean_midi(midi_path)

convert_midi_to_audio(
    midi_path,
    os.path.join(script_path, "soundfont", "Pan_Flute.sf2"),
    wav_path
)

mp3_path = os.path.join(script_path, "final.mp3")
os.remove(midi_path)
os.remove(mp3_path)

convert_wav_to_mp3(
    wav_path,
    mp3_path
)
os.remove(wav_path)
