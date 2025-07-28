from mp3_tagger import MP3File, VERSION_BOTH
from tqdm import tqdm

index = 1

def clean_comment_tagger(audio_path, index):
    audio = MP3File(str(audio_path))
    audio.set_version(VERSION_BOTH)
    
    # has a comment
    if str(audio.comment[0])[-5] != 'N':
        tqdm.write(f'{index} has a comment: {audio.comment}')
        audio.comment = ''
        audio.save()        
        tqdm.write(f'✅ cleaned comment for {audio_path}')
    # dosent have comment
    else:
        tqdm.write(f'{index} ❎ didnt had comment the music {audio_path}')


if __name__ == '__main__':
    print('''you are running me directly,
you should run me as a package''')
