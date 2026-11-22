import os
import shutil
from pathlib import Path

def main():
    bot_dir = Path(os.environ.get('MAKEFUN_BOT_DIR', '.'))
    output_dir_env = os.environ.get('MAKEFUN_OUTPUT_DIR')
    
    if not output_dir_env:
        raise RuntimeError("MAKEFUN_OUTPUT_DIR environment variable is not set")
    
    output_dir = Path(output_dir_env)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    src = bot_dir / 'entry.png'
    if not src.exists():
        raise FileNotFoundError(f"Source image not found at {src}")
    
    dst = output_dir / 'entry.png'
    shutil.copy2(src, dst)
    print(f"Copied {src} to {dst}")

if __name__ == '__main__':
    main()
