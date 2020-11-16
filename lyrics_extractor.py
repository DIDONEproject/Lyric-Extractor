import music21
import glob
import os
import json
import tqdm
import sys, getopt
from RepetitionsExpander import remove_repetitions
import concurrent.futures
from collections import ChainMap

class lyric_extr:
    def __init__(self, s):
        self.score = music21.converter.parse(s)
        repeat_elements = remove_repetitions.get_repeat_elements(self.score, v = False)
        self.score = remove_repetitions.expand_score_repetitions(self.score, repeat_elements)

    def get_lyrics(self):
        return music21.search.lyrics.LyricSearcher(self.score).indexText
        
def get_lyrics(s):
    n = os.path.basename(s[:-4])
    text = lyric_extr(s).get_lyrics()
    return {n:text}

if __name__ == "__main__":
    try:
      _, args = getopt.getopt(sys.argv[1:], '')
      if len(args) == 0:
          raise getopt.GetoptError('')
      folder = args[0]
    except getopt.GetoptError:
        print('lyrics_extractor.py "xmls folder"')
        sys.exit(2)

    executor = concurrent.futures.ProcessPoolExecutor()
    files = glob.glob(os.path.join(folder, '*.xml'))
    futures = [executor.submit(get_lyrics, s) for s in files]
    kwargs = {'total': len(files),'unit': 'it','unit_scale': True, 'leave': True}
    for _ in tqdm.tqdm(concurrent.futures.as_completed(futures), **kwargs):
        pass
    
    name_lyrics = dict(ChainMap(*[f._result for f in futures]))
    with open(os.path.join(os.getcwd(), 'score_lyrics.json'), 'w', encoding='utf-8') as json_file:
        json.dump(name_lyrics, json_file, indent=4, sort_keys=True, ensure_ascii=False)