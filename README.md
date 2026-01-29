<h1 align="center">MusicFakez</h1>

<p align="center">A Python script to fake your music library using MusicBrainz</p>

## Why?

If you want to share your Unix rice, but don't want others to know your music taste, then this tool is perfect you! Provide an album name and generate empty songs, complete with metadata.

**Why not just download the album?**

Save network bandwidth by not actually downloading the songs. Also, unlike other music downloaders, this tool is perfectly legal :)

**Why not a Bash script?**

Because I wanted to avoid too many dependencies. This tool only requires Python and FFmpeg.

## How to use

Make sure the above mentioned dependencies are installed.

```bash
git clone https://github.com/svhl/musicfakez
cd musicfakez
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set the download path in the `location` variable within the script before executing it.

```bash
python3 musicfakez.py
```

## License

The GNU General Public License v3.0
