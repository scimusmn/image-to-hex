usage: `img2hex.py [-h] [-w WIDTH] path`

turn images into sequences of hexadecimal values

positional arguments:
- `path` : path to image

optional arguments:
- `-h`, `--help` :  show this help message and exit
- `-w WIDTH`, `--width WIDTH` :  digits of output hex numbers. defaults to 2.
- `-i`, `--invert` :  bitflip resulting array (white is 1 and black is 0)
- `-r N`, `--reverse N` :  reverse array order, in blocks of N bytes
