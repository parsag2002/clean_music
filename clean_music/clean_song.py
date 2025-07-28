from mp3_tagger import MP3File ,VERSION_BOTH
from tqdm import tqdm
import re

index = 1

def clean_text(text):
    # Keep only parentheses that contain 'feat' or 'ft'
    def keep_feat(match):
        content = match.group(1).lower()
        return f"({content})" if "feat" in content or "ft" in content else ""

    # Step 1: keep only (feat...) or (ft...), remove others
    text = re.sub(r"\(([^)]*)\)", keep_feat, text)

    # Step 2: remove website addresses like www.example.com or example.ir
    text = re.sub(r"(www\.)?\b[\w-]+\.(com|ir|net|org|info)\b", "", text, flags=re.IGNORECASE)

    # Step 3: replace dashes/underscores with spaces (preserve word separation)
    text = re.sub(r"[-_]+", " ", text)

    # Step 4: remove all characters except letters, spaces, &, and parentheses
    text = re.sub(r"[^a-zA-Z&()\s]", "", text)

    # Step 5: remove all digits
    text = re.sub(r"\d+", "", text)

    # Step 6: collapse multiple spaces and strip
    text = re.sub(r"\s+", " ", text).strip()

    return text.strip()

def clean_song_tagger(audio_path, index):
    audio = MP3File(str(audio_path))
    audio.set_version(VERSION_BOTH)
    
    pure_name= str(audio.song[0])[14:-1]
    new_name = clean_text(pure_name)
    if new_name:
        audio.song = new_name
        audio.save()
        tqdm.write(f'{index} ✅ cleaned to: {clean_text(pure_name)}')
    else:
        tqdm.write(f'{index} ❎ left as: {pure_name}')

if __name__ == '__main__':
    print('''you are running me directly,
you should run me as a package''')
