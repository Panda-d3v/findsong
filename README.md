# Findsong

Have you ever wanted to find a song knowing only its lyrics ? Or to find the lyrics of a song but you only know the chorus ?

Stop right there, because this tool is for you!

## The CLI Command
This tool is for terminal use only, and is meant to stay like this. Who needs a UI when you have ASCII ?

## Install
- Download the repo
- Put it somewhere convenient.
- Get an Genius API key, and store it in the same environment calling it `GENIUS_ACCESS_TOKEN` (in your .zshrc for example)
- Execute the code `python3 findsong.py "..."` with the lyrics you want to look instead of ...
- create an alias in your .zshrc for example, so you can type `findsong "..."`

## What it actually does
- Checks whether you can access the Genius website ( i.e. online or offline)
- Checks if you have cached the lyrics on your device
- Finds the best match according to Genius
- Downloads the lyrics of the first result that Genius gave back
- If something else than the first result is selected, caches the lyrics too

## ⚠️ Disclaimer
This tool is intended for **personal, educational, or research use only**.
While the source code is provided under the MIT License, users are responsible for complying with the [Genius API Terms of Use](https://genius.com/static/terms) and applicable copyright laws.
This project uses the Genius API to fetch song lyrics for personal use.
Lyrics are copyrighted by their respective owners.
No lyrics are distributed with this code.
You must provide your own Genius API token.
