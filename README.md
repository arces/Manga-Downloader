# Manga Downloader

This is a manga Downloader and PDF script that will download all the manga from any given url from [mangakakalot.com](http://mangakakalot.com).
The PDF script will add the completed files into a pdf


## You will need the following packages to get it working:

```
Python 3.x (Tested with 3.7-32)
pillow (Tested with  5.3.0)
requests (Tested with 2.21.0)
requests-html (Tested with 0.9.0)
beautifulsoup4 (Tested with 4.6.3)
FPDF (Tested with 1.7.2)
```


If you don't know how to install a python package then just type in
```
pip install *Python_Package_name_here*
```



## Usage:
Just run both of them from the command line.
 
<b>photodownloader.py</b> will make folders and download to those folders were it was called from.

1.Enter in a URL that is similar in format to the default one.


<b>pdf.py</b> will look for those folders and take the images from them and make a pdf based off of the options selected.

1. Check "First Page Blank?" if you would like the first page of each pdf to be a blank page (Useful to know when a new chapter might start)
2. Check "Combo" if you would like to add all the chapters into one large PDF called "combo.pdf" (<b>See known bugs below and FAQ</b>)

##Known Bugs:
1. Due to how the algorithm in the PDF.py file is, it will not recognize multiples of 10.
<b>Ex</b>: Out of the this list of chapters [1,2,3,4,5,6,7,8,9,10,11,12,13] it will put it in the following order 
 [1,10,11,12,13,2,3,4,5,6,7,8,9] if combo checkbox is selected.
 

## FAQ:
<b>The program is frozen, I can't click anything!</b> 
>Don't worry this is normal. Due to how the code is written, it will be frozen until it is finished.

<b>The images are not downloading! Why?</b>
>There might be a couple reasons. If the program is finished running and it missed images. This means that the list of domains for the image server is out of date. You will need to look at the HTML source code and see what the domain where the images are hosted. You can add that into the program (Look for all the if statements). <b>PLEASE LET ME KNOW IF YOU FIND DOMAINS THAT ARE NOT IN THE LIST</b>

<b>How can I help improve the program?</b>
>Report any bugs you find! You can also suggest features or even code them yourself and do a pull request!

<b>Ok... If combo is broken, how do I make them into one pdf?</b>
>Use a program like Adobe Acrobat or SodaPDF to merge/combine pdfs together. I do that and it works perfect for me.

