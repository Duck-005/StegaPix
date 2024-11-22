# Steganography

This is a project that aims to understand the different types of steganography techniques.

Some include hiding the data in .wav formats or audio files, or hiding it in the metadata of the file or some obscure method which only the person making the file knows.

[Wikipedia](https://en.wikipedia.org/wiki/Steganography) <br>
[NumberPhile YT video](https://www.youtube.com/watch?v=TWEXCYQKyDc)

## Contents
1. [Least Significant Bit (LSB) manipulation](#LSB_Manipulation)

## LSB_Manipulation
This is a method in which the last bits of the rgb pixels is manipulated to store the bits of the message or image to be hidden.

The message can be encrypted before encoding it in the image, thus no one who doesn't know about it can decode it.

for ex. if a pixel has values: 
> (233, 21, 89) <br>

converting to binary it is:

> (1110 1001, 0001 0101, 0101 1001)

Same with the message, `ha` in binary is `01101000 01100001`
Now each bit of the message replaces the LSB of the pixel values. Thus for encoding the first 3 bits of the message, we need one pixel.

New pixel value becomes `(1110100"0", 0001010"1", 0101100"1")`
This is repeated until all the bits are encoded.

```
Also this particular method also encodes the length of the message in the same way in the first 8 LSBs.
Thus a message of size 32 bytes (2^8 / 8) can be hidden inside.
```
In  the same way any file can be hidden provided the base image is big enough. 

Original Image   |  Modified Image
:---------------:|:---------------:
![](kat03.png)   |  ![](output.png)

As we can see no visible change is seen by the naked eye since the shades may differ by one bit. Which is too small to notice.

### IMPORTANT

> Use a lossless saving format like png, bmp, gif to ensure that the message is not corrupted by the lossy compression. <br>
> jpeg, webp, HEIC, AVIF, TIFF are all lossy encoding formats.