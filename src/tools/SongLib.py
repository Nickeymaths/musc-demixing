from pathlib import Path
import traceback

from .Song import Song


class SongLib:
    def __init__(self, user_data_folder_path: str):
        self.user_data_folder = Path(user_data_folder_path).resolve()
        self.songs_folder = Path(f"{str(self.user_data_folder)}/songs")
        self.tmp_dir = Path(f"{str(self.user_data_folder)}/temp")

    def get_song_list(self) -> List[Song]:
        return [Song(p) for p in self.songs_folder.iterdir()]
    
    def get_song(self, song_name: str) -> Song:
        song_folder = Path(self.songs_folder, song_name)
        if song_folder.exists():
            return Song(song_folder)
        
        else:
            traceback.print_exc()
    
    def add_song(self):
        pass

    def rm_song(self) -> Song:
        pass

    def update_song(self, song: Song):
        pass

    def next_song(self) -> Song:
        pass

    def back_song(self) -> Song:
        pass
    



        
