import subprocess
import os
import glob
from subprocess import Popen, PIPE, STDOUT
import sys
from pathlib import Path
import argparse

def resource_path(relative=''):
    root = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    return os.path.join(root, 'data', relative)


def demixing(input_sound_path, output_folder_path, temporary_folder_path, stem):
    input_sound_file = Path(input_sound_path)
    output_folder = Path(output_folder_path)
    temporary_folder = Path(temporary_folder_path)

    if input_sound_file.exists():
        cmd = f"bash src/tools/spleeter-wrapper.sh -f {str(input_sound_file.resolve())} -o {str(output_folder.resolve())} -t {str(temporary_folder.resolve())} -s {stem}"
        # cmd = "bash src/tools/simple.sh"
        sub_process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

        with sub_process.stdout:
            for line in iter(sub_process.stdout.readline, b''):
                print(line.decode("utf-8").strip())

def mixing(input_sound_paths, output_file_path):
    cmd = "ffmpeg"
    for sf in input_sound_paths:
        cmd += f" -i {sf}"
    
    cmd += f" -filter_complex amix=inputs={len(input_sound_paths)}:duration=shortest {output_file_path}"
    sub_process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
    with sub_process.stdout:
        for line in iter(sub_process.stdout.readline, b''):
                print(line.decode("utf-8").strip())

def decode_result2lyric(decoded_file, output_file):
    scripts = []
    with open(decoded_file, "r") as f:
        lines = f.readlines()
        scripts = [f.split(" ", 1)[1].strip().lower() for f in lines]
    
    with open(output_file, "w") as f:
        f.write(" ".join(scripts))

def seperate_lyrics(input_sound_path, tmpdir, outputdir, logdir):
    subprocess.run(f"mkdir -p {outputdir} {tmpdir}", shell=True)
    cmd = f"./src/kaldi_helper/run.sh {input_sound_path} {tmpdir} {logdir}"
    subprocess.run(cmd, shell=True)

    tmp_dir_of_sound = os.path.basename(input_sound_path).split('.')[0]
    tmp_dir_of_sound = tmp_dir_of_sound.lower().replace(" ", "_")
    decode_dir = Path(tmpdir, tmp_dir_of_sound, "decode_results/scoring_kaldi/penalty_1.0")
    
    for i, f in enumerate(glob.glob(f"{decode_dir}/*.txt")):
        decode_result2lyric(f, f"{outputdir}/lyric_{i}.txt")

if __name__ == "__main__":
    # argpaser = argparse.ArgumentParser(description="Command line for music demixing")
    # argpaser.add_argument("input_sound_file", type=str, help="Input sound file path, allowed format: mp3,wav")
    # argpaser.add_argument("output_folder", type=str, help="Output folder with contain results")
    # argpaser.add_argument("temporary_folder", type=str, help="Output temporary data folder with contain results")
    # argpaser.add_argument("stem", type=int, default=5, help="Output temporary data folder with contain results")

    # args = argpaser.parse_args()
    # demixing(args.input_sound_file, args.output_folder, args.temporary_folder, args.stem)

    argpaser = argparse.ArgumentParser(description="Command line for music demixing")
    argpaser.add_argument("input_sound_file", type=str, help="Input sound file path, allowed format: mp3,wav")
    argpaser.add_argument("temporary_folder", type=str, help="Output temporary data folder with contain results")
    argpaser.add_argument("output_folder", type=str, help="Output folder with contain results")
    argpaser.add_argument("log_dir", type=str, help="Log dir of lyric separation processing")

    args = argpaser.parse_args()
    seperate_lyrics(args.input_sound_file, args.temporary_folder, args.output_folder, args.log_dir)