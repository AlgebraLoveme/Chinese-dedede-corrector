import re
import logging
import time
import argparse

from sentence_parser import JiebaParser, PkusegParser

global parser
global ignored_pos

def has_de(sentence:str):
    return '的' in sentence

def parse_de(sentence:str):
    '''
    Process one sentence and correct 的地得
    '''
    # if there is no occurrence of 的地得, return the sentence
    if not has_de(sentence):
        return sentence
    # otherwise, parse the sentence
    words = parser.cut(sentence)
    new_sentence = []
    last_pos, next_pos = None, None
    locked_id = -1 # indicate where de occurs; -1 means not locked
    for idx, (w, p) in enumerate(words):
        new_sentence.append(w)
        if not w in ['的']:
            if p in ignored_pos:
                continue
            if locked_id == -1:
                last_pos = p
            else:
                # if the next word is an adj followed by a noun, the center word is a noun; e.g., 制作的"大""电影"
                if p == "a" and idx+1 < len(words) and words[idx+1][1].startswith("n"):
                    p = "n"
                next_pos = p
        else:
            # e.g., 重要的(就)是什么
            if not (idx+1 < len(words) and "是" in words[idx+1][0]):
                locked_id = idx
                next_pos = None
            continue
        # if we are locked, check whether we can unlock
        if locked_id != -1 and last_pos and next_pos:
            # print("original:", new_sentence[locked_id])
            original = new_sentence[locked_id]
            if last_pos in ["a", "d"] and next_pos in ["v"]:
                new_sentence[locked_id] = '地'
            elif last_pos in ["v"] and next_pos in ["a"]:
                new_sentence[locked_id] = '得'
            elif next_pos in ["n", "nr", "nt", "nz", "vn", "ns"]:
                new_sentence[locked_id] = '的'
            new = new_sentence[locked_id]
            if original != new:
                logging.info(words)
                logging.info(f"Pos {idx} Corrected: {original} -> {new}")
            # print("proposed:", new_sentence[locked_id])
            # if no condition is matched, ignore this one (conservative)
            locked_id = -1
            last_pos, next_pos = None, None
    return "".join(new_sentence)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', required=True, type=str, help='File to process.')
    parser.add_argument('--savename', default=None, type=str, help='File to save.')
    parser.add_argument('--encoding', default="utf-8", type=str, help='Encoding of the file.')
    parser.add_argument('--parser_engine', default="pkuseg", type=str, choices=["pkuseg", "jieba"], help='Parser to use.')
    parser.add_argument('--verbose', action="store_true", help='Verbose mode.')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    filename = args.filename
    savename = args.savename if args.savename else filename + ".corrected"
    encoding = args.encoding
    parser_engine = args.parser_engine

    ignored_pos = ["m", "p", "u", "e", "q", "f"]

    if parser_engine == "jieba":
        parser = JiebaParser()
    elif parser_engine == "pkuseg":
        parser = PkusegParser()

    try:
        with open(filename, "r", encoding=encoding) as f:
            text = f.read()
    except UnicodeDecodeError as e:
        logging.error(f"Cannot decode {filename} with {encoding} encoding. Try other encodings.")
        exit(1)

    # split sentence-wise
    sb_marker = r"！ 。 ； ~ ， …… ： \n ？".split(" ") # sentence break marker

    t1 = time.time()

    logging.info("Splitting sentences...")
    marker_dict = {}
    for marker in sb_marker:
        count = text.count(marker)
        marker_dict[marker] = count
    logging.info(f"Sentence end marker statistics: {marker_dict}")

    sentences = re.split(fr"({'|'.join(sb_marker)})", text)

    corrected_sentences = [parse_de(sentence) for sentence in sentences]

    new_text = "".join(corrected_sentences)
    print("Saving to", savename)
    with open(savename, "w", encoding=encoding) as f:
        f.write(new_text)

    t2 = time.time()
    print(f"Process Time: {t2-t1:.1f}s.")