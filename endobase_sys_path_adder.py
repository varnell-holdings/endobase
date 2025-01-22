
from pathlib import Path
import sys.path



home = Path.home()

p1 = home / "Miniconda3"
p2 = p1 / "Scripts"
p3 = p1 / "Library" / "bin"

sys.path.append(p1)
sys.path.append(p2)
sys.path.append(p3)