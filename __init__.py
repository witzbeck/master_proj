from pathlib import Path
from sys import path
path.append(str(Path(__file__).parent.parent))
path.append(str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
load_dotenv()
