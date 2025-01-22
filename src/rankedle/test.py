import json
from main import Song


def normalize_name(name):
            return name.lower().strip()


def add_song(song: Song) -> bool:
    with open("./old_songs.json", "r") as f:
            data_old = json.load(f)
    with open("./songs.json", "r") as f:
            data = json.load(f)        

    
    # Comprobar nombres en songs.json
    for data_song in data:
          loaded_names = [normalize_name(name) for name in data_song["names"]]
          if any(normalize_name(name) in loaded_names for name in song.names):
                print(1)
                return False

    for data_song in data_old:
          loaded_names = [normalize_name(name) for name in data_song["names"]]
          if any(normalize_name(name) in loaded_names for name in song.names):
                print(2)
                return False
    
    
    if any(song.url.strip() == song_entry["url"].strip() for song_entry in data):
        print(3)
        return False

    if any(song.url.strip() == old_song["url"].strip() for old_song in data_old):
        print(4)
        return False
    
    # Añadir la canción si no existe
    data.append(song.to_json())
    with open("./songs.json", "w") as f:
        json.dump(data, f, indent=4)
    return True

print(add_song(Song("https://www.youtube.com/watch?v=5Cof9rP7TEQ", ["In the garden"], "Primary")))
print(add_song(Song("https://www.youtube.com/watch?v=Ng1qtXk8GBQ", ["Quaasar Dreams"], "Fvrwvrd")))