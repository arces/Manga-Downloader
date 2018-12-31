import requests
import os
from bs4 import BeautifulSoup

from tkinter import *
from PIL import Image

base_url = "https://mangakakalot.com/chapter/steinsgate"

first_chapter_url = base_url + "/chapter_1"
chapternames = []
chapterid = []
r = requests.get("http://mangakakalot.com")
soup = BeautifulSoup(r.content, "html.parser")
i = 0
pages = 0
dir_name = ""
root = Tk()
tf = Frame(root)
bf = Frame(root)
label_1 = Label(bf, text="Enter a URL like the one above then hit download")
label_2 = Label(bf, text="Only works with Mangakakalot")
label_3 = Label(bf, text="GUI will freeze when downloading, this is normal")
urlentry = Entry(tf, width=50)
urlentry.delete(0, END)
urlentry.insert(0, "https://mangakakalot.com/chapter/steinsgate")
root.title("Manga Downloader")


# Finds all of the id's of the chapters and the names of the chapters
def chapter_name():
    for link in soup.find_all("option"):
        # print(link)
        if (link.get(
                'value') and link.get_text() != "Fullsize" and link.get_text() != "Large" and link.get_text() != "Medium" and link.get_text() != "Small" and link.get_text() not in chapternames):
            chapterid.append(link.get('value'))
            ##print(link.get('value'))
            # print(linkz.get('value'))
            chapternames.append(link.get_text())
            ##print((link.get_text()))
            # print(linkz.get_text())


# Will remove any characters that can not be saved in the file system such as : or /
def clean_string(string):
    r_string = string
    r_string = r_string.replace("...", "")
    r_string = r_string.replace("?", "")
    r_string = r_string.replace("\\", "")
    r_string = r_string.replace("|", "")
    r_string = r_string.replace("/", "")
    r_string = r_string.replace(":", "")
    r_string = r_string.replace("*", "")
    r_string = r_string.replace("\"", "")
    r_string = r_string.replace(">", "")
    r_string = r_string.replace("<", "")
    r_string = r_string.replace("=", "")
    r_string = r_string.replace("[", "")
    r_string = r_string.replace("]", "")
    r_string = r_string.replace(";", "")
    r_string = r_string.replace("'", "")
    return r_string


## print (chapterid)

# Will start looping the chapters


def main_dl():
    global i
    global pages
    global dir_name
    for chapter in chapterid:

        ##print(chapternames[i] + " CHAPTER ID")

        # Downloads the first page of each chapter to count how many pages there are in each chapter

        # Will save the director name as the chapter name but cleaned up for windows
        dir_name = clean_string(chapternames[i])
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # Checks if the last character in the title name is a space. Windows will auto delete the last character if it is a space and will result in python not being able to find the dir
        if dir_name[-1:] == " ":
            # Will change dir_name and remove the space
            dir_name = dir_name[:-1]
            text_file = open(dir_name + "\\" + "links.txt", "w")

        # If it doesn't end with a space then carry on as normal
        else:
            text_file = open(dir_name + "\\" + "links.txt", "w")
        text_string = " "
        # loops through each <option> tag and sees if its an id, which the length is much longer, or a page number, less than 5 just to be safe

        new_r = requests.get(base_url + "/chapter_" + chapter)
        # Makes a new soup object for the current page
        new_soup = BeautifulSoup(new_r.content, "html.parser")

        pages = 1
        for img in new_soup.find_all("img"):
            ## print("TEST looping through image options")
            # If the image tag has cdn.mangaeden.com in it it will know that is the link to the manga image
            looping = True
            while looping:
                if (("mgimgcdn.com" in img.get("src")) or ("mgicdn.com" in img.get("src")) or (
                        "bp.blogspot.com" in img.get("src")) or ("s1.mkklcdnv2.com" in img.get("src")) or (
                        "s8.mkklcdn.com" in img.get("src")) or ("s7.mkklcdn.com" in img.get("src")) or (
                        "s6.mkklcdn.com" in img.get("src")) or (
                        "s5.mkklcdn.com" in img.get("src")) or (
                        "s4.mkklcdn.com" in img.get("src")) or (
                        "s3.mkklcdn.com" in img.get("src")) or (
                        "s2.mkklcdn.com" in img.get("src")) or (
                        "s1.mkklcdn.com" in img.get("src")) or (
                        "4.bp.blogspot.com" in img.get("src")) or (
                        "3.bp.blogspot.com" in img.get("src")) or (
                        "2.bp.blogspot.com" in img.get("src")) or (
                        "1.bp.blogspot.com" in img.get("src")) or (
                        "s2.mkklcdnv" in img.get("src")) or (
                        "s5.mkklcdnv" in img.get("src")) or (
                        "s3.mkklcdnv" in img.get("src")) or (
                        "s4.mkklcdnv" in img.get("src")) or (
                        "s1.mkklcdnv" in img.get("src"))
                        or ("s6.mkklcdnv" in img.get("src")) or (
                                "s7.mkklcdnv" in img.get("src"))
                        or ("s8.mkklcdnv" in img.get("src"))
                        or ("s9.mkklcdnv" in img.get("src"))):
                    ##print(img.get("src"))
                    img_link = img.get("src")
                    ## print(img.get("src"))
                    # Writes the link to the file so it will go from First page to last page
                    ## print("TEST About to write")
                    text_string = str(img_link) + "\n" + text_string
                    ## print("TEST Wrote")

                    # makes the full path of the image to be saved at
                    ## print("TEST About to write picture")

                    full_file_path = os.path.join(dir_name, str(pages) + img_link[-4:])

                    ## print("TEST Wrote image")
                    # Will open a new file for the image to be written
                    image_file = open(full_file_path, "wb")
                    # Dl's the image
                    img_r = requests.get(img_link)
                    # Writes the image
                    image_file.write(img_r.content)
                    image_file.close()
                    try:
                        # Very Important!!!!!!!!!! This will check the file to see if it downloaded properly
                        # It opens the image and sees if it is a valid image.
                        # If NOT then it will crash and keep looping and attempting to dl the image
                        # If it is valid it adds one to page and then exits the loop to the next page link
                        img = Image.open(full_file_path)
                        img.verify()
                        pages += 1
                        looping = False
                    except (IOError, SyntaxError) as e:
                        # Will crash here if the image is not valid and will NOT exit the loop
                        pass
                else:

                    looping = False

        i += 1
        print("Finished downloading chapter \"" + dir_name + "\"")


def setupz():
    # Downloads the first page to get the id's from them
    global r
    global base_url
    global soup

    base_url = urlentry.get()
    r = requests.get(base_url + "/chapter_1")
    soup = BeautifulSoup(r.content, "html.parser")
    ##print("Done packing")
    chapter_name()
    main_dl()


button1 = Button(tf, text="Download", width=45, command=setupz)

bf.pack(side=BOTTOM)
tf.pack()
urlentry.pack()
label_1.pack()
label_2.pack()
label_3.pack()
button1.pack()
root.mainloop()

print("All done")

'''
Sources:
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
http://www.thegeekstuff.com/2013/06/python-list/?utm_source=feedly
https://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
https://stackoverflow.com/questions/3559559/how-to-delete-a-character-from-a-string-using-python
http://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/functions.html
https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method
https://stackoverflow.com/questions/7983820/get-the-last-4-characters-of-a-string
https://opensource.com/article/17/2/python-tricks-artists
How it works:
    Downloads 1 page from the manga that the user provides
    Loops through that pages and gets all the chapter id's and chapter names
        Downloads the a chapter (stored from most recent to oldest) and find out how many pages there are
        Cleans up the chapter name (removes chars that can't be used as a folder name) and makes a new directory if one is not made already
        Stores the number of pages as int pages
            Loops through the pages and searches for the string "mgimgcdn.com" as the src in all the <img> tags on the page
            Downloads the img from the page and names it by the page number and last 4 of the file name (.png or .jpg)
            Closes the file and subtracts 1 from pages
            Repeates until all pages for the chapter are done downloading
        Subtracts 1 from int i which keeps track of what chapter is downloading (naming purpose only)
    Prints "All done" when finished
'''
