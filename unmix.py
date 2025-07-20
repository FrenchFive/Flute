import os
import torch
import torchaudio
import subprocess
from demucs.apply import apply_model
from demucs.pretrained import get_model
from demucs.audio import AudioFile

def audio_split(input_audio_path: str, output_dir: str, model_name="htdemucs"):
    """
    Separates audio using Demucs and saves all stems as individual .mp3 files.
    Ensures correct stem-to-source mapping using the model's metadata.
    """
    os.makedirs(output_dir, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    model = get_model(name=model_name).to(device)
    model.eval()

    print(f"Loading {input_audio_path}")
    file = AudioFile(input_audio_path)
    wav = file.read(streams=0, samplerate=model.samplerate, channels=model.audio_channels)
    wav = wav.to(device)

    ref = wav.mean(0)
    wav = (wav - ref.mean()) / ref.std()

    print("Separating sources...")
    with torch.no_grad():
        sources = apply_model(model, wav[None], device=device)[0]  # shape: [N, T]

    # Get correct stem names from model
    if hasattr(model, 'sources'):
        stem_names = model.sources
    else:
        # Default fallback order
        stem_names = ['vocals', 'drums', 'bass', 'other']

    # Save each stem as .wav and convert to .mp3
    for i, stem in enumerate(stem_names):
        wav_path = os.path.join(output_dir, f"{stem}.wav")
        mp3_path = os.path.join(output_dir, f"{stem}.mp3")

        print(f"Saving {stem} as {mp3_path}")
        torchaudio.save(wav_path, sources[i].cpu(), model.samplerate)

        # Convert to MP3
        subprocess.run([
            "ffmpeg", "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-qscale:a", "2", mp3_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        os.remove(wav_path)  # Clean up



def combine_stems(output_path: str, stem_dir: str,
                  vocals=True, drums=False, bass=True, other=True):
    """
    Combines selected stems from .mp3 files and saves the result as .wav.

    Parameters:
    - output_path: Final mixed file path (should be .wav)
    - stem_dir: Directory where the .mp3 stems are
    - vocals, drums, bass, other: Whether to include each stem in the mix
    """
    stem_flags = {
        "vocals": vocals,
        "drums": drums,
        "bass": bass,
        "other": other
    }

    waveforms = []
    sample_rate = None

    for stem, include in stem_flags.items():
        if include:
            mp3_path = os.path.join(stem_dir, f"{stem}.mp3")
            if not os.path.exists(mp3_path):
                print(f"Warning: {stem}.mp3 not found, skipping.")
                continue
            waveform, sr = torchaudio.load(mp3_path)
            waveforms.append(waveform)
            if sample_rate is None:
                sample_rate = sr
            elif sr != sample_rate:
                raise ValueError(f"Sample rate mismatch in {stem}.mp3")

    if not waveforms:
        raise RuntimeError("No valid stems selected or found to combine.")

    mix = sum(waveforms)
    torchaudio.save(output_path, mix, sample_rate)
    

    #convert to MP3
    mp3_path = output_path.replace('.wav', '.mp3')
    subprocess.run([
        "ffmpeg", "-y", "-i", output_path, "-codec:a", "libmp3lame", "-qscale:a", "2", mp3_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Combined mix saved to: {mp3_path}")


# Example usage
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "audio.mp3")
    output_dir = os.path.join(script_dir, "separated")

    # Step 1: Split audio
    audio_split(input_path, output_dir)

    # Step 2: Combine stems (e.g., everything except drums)
    combine_stems(
        output_path=os.path.join(script_dir, "audio_nodrums.wav"),
        stem_dir=output_dir,
        vocals=True, drums=False, bass=False, other=True
    )
