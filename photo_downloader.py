# Library Requirements
import requests
import urllib.request
import os
import tkinter
from bs4 import BeautifulSoup
from PIL import Image

# Global Variable Definitions
base_url = "https://manganelo.com/chapter/yovbxa13526492"
first_chapter_url = base_url + "/chapter_1"
chapternames = []
chapterid = []
r = requests.get("http://manganelo.com")
soup = BeautifulSoup(r.content, "html.parser")
i = 0
pages = 0
dir_name = ""

# tkinter setup
root = tkinter.Tk()
tf = tkinter.Frame(root)
bf = tkinter.Frame(root)
label_1 = tkinter.Label(bf, text="Enter a URL like the one above then hit download")
label_2 = tkinter.Label(bf, text="Only works with Mangakakalot")
label_3 = tkinter.Label(bf, text="GUI will freeze when downloading, this is normal")
urlentry = tkinter.Entry(tf, width=50)
urlentry.delete(0, tkinter.END)
urlentry.insert(0, "https://mangakakalot.com/chapter/steinsgate")
root.title("Manga Downloader")
failedloops = 0

# Build the request opener to prevent download requests from getting blocked
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)


# Finds all of the id's of the chapters and the names of the chapters
def chapter_name():
    for link in soup.find_all("option"):
        print(link)
        if (
                link.get_text() != "Fullsize" and link.get_text() != "Large" and link.get_text() != "Medium" and link.get_text() != "Small" and link.get_text() not in chapternames):
            chapterid.append(link.get('data-c'))
            print("Printing link.get(data-c)")
            print(link.get('data-c'))
            # print(linkz.get('value'))
            chapternames.append(link.get_text())
            print("Printing link.get_text")
            print((link.get_text()))
            # print(linkz.get_text())


# Will remove any characters that can not be saved in the file system such as : or /
def clean_string(string):
    valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    for x in string:
        if x not in valid_chars:
            string = string.replace(x, '')
    return string


def setup():
    # Downloads the first page to get the id's from them
    global r
    global base_url
    global soup

    base_url = urlentry.get()
    r = requests.get(base_url + "/chapter_1")
    soup = BeautifulSoup(r.content, "html.parser")
    print("Done packing")
    chapter_name()
    dl_loop()


def dl_loop():
    global i
    global pages
    global dir_name
    for chapter in chapterid:

        print(chapternames[i] + " CHAPTER ID")

        # Downloads the first page of each chapter to count how many pages there are in each chapter

        # Will save the director name as the chapter name but cleaned up for windows
        dir_name = clean_string(chapternames[i])

        if not os.path.exists(dir_name):
            print(dir_name)
            os.makedirs(dir_name)

        # Checks if the last character in the title name is a space. Windows will auto delete the last character if it is a space and will result in python not being able to find the dir
        if dir_name[-1:] == " ":
            # Will change dir_name and remove the space
            dir_name = dir_name[:-1]

        text_string = " "
        # loops through each <option> tag and sees if its an id, which the length is much longer, or a page number, less than 5 just to be safe

        new_r = requests.get(base_url + "/chapter_" + chapter)
        # Makes a new soup object for the current page
        new_soup = BeautifulSoup(new_r.content, "html.parser")

        pages = 1
        failedloops = 0
        for img in new_soup.find_all("img"):
            # print("TEST looping through image options")
            # If the image tag has cdn.mangaeden.com in it it will know that is the link to the manga image
            looping = True
            while looping:
                if (("/chapter" in img.get("src"))):
                    ##print(img.get("src"))
                    img_link = img.get("src")
                    print(img.get("src"))
                    # Writes the link to the file so it will go from First page to last page
                    text_string = str(img_link) + "\n" + text_string

                    # makes the full path of the image to be saved at
                    full_file_path = os.path.join(dir_name, str(pages) + img_link[-4:])

                    print("TEST Wrote image")
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
                        print(e)
                        pass
                else:

                    looping = False

                # Page might fail, had a couple times when their page was giving php errors and refreshing it would give me the correct page
                if (pages == 1 and failedloops < 3):
                    failedloops+=1
                    new_r = requests.get(base_url + "/chapter_" + chapter)
                    looping = True

    i += 1
    print("Finished downloading chapter \"" + dir_name + "\"")


def main():
    button1 = tkinter.Button(tf, text="Download", width=45, command=setup)

    bf.pack(side=tkinter.BOTTOM)
    tf.pack()
    urlentry.pack()
    label_1.pack()
    label_2.pack()
    label_3.pack()
    button1.pack()
    root.mainloop()

    print("All done")


# Run main function
if __name__ == "__main__":
    main()
