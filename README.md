<h1 align="center">MusicFakez</h1>

<p align="center">
  <img src="https://github.com/user-attachments/assets/e91dce23-f9c0-4131-8096-3e077053d346" width="500")
</p>

<p align="center">A Python script to fake your music library using MusicBrainz</p>

## Why?

If you want to showcase your custom CLI music player rice, but don't want others to know your music taste, then this tool is for you! Provide an album name and generate empty songs filled with silence, complete with metadata such artist name, genre, and release year.

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
python3 musicfakez.py
```

You can change the download path in the `location` variable within the script.

## License

The GNU General Public License v3.0
