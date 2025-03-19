import os
import platform
if platform.system() == "Windows":
    import winsound

# Determine the script's directory and construct the Sounds folder path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(SCRIPT_DIR, "..", "Sounds")

# Check if sound is available (Windows with winsound)
SOUND_AVAILABLE = platform.system() == "Windows"

def play_sound(sound_file):
    """Play a sound effect asynchronously."""
    if SOUND_AVAILABLE:
        full_path = os.path.join(SOUNDS_DIR, sound_file)
        if os.path.exists(full_path):
            winsound.PlaySound(full_path, winsound.SND_ASYNC)
