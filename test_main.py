#!/usr/bin/env python3
import unittest
import os
import main
import datetime


class TestExif(unittest.TestCase):

    def test_get_date(self):
        file_date = main.get_date("static/exif.jpg")
        assert type(file_date) == datetime.datetime

    def test_get_dirname(self):
        file_date = main.get_date("static/exif.jpg")
        creation_date = datetime.datetime.fromtimestamp(os.path.getmtime("static/exif.jpg"))
        dirname = main.get_dirname(file_date, "output", creation_date)
        assert dirname == "output/{}-{}".format(
            str(file_date.year),
            str(file_date.month).zfill(2)
            )

    def test_get_hash(self):
        file_hash = main.get_hash("static/exif.jpg")
        assert file_hash == "c3d98686223ad69ea29c811aaab35d343ff1ae9e"

    def test_get_filename(self):
        file_extension = os.path.splitext("static/exif.jpg")[1]
        file_date = main.get_date("static/exif.jpg")
        file_hash = main.get_hash("static/exif.jpg")
        creation_date = datetime.datetime.fromtimestamp(os.path.getmtime("static/exif.jpg"))
        file_name = main.get_filename(file_date, file_hash, file_extension, creation_date)
        assert file_name == "{}-{}{}".format(
            file_date.isoformat(),
            file_hash,
            file_extension
        )


class TestNonExif(unittest.TestCase):


    def test_get_dirname(self):
        file_date = main.get_date("static/urandom.jpg")
        creation_date = datetime.datetime.fromtimestamp(os.path.getmtime("static/urandom.jpg"))
        dirname = main.get_dirname(file_date, "output", creation_date)
        print(creation_date.year)
        assert dirname == "output/no-metadata/{}-{}".format(
            str(creation_date.year),
            str(creation_date.month).zfill(2)
        )

    def test_get_hash(self):
        file_hash = main.get_hash("static/urandom.jpg")
        assert file_hash == "1f95220e253908712fe34bf5ac568e28f403260d"

    def test_get_filename(self):
        file_extension = os.path.splitext("static/urandom.jpg")[1]
        file_date = main.get_date("static/urandom.jpg")
        file_hash = main.get_hash("static/urandom.jpg")
        creation_date = datetime.datetime.fromtimestamp(os.path.getmtime("static/urandom.jpg"))
        file_name = main.get_filename(file_date, file_hash, file_extension, creation_date)
        assert file_name == "{}-{}-{}-{}{}".format(
            str(creation_date.year),
            str(creation_date.month).zfill(2),
            str(creation_date.day).zfill(2),
            file_hash,
            file_extension
        )
       

if __name__ == "__main__":
    unittest.main()