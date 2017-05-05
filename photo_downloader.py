import requests
import os
from bs4 import BeautifulSoup


'''
The Mangachaeleon url is made up of 3 parts
i=blank is the id for the manga you want to read. Example: i=4e70ea6ac092255ef7006a52 is the id for Attack On Titan
c=blank is the id for the chapter you want to read. Example: c=55a2acb1719a165e76360f6a is the first chapter in the Attack on Titan manga
cp=blank is the page number of the chapter. If not included it will go to page 0 (first page), it must be a number and if it is greater than the number of pages in that chapter it will return a normal page but no image for that page
a valid URL will look like this:http://mangachameleon.com/?i=BLANK&c=BLANK&cp=BLANK
The 3 options can be switched around but the first option that comes after the .com/ must be a ? and not a &
'''
# First_chapter_url can be any full url. Must include an i and c var in the url
first_chapter_url = "NEEDS_TO_BE_UPDATED!!!!!!!!!"

# Base url need to be in this format
# http://mangachameleon.com/?i=WHAT_EVER_THE_i_Is
base_url = "NEEDS_TO_BE_UPDATED!!!!!!!!!"
chapternames = []
chapterid = []

# Downloads the first page to get the id's from
r = requests.get(first_chapter_url)
# Sets up the BeautifulSoup object
soup = BeautifulSoup(r.content, "html.parser")

# Finds all of the id's of the chapters and the names of the chapters
for link in soup.find_all("option"):
    if (link.get('value') and len(link.get('value')) > 4):
        chapterid.append(link.get('value'))
        # print(linkz.get('value'))
        chapternames.append(link.get_text())
        # print(linkz.get_text())

# Declares some vars for looping
i = 0
pages = 0

#Will remove any characters that can not be saved in the file system such as : or /
def clean_string(string):
    r_string = string
    r_string = r_string.replace("?", "")
    r_string = r_string.replace("\\", "")
    r_string = r_string.replace("|", "")
    r_string = r_string.replace("/", "")
    r_string = r_string.replace(":", "")
    r_string = r_string.replace("*", "")
    r_string = r_string.replace("\"", "")
    r_string = r_string.replace(">", "")
    r_string = r_string.replace("<", "")
    return r_string


# Will start looping the chapters
for chapter in chapterid:

    # Prints for debugging
    # print(chapter)
    print(chapternames[i])

    # Downloads the first page of each chapter to count how many pages there are in each chapter
    r = requests.get(base_url + "&c=" + chapter)
    #Makes a new soup object
    soup = BeautifulSoup(r.content, "html.parser")
    #Will save the director name as the chapter name but cleaned up for windows
    dir_name = clean_string(chapternames[i])
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # Will loop through and get the total number of pages per chapter and store it as int pages
    for link in soup.find_all("option"):
        if (link.get('value') and len(link.get('value')) < 5):
            pages = pages + 1

    # Debug prints
    #print(dir_name)
    #print(dir_name[:-1])

    # Checks if the last character in the title name is a space. Windows will auto delete the last character if it is a space and will result in python not being able to find the dir
    if dir_name[-1:] == " ":
        #Will change dir_name and remove the space
        dir_name = dir_name[:-1]
        text_file = open(dir_name + "\\" + "links.txt", "w")

    #If it doesn't end with a space then carry on as normal
    else:
        text_file = open(dir_name + "\\" + "links.txt", "w")
    text_string = " "
    # loops through each <option> tag and sees if its an id, which the length is much longer, or a page number, less than 5 just to be safe
    for link in soup.find_all("option"):
        if (link.get('value') and len(link.get('value')) < 5):

            # Prints the page number from highest to lowest
            # print(link.get('value'))

            # Will grab the current page number
            page_number = link.get('value')
            # Will make a new request based off of the base URL the current chapter id and the current page number as grabbed from above
            new_r = requests.get(base_url + "&c=" + chapter + "&cp=" + page_number)
            # Makes a new soup object for the current page
            new_soup = BeautifulSoup(new_r.content, "html.parser")

            # Will loop through the current page and find all <img> tags
            for img in new_soup.find_all("img"):
                # If the image tag has cdn.mangaeden.com in it it will know that is the link to the manga image
                if ("cdn.mangaeden.com" in img.get("src")):
                    # print(img.get("src"))
                    img_link = img.get("src")
                    # Writes the link to the file so it will go from First page to last page
                    text_string = str(img_link) + "\n" + text_string

                    # makes the full path of the image to be saved at
                    full_file_path = os.path.join(dir_name, str(pages) + img_link[-4:])

                    # Will open a new file for the image to be written
                    image_file = open(full_file_path, "wb")
                    # Dl's the image
                    img_r = requests.get(img_link)
                    # Writes the image
                    image_file.write(img_r.content)
                    # Closes the file
                    image_file.close()
                    # Debug print
                    # print("Finished downloading " + dir_name + " Page " + str(pages))

                    # Will subtract one off the page count since it loops threw from the highest page to 0 (easyer to do)
                    pages = pages - 1

    # writes the image link to the text file
    text_file.write(text_string)
    # Closes the text file of links
    text_file.close()
    # Prints every time a chapter is fully looped through
    print("Finished downloading chapter \"" + dir_name + "\"")
    # Will add 1 to i which keeps track of what chapter it is working on
    i = i + 1

#Prints all done :P
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

How it works:
    Downloads 1 page from the manga that the user provides
    Loops through that pages and gets all the chapter id's and chapter names
        Downloads the a chapter (stored from most recent to oldest) and find out how many pages there are
        Cleans up the chapter name (removes chars that can't be used as a folder name) and makes a new directory if one is not made already
        Stores the number of pages as int pages
            Loops through the pages and searches for the string "cdn.mangaeden.com" as the src in all the <img> tags on the page
            Downloads the img from the page and names it by the page number and last 4 of the file name (.png or .jpg)
            Closes the file and subtracts 1 from pages
            Repeates until all pages for the chapter are done downloading
        Subtracts 1 from int i which keeps track of what chapter is downloading (naming purpose only)
    Prints "All done" when finished

'''
