import music21
import glob
import os
import json
import tqdm
import sys, getopt
from RepetitionsExpander import remove_repetitions

class lyric_extr:
    def __init__(self, s):
        self.score = music21.converter.parse(s)
        repeat_elements = remove_repetitions.get_repeat_elements(self.score, v = False)
        self.score = remove_repetitions.expand_score_repetitions(self.score, repeat_elements)

    def get_lyrics(self):
        return music21.search.lyrics.LyricSearcher(self.score).indexText
        

if __name__ == "__main__":
    try:
      _, args = getopt.getopt(sys.argv[1:], '')
      folder = args[0]
    except getopt.GetoptError:
        print('lyrics_extractor.py "xmls folder"')
        sys.exit(2)
    name_lyrics = {}
    for s in tqdm.tqdm(glob.glob(os.path.join(folder, '*.xml'))):
        text = lyric_extr(s).get_lyrics()
        xml_name = os.path.basename(s[0:-4])
        name_lyrics[xml_name] = text
    with open(os.path.join(os.getcwd(), 'score_lyrics.json'), 'w', encoding='utf-8') as json_file:
        json.dump(name_lyrics, json_file, indent=4, sort_keys=True, ensure_ascii=False)