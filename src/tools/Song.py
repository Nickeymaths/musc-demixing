from pydub import AudioSegment
from setuptools import setup
from pathlib import Path
from pydub import AudioSegment


class Song:
    def __init__(self, song_folder: Path, author: str, cover: Path):
        self.cover = cover
        self.author = author

        song_parts = [song_folder.name, "bass", "piano", "drum", "vocals", "other"]
        self.song_part_ditcs = {part_name: AudioSegment.from_file(Path(song_folder, f"{part_name}.mp3"), format="mp3") for part_name in song_parts}
    
    def get_low(self, x: int, part_name: str):
        self.song_part_ditcs[part_name] -= x

    def get_high(self, x: int, part_name: str):
        self.song_part_ditcs[part_name] += x
    
    def replace_part(self, part_name, target: Path):
        pass

    def accelerate(self, part_name, speed: float):
        pass

    def export(self, output: Path, tags: Dict[str, str], cover: Path,  bitrate="320k"):
        self.song_part_ditcs[part_name].export(output, format="mp3", bitrate=bitrate, tags=tags, cover=cover)
