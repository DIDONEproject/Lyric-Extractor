# Lyric-Extractor
Script that extracts the lyrics from xml scores in JSON format.

## How to clone the project
```bash
> git clone --recurse-submodules git@github.com:DIDONEproject/Lyric-Extractor.git
```
## Limitations
This program uses music21 as background to process digital scores. It currently does not extract the second lyric in a note, indicated as restriction in the music21's documentation: http://web.mit.edu/music21/doc/moduleReference/moduleSearchLyrics.html
