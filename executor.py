from clean_music import clean_all, clean_comment, edit_artist, clean_song, clean_title, edit_album
from pathlib import Path
from tqdm import tqdm

# path of the folder you want to work on
folder = Path('data')
files = list(folder.glob('*.mp3'))


# executor of clean comments
def comments():
    with tqdm(total=len(files), desc="Processing", ncols=80, leave=True) as pbar:
        for audio_path in files:
            try:
                clean_comment.clean_comment_tagger(audio_path, clean_comment.index)
            except Exception as e:
                tqdm.write(f'{clean_comment.index} ❌ Error : {e}')
            finally:
                clean_comment.index += 1
                pbar.update(1)


# executor of clean all other tags
def all():
    with tqdm(total=len(files), desc="Processing",ncols=80, leave=True) as pbar:
        for audio_path in files:
            try:
                clean_all.clean_all_tagger(audio_path, clean_all.index)
            except Exception as e:
                tqdm.write(f'{clean_all.index} ❌ Error : {e}')
            finally:
                clean_all.index += 1
                pbar.update(1)

# executor of edit artist
def artist_menu():
    while True:
        print('////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
        
        # clear artists list for the next round of the loop
        edit_artist.artists.clear()

        # list current artists
        edit_artist.print_list(edit_artist.human_index, files)

        # get search input
        wanted_artist = input('which artist to find: ')

        # reset good matches
        edit_artist.reset_good_matches()

        # loop though songs find similar songs and human_index them
        edit_artist.find_similar_artists(wanted_artist=wanted_artist, artist_list=edit_artist.artists)
        edit_artist.print_matches(wanted_artist)

        # get confirmation
        confirmation = input('Is the result ok?(y/n(search again)/r(remove some results)/e(exit program)): ').lower().strip()
        
        # if y change all
        if confirmation == 'y':
            new_name = input('Give me a new artist name: ').title()
            edit_artist.set_new_name(new_name, files)
            edit_artist.artists.clear()  
                    


        # if r remove some
        elif confirmation == 'r':
            while True:
                print(f'len of good_matches {len(edit_artist.good_matches)}')
                command = input('which one to remove?(type e when finished): ').lower().strip()
                
                # if is number
                if command.isdigit():
                    if (int(command) - 1) in range(len(edit_artist.good_matches)):                        
                        edit_artist.remove_match(int(command))
                        edit_artist.print_matches(wanted_artist)                        

                    else:
                        print('Wrong input, try again..')
                # if is a String
                elif command == 'e':
                    if not edit_artist.good_matches:
                        print("⚠️ No matches left to rename!")
                        break
                    edit_artist.print_matches(wanted_artist)
                    new_name = input('Give me a new artist name: ').title()
                    edit_artist.set_new_name(new_name, files)
                    edit_artist.artists.clear()
                    break
                # else
                else:
                    print('Wrong input, try again..')


        # if n search again(continue)
        elif confirmation == 'n':
            print('Search again..')
            continue

        # if E exit the program
        elif confirmation == 'e':
            print('Good bye!')
            break

        # if none go back again
        else:
            print('Wrong input, try again..')
            continue

# executor of edit song
def song():
    with tqdm(total=len(files), desc="Processing",ncols=80, leave=True) as pbar:
        for audio_path in files:
            try:
                clean_song.clean_song_tagger(audio_path, clean_song.index)
            except Exception as e:
                tqdm.write(f'{clean_song.index} ❌ Error : {e}')
            finally:
                clean_song.index += 1
                pbar.update(1)


# executor of edit album
def album():
    with tqdm(total=len(files), desc="Processing",ncols=80, leave=True) as pbar:
        for audio_path in files:
            try:
                edit_album.clean_album_tagger(audio_path, edit_album.index)
            except Exception as e:
                tqdm.write(f'{edit_album.index} ❌ Error : {e}')
            finally:
                edit_album.index += 1
                pbar.update(1)

# executor of edit title
def title():
    with tqdm(total=len(files), desc="Renaming",ncols=80, leave=True) as pbar:
        for file in files:
            try:
                clean_title.clean_title(file, clean_title.index)
            except Exception as e:
                tqdm.write(f'{clean_title.index} ❌ Error : {e}')
            finally:
                clean_title.index += 1
                pbar.update(1)


# uncomment each program you want to run

# comments()
# all()
# artist_menu()
# song()
# album()
# title()