#!/usr/bin/env python3
import unittest
import os
import main


class TestExif(unittest.TestCase):

    def test_get_date(self):
        file_date = main.get_date("static/exif.jpg")
        assert file_date.year == 2008
        assert file_date.month == 7
        assert file_date.day == 31
        assert file_date.hour == 10
        assert file_date.minute == 38
        assert file_date.second == 11

    def test_get_dirname(self):
        file_date = main.get_date("static/exif.jpg")
        dirname = main.get_dirname(file_date, "output")
        assert dirname == "output/2008-07"


    def test_get_hash(self):
        file_hash = main.get_hash("static/exif.jpg")
        assert file_hash == "c3d98686223ad69ea29c811aaab35d343ff1ae9e"

    def test_get_filename(self):
        file_extension = os.path.splitext("static/exif.jpg")[1]
        file_date = main.get_date("static/exif.jpg")
        file_hash = main.get_hash("static/exif.jpg")
        file_name = main.get_filename(file_date, file_hash, file_extension)
        assert file_name == "2008-07-31T10:38:11-c3d98686223ad69ea29c811aaab35d343ff1ae9e.jpg"


class TestNonExif(unittest.TestCase):

    def test_get_date(self):
        
        file_date = main.get_date("static/urandom.jpg")
        assert file_date.year == 2019
        assert file_date.month == 12
        assert file_date.day == 27
        assert file_date.hour == 23
        assert file_date.minute == 40
        assert file_date.second == 47


    def test_get_dirname(self):
        file_date = main.get_date("static/urandom.jpg")
        dirname = main.get_dirname(file_date, "output")
        assert dirname == "output/2019-12"


    def test_get_hash(self):
        file_hash = main.get_hash("static/urandom.jpg")
        assert file_hash == "1f95220e253908712fe34bf5ac568e28f403260d"

    def test_get_filename(self):
        file_extension = os.path.splitext("static/urandom.jpg")[1]
        file_date = main.get_date("static/urandom.jpg")
        file_hash = main.get_hash("static/urandom.jpg")
        file_name = main.get_filename(file_date, file_hash, file_extension)
        assert file_name == "2019-12-27T23:40:47.047263-1f95220e253908712fe34bf5ac568e28f403260d.jpg"
       

if __name__ == "__main__":
    unittest.main()