from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('/Users/lchris/Desktop/Coding/python/hackathons/hackuci/flashME/.env')
load_dotenv(dotenv_path=env_path)

uri = os.getenv("WHOISGAY")
print(uri)


