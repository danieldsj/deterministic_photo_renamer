![](https://github.com/danieldsj/photobomb/workflows/Test/badge.svg)

# Summary
Given an input and output directory, reads all of the image files on the input directory and attempts to create a hard link or copy in the output directory using a deterministic path and filename based on EXIF, file creation dates, and sha1 hash digests.