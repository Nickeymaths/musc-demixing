from wsgiref import util
from .tools import utils
from pathlib import Path
import subprocess
import os

class Application(object):
    def __init__(self):
        pass
    
    # Tách bài hát thành các thành phần
    def spleetSong(self, mp3_path, user_folder_path):
        lib_path = f"{user_folder_path}/lib"
        tmp_path = f"{user_folder_path}/tmp/demixing"
        stem = 5

        utils.demixing(mp3_path, lib_path, tmp_path, stem)
        print("Tách bài hát thành các thành phần")
    
    # Tạo bài hát hoàn chỉnh từ mảng tham số được truyền vào
    def combineSong(self, part_location_list, user_folder_path, song_name):
        song_folder_in_lib = Path(user_folder_path, song_name)
        song_folder_in_lib.mkdir(exist_ok=True, parents=True)
        utils.mixing(part_location_list, str(song_folder_in_lib))
        print("Tạo bài hát hoàn chỉnh từ mảng tham số được truyền vào")

    # Tách lời bài hát
    def detachLyric(self, user_folder_path, song_name):
        print("Tách lời bài hát")
        """
            input: đường dẫn đến bài hát
            output: void
        """

        song_name = song_name.lower().replace(" ", "_")
        input_mp3 = f"{user_folder_path}/lib/{song_name}/vocals.mp3"

        lyric_folder = Path(f"{user_folder_path}/lib/{song_name}/lyrics")
        tmp_folder = Path(f"{user_folder_path}/tmp/lyric_seperation/{song_name}")
        log_folder = Path(f"{user_folder_path}/log/lyric_seperation/{song_name}")

        utils.seperate_lyrics(input_mp3, tmp_folder, lyric_folder, log_folder)
    
    def export_custom_mixing_song(self, output_folder, part_song_path_list, new_song_name):
        utils.mixing(part_song_path_list, output_folder, new_song_name)
    
    def export_duration_info(self, user_folder_path, song_name):
        song_name = song_name.lower().replace(" ", "_")
        file_path = os.path.join(user_folder_path, "lib", song_name, "vocals.mp3")
        output_file_path = os.path.join(user_folder_path, "lib", song_name, "duration_info.txt")
        subprocess.run(f"ffprobe -show_entries format=duration -i {file_path} > {output_file_path}", shell=True)