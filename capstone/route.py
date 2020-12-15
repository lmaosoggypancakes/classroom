from pathlib import Path as path
print(path(__file__).resolve(strict=True).parent)