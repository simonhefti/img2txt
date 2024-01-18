# tf.py
# (c) 2023-2024 Simon Hefti
# detect good words in given text

import re
import nostril
import ftfy
import fold_to_ascii


def get_words(txt):
    words = [w for w in re.findall(r"\b\w*\b", txt) if len(w) > 0]
    return words

def is_nonsense(word):
    res = True
    try:
        res = nostril.nonsense(word)
    except:
        pass
    return res

def good_words(words):
    res = []
    if words is None or len(words) == 0:
        return res
    words_good = [word for word in words if not is_nonsense(word)]
    res = list(set(words_good))
    
    return res

def ascii_fold(zin):

    res = str(zin)

    tpl : tuple = (
        ( 'ü' , "ue" ) , ( 'Ü' , "Ue" ) , ( 'ä'  , "ae" ) , ( 'Ä' , "Ae" ) , ( "ö" , "oe" ) ,
        ( 'Ö' , "Oe" ) , ( 'ß' , "ss" )
    )

    for item1 , item2 in tpl :
        res = res.replace( item1 , item2 )

    return res


def tf(txt):

    if txt is None or len(txt) < 1:
        return [], [], txt
    
    txt = ascii_fold(txt)
    txt = fold_to_ascii.fold(txt)
    txt = ftfy.fix_text(txt)

    words = get_words(txt)

    wg = good_words(words)

    return words, wg, txt
