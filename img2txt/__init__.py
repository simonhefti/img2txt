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
    wa, wg, txt = tf.tf(txt)

    return wa, wg, txt

def img2txt(pil_img, wg_wa_th=0.33):

    wa, wg, txt = rotate_and_text_features(pil_img, "eng", 0)

    if len(wa) < 1:
         # no words detected
         return ""
    
    if len(wg) < 1:
         # no good words detected
         return ""

    if len(wg) / float(len(wa)) > wg_wa_th:
         # no further processing required
         print(f"DBG first threshold ({wg_wa_th}) met")
         return txt
    
    language = lang_dect.detect_language_of(txt)

    t_lang = to_tesseract_language_code(language)
    print(f"DBG t_lang {t_lang}")

    wg_bl = wg
    wa, wg, txt = rotate_and_text_features(pil_img, t_lang, 0)
    print(f"DBG t_lang {t_lang} wg {len(wg)} (baseline {len(wg_bl)})")

    if len(wg) / float(len(wa)) > wg_wa_th:
         print(f"DBG 2nd threshold ({wg_wa_th}) met")
         # no further processing required
         return txt
    
    # attempt rotation
    for angle in [90, 180, 270]:
        wa2, wg2, txt2 = rotate_and_text_features(pil_img, t_lang, angle)
        if wg2 > wg:
            print(f"DBG improved with rotation {angle}: {len(wg2)} vs {len(wg)}")
            return txt2
        
    return txt
