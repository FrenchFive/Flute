import subprocess
import os
import m2a

script_path = os.path.dirname(os.path.abspath(__file__))

soundfont_path = os.path.join(script_path, "soundfont", "flute4.sf2")
midi_path = os.path.join(script_path, "outputs", "audio_basic_pitch.mid")
wav_path = os.path.join(script_path, "outputs", "final.wav")

subprocess.run([
    "fluidsynth",
    "-ni",
    "-F", wav_path,
    "-r", "44100",
    soundfont_path,
    midi_path
])

m2a.convert_midi_to_audio(midi_path, soundfont_path, wav_path)