from mp3_tagger import MP3File ,VERSION_BOTH
from pathlib import Path
from thefuzz import process
from thefuzz import fuzz
from tqdm import tqdm

human_index = 1
artists = []

def list_artists(audio_path, human_index):
    audio = MP3File(str(audio_path))
    audio.set_version(VERSION_BOTH)
    artists.append(str(audio.artist[0])[16:-1])



def find_similar_artists(wanted_artist, artist_list, threshold=70):
    wanted = wanted_artist.lower().strip()
    
    # Use fuzzy search against all artists
    matches = process.extract(wanted, artist_list, scorer=fuzz.partial_ratio)

    # Filter by threshold
    global good_matches
    good_matches = [(artist, score) for artist, score in matches if score >= threshold]

def print_matches(wanted_artist):
    # Show results
    if good_matches:
        print(f"\n🔍 Similar matches for '{wanted_artist}':")
        i = 1
        for artist, score in sorted(good_matches, key=lambda x: -x[1]):
            print(f"🎵 {i}- {artist} (match score: {score})")
            i += 1
    else:
        print("❌ No similar matches found.")



def set_new_name(new_name, files):
    with tqdm(total=len(good_matches), desc='Editing', ncols=80, leave=True) as pbar:
        for i in range(len(good_matches)):
            artist_to_change = good_matches[i][0]
            tqdm.write(artist_to_change)
            for artist in artists:
                if artist_to_change == artist:
                    human_index = artists.index(artist) + 1
                    tqdm.write(f'artist to change {artist_to_change} and artist {artist} in human_index of {human_index}')

                    # find its path
                    file_path = files[artists.index(artist)]

                    # open it with mp3_tagger
                    audio = MP3File(str(file_path))
                    audio.set_version(VERSION_BOTH)
                    
                    # change the artist tag
                    audio.artist = new_name
                    audio.save()
                    tqdm.write("✅ Artist tag updated successfully.")

                    # edit the list of artists so it dose not find the same one
                    artists[artists.index(artist)] += ' done'
                    break
            pbar.update(1)

def remove_match(nth):
    index_to_remove = nth - 1
    good_matches.pop(index_to_remove)

def print_list(human_index, files):
    print('\n')
    # create the list to work on
    with tqdm(total=len(files), desc='Scanning', ncols=80, leave=True) as pbar:
        for audio_path in files:
            try:
                list_artists(audio_path, human_index)
            except:
                pass
            pbar.update(1)

    # print unic artists to user
    with tqdm(total=len(set(artists)), desc='Printing', ncols=80, leave=True) as pbar:
        for unic_artist in set(artists):
            tqdm.write(f'{human_index} name: {unic_artist}')
            human_index += 1
            pbar.update(1)
        human_index = 1

def reset_good_matches():
    good_matches = []

if __name__ == '__main__':
    print('''you are running me directly,
you should run me as a package''')
