# tf.py
# (c) 2023-2024 Simon Hefti
# detect good words in given text

import re
import nostril
import ftfy
import fold_to_ascii

class word_analysis():

    def __init__(self, txt):

        self.txt = txt

        words = [w for w in re.findall(r"\b\w*\b", txt) if len(w) > 0]
        wwreps = [w for w in words if re.match(r"\w*(\w)\1{2,}\w*", w)]
        wwnums = [w for w in words if re.match(r"[a-zA-Z]+\d+[a-zA-Z]+", w)]
        wgood  = self.good_words(words)

        self.words      = list(set(words))
        self.words_bad  = list(set(wwreps + wwnums))
        self.words_good = list(set(wgood))

        if len(self.words) < 1:
            wgwa = 0
            wbwa = 1
        else:
            wgwa = len(self.words_good) / float(len(self.words))
            wbwa = len(self.words_bad) / float(len(self.words))

        self.ratio_good = wgwa
        self.ratio_bad  = wbwa

        self.txt_fixed  = ftfy.fix_text(self.txt)
        self.txt_folded = self.ascii_fold(self.txt_fixed)

    def is_better(self, other):

        res = False

        if len(self.words) > 1 and len(other.words) > 1:
            print(f"DBG self and other have words")
            if self.ratio_good > other.ratio_good:
                print(f"DBG self ratio_good is higher")
                if self.ratio_bad <= other.ratio_bad:
                    print(f"DBG self ratio_bad is lower")
                    res = True
            else:
                print(f"DBG self ratio_good is worse: {self}")
        else:
            print(f"DBG not enough words")


        return res

    def __str__(self):
        return f'a: {len(self.words):3d} g: {len(self.words_good):3d} {self.ratio_good:.3f} b: {len(self.words_bad):3d} {self.ratio_bad:.3f} {",".join(self.words_good)} {",".join(self.words_bad)}'

    def count_capitals(self, word):
        return sum(1 for letter in word if letter.isupper())

    def get_words(self, txt):
        words = [w for w in re.findall(r"\b\w*\b", txt) if len(w) > 0]
        return words

    def is_nonsense(self, word):
        res = True
        try:
            res = nostril.nonsense(word)
        except:
            pass
        if res == False:
            cc = self.count_capitals(word)
            if cc > 1 and len(word) != cc:
                res = True
        return res

    def good_words(self, words):
        res = []
        if words is None or len(words) == 0:
            return res
        words_good = [word for word in words if not self.is_nonsense(word)]
        res = list(set(words_good))
        
        return res

    def ascii_fold(self, zin):

        res = str(zin)

        tpl : tuple = (
            ( 'ü' , "ue" ) , ( 'Ü' , "Ue" ) , ( 'ä'  , "ae" ) , ( 'Ä' , "Ae" ) , ( "ö" , "oe" ) ,
            ( 'Ö' , "Oe" ) , ( 'ß' , "ss" )
        )

        for item1 , item2 in tpl :
            res = res.replace( item1 , item2 )

        res = fold_to_ascii.fold(res)

        return res

# def tf(txt):

#     if txt is None or len(txt) < 1:
#         return [], []
    
#     words = [w for w in re.findall(r"\b\w*\b", txt) if len(w) > 0]
#     wwreps = [w for w in words if re.match(r"\w*(\w)\1{2,}\w*", w)]
#     wwnums = [w for w in words if re.match(r"[a-zA-Z]+\d+[a-zA-Z]+", w)]
#     wgood  = good_words(words)

#     w1 = list(set(words))
#     w2 = list(set(wwreps + wwnums))
#     w3 = list(set(wgood))

#     # txt = ascii_fold(txt)
#     # txt = fold_to_ascii.fold(txt)
#     # txt = ftfy.fix_text(txt)

#     # words = get_words(txt)

#     # wg = good_words(words)

#     # return words, wg, txt
#     return w1, w2, w3

# def tf1(txt):

#     if txt is None or len(txt) < 1:
#         return [], []
    
#     words = [w for w in re.findall(r"\b\w*\b", txt) if len(w) > 0]
#     wwreps = [w for w in words if re.match(r"\w*(\w)\1{2,}\w*", w)]
#     wwnums = [w for w in words if re.match(r"[a-zA-Z]+\d+[a-zA-Z]+", w)]
#     wgood  = good_words(words)

#     w1 = list(set(words))
#     w2 = list(set(wwreps + wwnums))
#     w3 = list(set(wgood))

#     # txt = ascii_fold(txt)
#     # txt = fold_to_ascii.fold(txt)
#     # txt = ftfy.fix_text(txt)

#     # words = get_words(txt)

#     # wg = good_words(words)

#     # return words, wg, txt
#     return w1, w2, w3
