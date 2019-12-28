#!/usr/bin/env python3

from PIL import Image, ExifTags
import os
import argparse
import logging
import sys
import hashlib
import shutil
from datetime import datetime

# Setup logging.
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt="%Y-%m-%dT%H:%M:%S%z"
)
stdout_handler.setFormatter(formatter)
log.addHandler(stdout_handler)


def get_date(file_path):
    log.info("Getting EXIF data.")
    try:
        image = Image.open(file_path)
        exif = dict(image.getexif())

        try:
            return datetime.strptime(exif.get(306), "%Y:%m:%d %H:%M:%S")
            log.info("Using EXIF DateTime data for file: {}".format(file_path))
        except TypeError as e:
            log.warning("Failed to get EXIF DateTime data. Error: {}".format(e))

        try:
            return datetime.strptime(exif.get(36867), "%Y:%m:%d %H:%M:%S")
            log.info("Using EXIF DateTimeOriginal data for file: {}".format(file_path))
        except TypeError as e:
            log.warning("Failed to get EXIF DateTimeOriginal data. Error: {}".format(e))

        try:
            return datetime.strptime(exif.get(36868), "%Y:%m:%d %H:%M:%S")
            log.info("Using EXIF DateTimeDigitized data for file: {}".format(file_path))
        except TypeError as e:
            log.warning("Failed to get EXIF DateTimeDigitized data. Error: {}".format(e))

        try:
            return datetime.fromtimestamp(os.path.getctime(file_path))
            log.info("Using file creation time for file: {}".format(file_path))
        except Exception as e:
            log.error("Failed to get file creation time. Error: {}".format(e))
            raise e

    except OSError as e:
        log.warning("The file {} does not appear to be a valid image file.".format(file_path))
        try:
            return datetime.fromtimestamp(os.path.getctime(file_path))
            log.info("Got creation time {} for file: {}".format(file_date, file_path))
        except Exception as e:
            log.error("Failed to get file creation time.")
            raise e

def get_hash(file_path):
    log.info("Getting a file hash.")
    hasher = hashlib.sha1()
    with open(file_path, 'rb') as file_handle:
        buffer = file_handle.read(65000)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = file_handle.read(65000)
    file_hash = hasher.hexdigest()
    log.info("Calculated hash of {} for file {}".format(file_hash, file_path))
    return file_hash

def get_filename(file_date, file_hash, file_extension):
    return "{}-{}{}".format(file_date.isoformat(), file_hash, file_extension)

def get_dirname(file_date, output_dir):
    return "{}/{}-{}".format(output_dir, str(file_date.year), str(file_date.month).zfill(2))

def is_directory_valid(directory):
    log.info('Validating input_dir argument.')
    if os.path.isdir(directory):
        return True
    else:
        return False

if __name__ == "__main__":
    log.info("Parsing arguments.")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_dir",
        nargs=1,
        help="The source location for photographs (PHOTOBOMB_INPUT_DIR).",
        default=os.environ.get('PHOTOBOMB_INPUT_DIR', None),
        type=str)
    parser.add_argument(
        "output_dir",
        nargs=1,
        help="The destination location for photographs \
            (PHOTOBOMB_OUTPUT_DIR).",
        default=os.environ.get('PHOTOBOMB_OUTPUT_DIR', None),
        type=str)
    arguments = parser.parse_args()
    input_dir = arguments.input_dir[0]
    output_dir = arguments.output_dir[0]
    assert os.path.isdir(input_dir)
    assert os.path.isdir(output_dir)

    log.info("Iterating over input directory.")
    for root, directory, files in os.walk(input_dir):

        log.info("Processing directory: {}".format(root))
        for f in files:
            file_path = os.path.join(root, f)
            log.info("Processing file: {}".format(file_path))
            file_extension = os.path.splitext(f)[1]
            file_date = get_date(file_path)
            file_hash = get_hash(file_path)
            destination_dir = get_dirname(file_date, output_dir)
            destination_file_name = get_filename(file_date, file_hash, file_extension)
            destination_file_path = os.path.join(destination_dir, destination_file_name)

            if not os.path.exists(destination_dir):
                log.info("Creating folder {}".format(destination_dir))
                os.mkdir(destination_dir)

            if not os.path.exists(destination_file_path):
                try:
                    log.info("Creating hard link from {} to {}".format(file_path, destination_file_path))
                    os.link(file_path, destination_file_path)
                except Exception as e:
                    log.warning("Failed to create link with error: {}".format(e))
                    log.info("Attempting to copy file instead.")
                    try:
                        log.info("Copying file {} to {}".format(file_path, destination_file_path))
                        shutil.copy2(file_path, destination_file_path)
                    except Exception as e:
                        log.error("Failed to copy file with error: {}".format(e))
                        exit(1)
            else:
                log.info("The file {} already exists in destination, skipping.".format(destination_file_path))
