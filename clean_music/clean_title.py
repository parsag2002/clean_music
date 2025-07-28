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

def clean_title(file, index):
    old_name = file.stem
    new_name = clean_text(old_name)

    # Skip if name didn't change
    if new_name and new_name != old_name:
        new_path = file.with_name(new_name + file.suffix)
        file.rename(new_path)
        tqdm.write(f'{index} ✅ cleaned to: {new_name}')
    else:
        tqdm.write(f'{index} ❎ left as: {old_name}')

if __name__ == '__main__':
    print('''you are running me directly,
you should run me as a package''')
