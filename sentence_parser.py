import jieba
import jieba.posseg as pseg
import pkuseg

class JiebaParser():
    def __init__(self) -> None:
        self.cutter = pseg
        jieba.enable_paddle()


    def cut(self, sentence:str):
        return [tuple(i) for i in list(self.cutter.cut(sentence, use_paddle=True))]

class PkusegParser():
    def __init__(self) -> None:
        self.cutter = pkuseg.pkuseg(postag=True)

    def cut(self, sentence:str):
        return self.cutter.cut(sentence)