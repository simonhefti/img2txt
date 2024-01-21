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

    wa, wb, wg, txt = rotate_and_text_features(pil_img, "eng", 0)
    wgwa, wbwa, f1 = word_ratios(wa, wb, wg)

    if len(wa) < 1:
         # no words detected
         print(f"WAR no words detected")
         return ""

    language = lang_dect.detect_language_of(txt)
    t_lang = to_tesseract_language_code(language)
    print(f"DBG t_lang {t_lang}")

    if "eng" != t_lang:

        wa1 = wa, wg1 = wg, wb1 = wb, wgwa1 = wgwa, wbwa1 = wbwa
        wa, wb, wg, txt = rotate_and_text_features(pil_img, t_lang, 0)
        wgwa, wbwa, f1 = word_ratios(wa, wb, wg)

        if is_better(wgwa1, wbwa1, wgwa, wbwa):
            print(f"DBG improved with language")
        else:
            wa = wa1, wb = wb1, wg = wg1, 


        


    # print(f"wa {','.join(wa)}")
    # print(f"wb {','.join(wb)}")
    # print(f"wg {','.join(wb)}")

    # if len(wb) / float(len(wa)) < wb_wa_th:
    #      # no further processing required
    #      print(f"DBG first threshold ({wb_wa_th}) met")
    #      return txt
    
    # attempt rotation
    for angle in [90, 180, 270]:
        wa2, wb2, wg2, txt = rotate_and_text_features(pil_img, t_lang, angle)
        wgwa, wbwa, f1 = word_ratios(wa2, wb2, wg2)
        if len(wb2) < len(wb) and len(wg2) > len(wg):
            print(f"DBG improved with rotation {angle}: {len(wb2)} vs {len(wb)}")
            return txt
        
    return txt
