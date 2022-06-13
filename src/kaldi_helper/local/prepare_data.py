import os
import glob
import subprocess
import argparse

def main(audio_folder, export_folder):
    audio_files = os.listdir(audio_folder)
    audio_files = [os.path.basename(f) for f in audio_files]

    # Prepare wav.scp
    wav_scps = [f"{f.split('.')[0]} {audio_folder}/{f}" for f in audio_files]
    with open(f"{export_folder}/wav.scp", "w") as f:
        f.write("\n".join(sorted(wav_scps)))
    
    # Prepare text
    texts = [f"{f.split('.')[0]} NONE" for f in audio_files]
    with open(f"{export_folder}/text", "w") as f:
        f.write("\n".join(sorted(texts)))

    # Prepare utt2spk
    utt2spks = [f"{f.split('.')[0]} {f[:f.find('-')]}" for f in audio_files]
    with open(f"{export_folder}/utt2spk", "w") as f:
        f.write("\n".join(sorted(utt2spks)))
    

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_folder", type=str)
    parser.add_argument("export_folder", type=str)

    args = parser.parse_args()
    main(args.audio_folder, args.export_folder)
