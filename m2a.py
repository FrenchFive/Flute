import os
from midi2audio import FluidSynth

script_path = os.path.dirname(os.path.abspath(__file__))

midi_path = os.path.join(script_path, "outputs", "audio_basic_pitch.mid")
soundfont_path = os.path.join(script_path, "soundfont", "flute4.sf2")
output_wav = os.path.join(script_path, "final.wav")
output_mp3 = os.path.join(script_path, "final.mp3")

# Initialize FluidSynth with your custom SoundFont
fs = FluidSynth(sound_font=soundfont_path)

# Convert MIDI to WAV
fs.midi_to_audio(midi_path, output_wav)

# Convert WAV to MP3 (optional)
os.system(f'ffmpeg -y -i "{output_wav}" "{output_mp3}"')
os.remove(output_wav)
