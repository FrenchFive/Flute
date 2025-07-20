# Flute

**Flute** is a Python tool that transforms a YouTube music video into a solo pan flute performance. It uses audio source separation, pitch detection, MIDI editing, and synthesis to recreate the melody from any song — rendered with a pan flute sound.

---

## 🧠 What It Does

1. **Downloads** a YouTube video (audio only).
2. **Separates** stems using a source separation model.
3. **Extracts melody** using BasicPitch.
4. **Cleans and transposes** the MIDI.
5. **Synthesizes audio** using FluidSynth and a pan flute soundfont.
6. **Converts to MP3** for final output.

---

## 📦 Dependencies

You'll need the following Python packages and tools installed:

### Python packages:

* `yt-dlp`
* `mido`
* `basic-pitch`
* `demucs`
* system `ffmpeg`

Install them using:

```bash
pip install yt-dlp mido basic-pitch demucs
```

### System requirements:

* `ffmpeg`
* `fluidsynth`

---

## 🚀 Usage

### 1. Add YouTube URL

You can paste a URL in a file named `ytb.txt`, or it will default to a preset example.

```txt
https://www.youtube.com/watch?v=your_video_id
```

### 2. Download and Split Audio

```bash
python ytb.py
```

This will:

* Download the YouTube audio.
* Split it into stems (`vocals`, `drums`, `bass`, `other`).

### 3. Generate Flute MIDI and MP3

```bash
python flute.py
```

This will:

* Combine stems (excluding drums and bass).
* Run pitch prediction with BasicPitch.
* Clean and transpose the MIDI.
* Synthesize the audio using FluidSynth + pan flute soundfont.
* Convert to a final MP3 file.

---

## 🔧 Customization

* **Transposition**: Change `octave = 0` in `flute.py` to control pitch range.
* **Soundfont**: Replace `Pan_Flute.sf2` in the `soundfont/` folder with your preferred `.sf2` file.

---

## 📜 License

MIT License

---

## 💡 Credits

* [BasicPitch (by Spotify)](https://github.com/spotify/basic-pitch) – For pitch extraction.
* [yt-dlp](https://github.com/yt-dlp/yt-dlp) – For downloading audio.
* [FluidSynth](https://www.fluidsynth.org/) – For MIDI synthesis.
* [Demucs](https://github.com/facebookresearch/demucs) – For source separation (if used in `unmix`).
* Pan flute SoundFont (credit the source if applicable).

---

Let me know if you'd like me to also clean or restructure your code files!
