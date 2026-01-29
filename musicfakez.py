#       __  __           _      _____     _
#      |  \/  |_   _ ___(_) ___|  ___|_ _| | _____ ____
#      | |\/| | | | / __| |/ __| |_ / _` | |/ / _ \_  /
#      | |  | | |_| \__ \ | (__|  _| (_| |   <  __// /
# svhl/|_|  |_|\__,_|___/_|\___|_|  \__,_|_|\_\___/___|

import os
import re
import json
import shlex
import subprocess
import requests
import time
from requests.exceptions import RequestException
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TPE2, TDRC, TRCK, TCON

HEADERS = {
	"User-Agent": "MusicFakez/1.0 (https://github.com/svhl/musicfakez)"
}

# IMPORTANT
# Set the location to save the songs to
location = os.path.expanduser("~/Music/Fakez")

if not location:
	print("Download path not provided! Please set the location variable.")
	exit(1)

def mb_get(url, params):
	for attempt in range(4):
		try:
			return requests.get(
				url,
				params=params,
				headers=HEADERS,
				timeout=15
			)
		
		except RequestException as e:
			if attempt == 3:
				print(f"Network error: {e}")
				return None
			time.sleep(2 * (attempt + 1))

def search(release_name):
	url = f"https://musicbrainz.org/ws/2/release/"
	params = {
		"query": release_name,
		"fmt": "json",
		"limit": 1
	}

	r = mb_get(url, params)

	if not r:
		return None
	
	r.raise_for_status()
	data = r.json()

	if not data.get("releases"):
		return None

	return data["releases"][0]["id"]

def get_tracks(release_id):
	url = f"https://musicbrainz.org/ws/2/release/{release_id}"
	params = {
		"inc": "recordings artists tags",
		"fmt": "json"
	}

	r = mb_get(url, params)

	if not r:
		return {}
	
	r.raise_for_status()
	return r.json()

def safe_name(name):
	return re.sub(r'[\\/:*?"<>|]', "_", name)

def make_mp3(path, length_ms):
	seconds = max(0, (length_ms or 0) / 1000)
	# Create silent track
	cmd = f'ffmpeg -loglevel quiet -y -f lavfi -i anullsrc=r=44100:cl=stereo -t {seconds} -q:a 9 -acodec libmp3lame "{path}"'
	subprocess.run(shlex.split(cmd), check=True)

def write_tags(path, title, artist, album, album_artist, year, genre, track_no):
	tags = ID3()

	# These are ID3 tags for metadata
	tags.add(TIT2(encoding=3, text=title))
	tags.add(TPE1(encoding=3, text=artist))
	tags.add(TALB(encoding=3, text=album))
	tags.add(TPE2(encoding=3, text=album_artist))

	if year:
		tags.add(TDRC(encoding=3, text=str(year)))
	if track_no:
		tags.add(TRCK(encoding=3, text=str(track_no)))
	if genre:
		tags.add(TCON(encoding=3, text=genre))

	tags.save(path)

def build_files(data):
	album = data.get("title") or "Unknown Album"

	album_artist = "Unknown Artist"
	if data.get("artist-credit"):
		album_artist = data["artist-credit"][0]["name"]

	year = (data.get("date") or "")[:4]

	genre = None
	if data.get("tags"):
		genre = data["tags"][0]["name"]

	album_dir = os.path.join(location, safe_name(album))
	os.makedirs(album_dir, exist_ok=True)

	for medium in data.get("media", []):
		for track in medium.get("tracks", []):
			title = track.get("title") or "Unknown"
			length_ms = track.get("length")
			track_no = track.get("number") or ""

			artist = album_artist
			if track.get("artist-credit"):
				artist = track["artist-credit"][0]["name"]

			filename = safe_name(title) + ".mp3"
			path = os.path.join(album_dir, filename)

			if os.path.exists(path):
				print(f"Already exists, skipping: {filename}")
				continue

			make_mp3(path, length_ms)
			write_tags(
				path,
				title,
				artist,
				album,
				album_artist,
				year,
				genre,
				track_no
			)

			print(f"Created: {filename}")

if __name__ == "__main__":
	release_name = input("Enter album name: ").strip()

	release_id = search(release_name)
	if not release_id:
		print("Album not found :(")

	else:
		data = get_tracks(release_id)
		build_files(data)
		print("Done :)")
