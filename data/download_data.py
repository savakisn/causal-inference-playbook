"""Download the Criteo Uplift Modeling dataset from HuggingFace."""

import gzip
import shutil
from pathlib import Path

import requests

DATA_DIR = Path(__file__).parent
URL = "https://huggingface.co/datasets/criteo/criteo-uplift/resolve/main/criteo-research-uplift-v2.1.csv.gz"
GZ_FILE = DATA_DIR / "criteo-research-uplift-v2.1.csv.gz"
CSV_FILE = DATA_DIR / "criteo-research-uplift-v2.1.csv"


def download():
    if CSV_FILE.exists():
        print(f"Already downloaded: {CSV_FILE}")
        return

    print("Downloading Criteo Uplift v2.1 from HuggingFace (~300 MB)...")
    with requests.get(URL, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        downloaded = 0
        with open(GZ_FILE, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    print(f"\r  {100*downloaded/total:.1f}%  ({downloaded/1e6:.0f} MB)", end="", flush=True)
    print(f"\nSaved {GZ_FILE}")

    print("Decompressing...")
    with gzip.open(GZ_FILE, "rb") as gz, open(CSV_FILE, "wb") as out:
        shutil.copyfileobj(gz, out)
    GZ_FILE.unlink()
    print(f"Done: {CSV_FILE}")


if __name__ == "__main__":
    download()
