from mp3_tagger import MP3File, VERSION_BOTH
from tqdm import tqdm

index = 1

def clean_all_tagger(audio_path, index):
    audio = MP3File(str(audio_path))
    audio.set_version(VERSION_BOTH)
    
    audio.band = ''
    audio.composer = ''
    audio.copyright = ''
    audio.publisher = ''
    # audio.track = 0
    # audio.genre = ''
    audio.url = ''
    audio.save()
    tqdm.write(f'{index} ✅ cleaned')

if __name__ == '__main__':
    print('''you are running me directly,
you should run me as a package''')
