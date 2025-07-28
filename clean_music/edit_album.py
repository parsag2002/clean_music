from mp3_tagger import MP3File ,VERSION_BOTH
from tqdm import tqdm
import re

index = 1

def is_valid_album(album: str) -> bool:
    album = album.strip()

    # Empty or too short or too long
    if not album or len(album) < 3 or len(album) > 50:
        return False

    # Contains URL or domain name
    if re.search(r"(www\.|\.com|\.ir|\.net|\.org)", album, re.IGNORECASE):
        return False

    # Contains common spammy keywords
    spam_words = ['site', 'music', 'download', 'mp3', 'media', 'track', 'listen']
    if any(word in album.lower() for word in spam_words):
        return False

    # Only digits or mostly symbols
    if re.fullmatch(r"[\W\d\s]+", album):
        return False

    # Album is suspiciously all uppercase or lowercase
    if album == album.upper() or album == album.lower():
        return False

    # Passed all filters — assume it's a valid album
    return True

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

def clean_album_tagger(audio_path, index):
    audio = MP3File(str(audio_path))
    audio.set_version(VERSION_BOTH)
    
    pure_name= str(audio.album[0])[15:-1]
    if is_valid_album(pure_name):
        tqdm.write(f'{index} ❎ was a valid album: {pure_name}')
    else:
        new_name = clean_text(pure_name)
        if new_name:
            audio.album = new_name
            audio.save()
            tqdm.write(f'{index} ✅ cleaned to: {clean_text(pure_name)}')
        else:
            tqdm.write(f'{index} ❎ left as: {pure_name}')

if __name__ == '__main__':
    print('''you are running me directly,
you should run me as a package''')
