# Introduction

This is a tool to generate osu mania beatmap according to midi track and corresponding mp3 file.

This tool is in early development. 

# Usage

Install requirements

```
python3 -m pip install pretty_midi
```

Run

Note that `[file]` is the basename of mid and mp3 file.
`[file].mp3` and `[file].mid` should be both present.

```
python3 midi2osu.py [file]
```


# Reference

OSU file format
(https://osu.ppy.sh/wiki/en/osu%21_File_Formats/Osu_%28file_format%29)

