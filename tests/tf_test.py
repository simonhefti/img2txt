"""Tests for tf.py"""

import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
from img2txt import tf

import PIL
import pytesseract

class TfTest(unittest.TestCase):

    def test_is_nonsense_1(self):
        wa = tf.word_analysis("")
        self.assertFalse(wa.is_nonsense("Zuckerberg"))
        self.assertTrue(wa.is_nonsense("JO9JJa"))
        self.assertTrue(wa.is_nonsense("BSOU"))
        self.assertTrue(wa.is_nonsense("I9A0U"))
        self.assertTrue(wa.is_nonsense("ouUIOS"))
        self.assertTrue(wa.is_nonsense("d1IYMIUIOS"))

    def test_is_better_1(self):
        wa1 = tf.word_analysis("Wettrusten")
        wa2 = tf.word_analysis("Wettrüsten")
        print(wa1)
        print(wa2)
        self.assertFalse(wa1.is_better(wa2))

    def test_is_better_2(self):

        wa1 = wa2 = None

        with PIL.Image.open("tests/t3.png") as pil_img:
            txt = pytesseract.image_to_string(pil_img, lang="eng")
            wa1 = tf.word_analysis(txt)

            pil_img = pil_img.rotate(270, PIL.Image.NEAREST, expand = 1)
            txt = pytesseract.image_to_string(pil_img, lang="eng")
            wa2 = tf.word_analysis(txt)

        print(wa1)
        print(wa2)
        self.assertTrue(wa2.is_better(wa1))

    def test_is_better_3(self):

        wa1 = wa2 = None

        with PIL.Image.open("tests/t1.png") as pil_img:
            txt = pytesseract.image_to_string(pil_img, lang="eng")
            wa1 = tf.word_analysis(txt)

            txt = pytesseract.image_to_string(pil_img, lang="deu")
            wa2 = tf.word_analysis(txt)

        print(wa1)
        print(wa2)
        self.assertTrue(wa2.is_better(wa1))

    def test_wa1(self):
        txt = "Zuckerberg stellte am Mittwoch neue KI-Software vor."
        wa = tf.word_analysis(txt)
        self.assertEqual(txt, wa.txt)
        print(wa)
        self.assertEqual(0.5, wa.ratio_good)
        self.assertEqual(0, wa.ratio_bad)

    def test_wa2(self):
        txt = "JO9JJa BSOU YUIY SW edunos Ajdai"
        wa = tf.word_analysis(txt)
        self.assertEqual(txt, wa.txt)
        print(wa)
        self.assertEqual(1/6.0, wa.ratio_good)
        self.assertEqual(1/6.0, wa.ratio_bad)

if __name__ == "__main__":
    unittest.main()
