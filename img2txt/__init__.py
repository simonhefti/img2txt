"""
img2txt.

Extract text from PDF or image.
"""

__version__ = "0.1.0"
__author__ = 'Simon Hefti'
__credits__ = 'Simon Hefti'

import pytesseract
import PIL
import lingua

import img2txt.tf as tf

lang_dect  = lingua.LanguageDetectorBuilder.from_all_languages().build()

def to_tesseract_language_code(lingua_language):
    language_map = {
        lingua.Language.ENGLISH: "eng",
        lingua.Language.FRENCH: "fra",
        lingua.Language.ITALIAN: "ita",
        lingua.Language.GERMAN: "deu",
        lingua.Language.GREEK: "grek",
        None: "eng"
    }
    return language_map.get(lingua_language, "eng")

def rotate_and_text_features(pil_img, lang, angle):

    img = pil_img
    if angle != 0:
        img = pil_img.rotate(angle, PIL.Image.NEAREST, expand = 1)

    txt = pytesseract.image_to_string(img, lang=lang)
    wa, wb, wg = tf.tf(txt)

    return wa, wb, wg, txt

# def word_ratios(wa, wb, wg):

#     print(f"wa {','.join(wa)}")
#     print(f"wb {','.join(wb)}")
#     print(f"wg {','.join(wg)}")

#     if len(wa) < 1:
#         wgwa = 0
#         wbwa = 1
#     else:
#         wgwa = len(wg) / float(len(wa))
#         wbwa = len(wb) / float(len(wa))

#     f1 = wgwa * wbwa

#     print(f"DBG   wgwa {wgwa:.2f} wbwa {wbwa:.2f} f1 {f1:.2f}")

#     return wgwa, wbwa, f1

def is_better(wgwa1, wbwa1, wgwa2, wbwa2):

    res = False
    if wgwa2 >= wgwa1 and wbwa2 <= wbwa1:
        res = True
    return res

def img2txt(pil_img, wb_wa_th=0.1):

    txt = pytesseract.image_to_string(pil_img, lang="eng")
    wab = tf.word_analysis(txt) # best we know so far

    if len(wab.words) < 1:
         # no words detected
         print(f"WAR no words detected")
         return ""

    language = lang_dect.detect_language_of(txt)
    t_lang = to_tesseract_language_code(language)
    print(f"DBG t_lang {t_lang}")

    if "eng" != t_lang:
        tx2 = pytesseract.image_to_string(pil_img, lang=t_lang)
        wa2 = tf.word_analysis(tx2)

        if wa2.is_better(wab):
            # adopt proposed language
            txt = tx2
            wab = wa2
        else:
            t_lang = "eng" # stay with default

    # try rotations
    for angle in [270, 90, 180]:
        img = pil_img.rotate(angle, PIL.Image.NEAREST, expand = 1)
        tx3 = pytesseract.image_to_string(img, lang=t_lang)
        wa3 = tf.word_analysis(tx3)

        if wa3.is_better(wab):
            print(f"improved with angle {angle}")
            # adopt angle
            txt = tx3
            wab = wa3
        
    return txt
