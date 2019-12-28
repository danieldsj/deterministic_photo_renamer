![](https://github.com/danieldsj/photobomb/workflows/Test/badge.svg)

# Summary
Given an input and output directory, reads all of the image files on the input directory and attempts to create a hard link or copy in the output directory using a deterministic path and filename based on EXIF, file modify dates, and sha1 hash digests.

# Usage
Basic usage...
```
./main.py <input_directory> <output_directory>
```

# Features
* Extracts the EXIF information from image files.
* Generates a sha1 hash of the entire file.
* Uses EXIF date information and sha1 hash to generated a unique deterministic filename and path. Example: `output_directory/2019-12/2019-12-25T12:00:00-28b19c8a98ceb8da72fb01db2f4fb1cb03efe9c4.jpg`
* Reduces duplication in the output directory by skipping already existing files with the same name.
* Reduces IO by attempting to create hard links before creating copies of files.
* When copying files attempts to retain as much metadata as possible.
* Files with no EXIF information use the file modified date to generate a name.  Example: `output_directory/no-metadata/2019-12/2019-12-25-28b19c8a98ceb8da72fb01db2f4fb1cb03efe9c5.bin`