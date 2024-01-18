"""Tests for img2txt.py"""

import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
import img2txt
import PIL

class Img2TxtTest(unittest.TestCase):

    def test_png1(self):

        print("Hello")

        with PIL.Image.open("tests/t1.png") as pil_img:
            txt = img2txt.img2txt(pil_img)
            print(f"DBG txt: {txt}")
            self.assertTrue(len(txt) > 0)

            self.assertTrue("Zuckerberg stellte am Mittwoch neue" in txt)
            self.assertTrue("KI-Software vor. Zudem lancierte der" in txt)
            self.assertTrue("Meta-Chef auch eine neue VR-Brille" in txt)
            self.assertTrue("Der Chatbot Chat GPT trat ein Wettruesten der" in txt)

if __name__ == "__main__":
    unittest.main()
