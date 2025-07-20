import unmix
import os
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
import subprocess
import mido

script_path = os.path.dirname(os.path.abspath(__file__))
audio_path  = os.path.join(script_path, "audio_nodrums.mp3")
midi_path = os.path.join(script_path, "outputs", "audio_nodrums_basic_pitch.mid")
wav_path = os.path.join(script_path, "final.wav")

if os.path.exists(midi_path):
    os.remove(midi_path)

unmix.combine_stems(
    output_path=audio_path,
    stem_dir=os.path.join(script_path, "separated"),
    vocals=True, drums=False, bass=False, other=True
)

octave = 0

predict_and_save(
    [audio_path],             # 1) list of input files
    "outputs",                # 2) output directory
    True,                     # 3) save MIDI
    False,                    # 4) sonify MIDI (WAV) — off
    False,                    # 5) save raw model outputs — off
    False,                    # 6) save notes CSV — off
    ICASSP_2022_MODEL_PATH    # 7) model path
)


def clean_midi(midi_path, octave=25):
    mid = mido.MidiFile(midi_path)
    for track in mid.tracks:
        for i, msg in enumerate(track):
            if msg.type == 'note_on':
                # Remove quiet notes
                if msg.velocity < 5 or msg.note < 10:
                    msg = msg.copy(velocity=0)
                # Transpose up by 12 semitones
                new_note = max(min(msg.note + octave, 127), 0)
                msg = msg.copy(note=new_note)
                track[i] = msg  # Replace the message in the track
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
        "-codec:a", "libmp3lame",
        "-qscale:a", "2",
        mp3_path
    ])

clean_midi(midi_path)

convert_midi_to_audio(
    midi_path,
    os.path.join(script_path, "soundfont", "Pan_Flute.sf2"),
    wav_path
)

mp3_path = os.path.join(script_path, "final.mp3")
os.remove(mp3_path)

convert_wav_to_mp3(
    wav_path,
    mp3_path
)
os.remove(wav_path)
