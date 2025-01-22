import subprocess
import os
import json
import random
from typing import List
from pydub.utils import mediainfo
from collections import Counter

RESOURCES_PATH = os.path.dirname(os.path.realpath(__file__))


def normalize_name(name: str):
    return name.lower().strip()


def cut_audio(start: str,
              end: str,
              input="full_audio.mp3",
              output="audio.mp3"):
    """
    Cut a part of the audio.

    Args:
        start: The start time for the cut. Format mm:ss. Consider format_time().
        end: The end time for the cut. Format mm:ss. Consider format_time().
        input (optional): The path to the input audio file.
        output (optional): The path to save the output audio file.
    """
    try:
        print("Cutting audio...")
        input_path = os.path.join(RESOURCES_PATH, input)
        output_path = os.path.join(RESOURCES_PATH, output)
        cmd = [
            "ffmpeg", "-i", input_path, "-ss", start, "-to", end, "-c", "copy",
            output_path, "-y"
        ]
        subprocess.run(cmd, check=True)
        print(f"Saved file as {output_path}"
              ".")
    except subprocess.CalledProcessError as e:
        print(f"Error cutting audio: {e}")


def format_time(duration: float):
    minutes = int(duration // 60)
    seconds = int(duration % 60)

    return f"{minutes}:{seconds:02}"


class Song():

    def __init__(self, url: str, names: set[str], author: str):
        self.url = url
        self.names = names
        self.author = author
        self.duration = 0
        self.end_preview = 5
        self.start_preview = 0
        self.winner = None

    def download_audio(self, file_name="full_audio.mp3", format="mp3"):
        """
        Download full audio track
        """
        try:
            print("Downloading audio...")
            cmd = [
                "yt-dlp", "--extract-audio", "--audio-format", format, "-o",
                f"{RESOURCES_PATH}/{file_name}", self.url
            ]
            subprocess.run(cmd, check=True)
            print(f"Complete audio saved as {RESOURCES_PATH}/{file_name}.")
            self.duration = float(
                mediainfo(f"{RESOURCES_PATH}/full_audio.mp3")['duration'])
            self.end_preview = random.randint(3, int(self.duration - 6))
            self.start_preview = self.end_preview - 3
        except subprocess.CalledProcessError as e:
            print(f"Error downloading audio: {e}")

    def extend(self):
        self.end_preview += 3
        cut_audio(format_time(self.start_preview),
                  format_time(self.end_preview))

    def match(self, song: str, sender) -> bool:
        ret = any(song.lower().strip() == name.lower().strip()
                  for name in self.names)
        if ret == True:
            self.winner = sender
        return ret

    def to_json(self):
        return {
            "names": list(self.names),
            "author": self.author,
            "url": self.url,
            "winner": self.winner
        }

    def add_song(self, song) -> bool:
        with open(f"{RESOURCES_PATH}/old_songs.json", "r") as f:
            data_old = json.load(f)
        with open(f"{RESOURCES_PATH}/songs.json", "r") as f:
            data = json.load(f)

        for data_song in data:
            loaded_names = [
                normalize_name(name) for name in data_song["names"]
            ]
            if any(
                    normalize_name(name) in loaded_names
                    for name in song.names):
                return False

        for data_song in data_old:
            loaded_names = [
                normalize_name(name) for name in data_song["names"]
            ]
            if any(
                    normalize_name(name) in loaded_names
                    for name in song.names):
                return False

        if any(song.url.strip() == song_entry["url"].strip()
               for song_entry in data):
            return False

        if any(song.url.strip() == old_song["url"].strip()
               for old_song in data_old):
            return False

        data.append(song.to_json())
        with open(f"{RESOURCES_PATH}/songs.json", "w") as f:
            json.dump(data, f, indent=4)
        return True


class SongSelector():

    def __init__(self):
        self.current_song = None
        self.file = os.path.dirname(os.path.realpath(__file__))

    def pick_new(self):
        try:
            os.remove(f"{RESOURCES_PATH}/full_audio.mp3")
            os.remove(f"{RESOURCES_PATH}/audio.mp3")
        except Exception as e:
            print("No file to remove")

        with open(f"{self.file}/songs.json", "r") as f:
            data = json.load(f)
            print(f"{data} {len(data)}")
            data = data[random.randint(0, len(data) - 1)]
            self.current_song = Song(data.get("url"), data.get("names"),
                                     data.get("author"))

        self.current_song.download_audio()
        cut_audio(format_time(self.current_song.start_preview),
                  format_time(self.current_song.end_preview),
                  input=f"{RESOURCES_PATH}/full_audio.mp3",
                  output=f"{RESOURCES_PATH}/audio.mp3")

    def store_old(self):
        try:
            with open(f"{RESOURCES_PATH}/old_songs.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data.append(self.current_song.to_json())

        with open(f"{RESOURCES_PATH}/old_songs.json", "w") as f:
            json.dump(data, f, indent=4)

        # Remove from songs.json
        try:
            with open(f"{RESOURCES_PATH}/songs.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data = [song for song in data if song["url"] != self.current_song.url]

        with open(f"{RESOURCES_PATH}/songs.json", "w") as f:
            json.dump(data, f, indent=4)

    def match(self, name: str, sender) -> bool:
        if self.current_song.match(name, sender):
            self.pick_new()

    def get_ranking(self) -> str:
        try:
            with open(f"{RESOURCES_PATH}/old_songs.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        winners = [song["winner"] for song in data if song["winner"]]
        ranking = Counter(winners)
        ranking_sorted = ranking.most_common()

        s = ("""Ranking:""")
        for rank, (winner, count) in enumerate(ranking_sorted, start=1):
            s += f"\n{rank}. {winner}: {count} pp"
        return s


# Example
if __name__ == "__main__":
    s = SongSelector()
    s.pick_new()
    s.store_old()
    '''
    url_video = "https://www.youtube.com/watch?v=xvUO2FYtIEY"
    start = "00:01:00"  # hh:mm:ss
    end = "00:02:00"  # hh:mm:ss
    
    download_audio(url_video)
    cut_audio(start, end, input="full_audio.mp3", output="audio.mp3")
    song = Song(url_video, ["anomaly"], "camellia")
    print(song.match("aanomaly"))            # false
    print(song.match("aanomalya"))           # false
    print(song.match("ano"))                 # false
    print(song.match("anomaly"))             # true
    print(song.match("            anoMaly")) # true
    print(song.match("anomaly "))            # true
    '''
