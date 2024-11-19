# MusiToSpotify
Converts Musi playlist to Spotify playlist.

This Python script converts a playlist from the Musi app to a Spotify playlist. It fetches songs from a given Musi playlist link, searches for the corresponding tracks on Spotify, and creates a new Spotify playlist with the same songs in the same order. It also logs any songs that could not be found on Spotify.

## Features
- Scrape songs from a Musi playlist link.
- Search for songs on Spotify using the Spotify Web API.
- Create a new Spotify playlist and populate it with the found songs.
- Log any songs that couldn't be matched on Spotify.

## Requirements
1. **Spotify Developer Account**: You need a Spotify Developer account and a registered application to obtain your `CLIENT_ID` and `CLIENT_SECRET`.
2. **Python 3.9+**: Ensure you have Python installed on your system.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/musi-to-spotify.git
   cd musi-to-spotify
