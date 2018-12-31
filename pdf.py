from fpdf import FPDF
import os
import sys

folders = []
chapters = []
images = []
errors = []
num_errors = 0
folder_name = ""

dir_path = os.path.dirname(os.path.realpath(__file__))


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


folders = (get_immediate_subdirectories(os.getcwd()))
#Debug print
#print(folders)
#print("these are the folders ^")
for f in folders:
    if (f[:2] == "Ch" or f[:3] =='vol' or f[:2] == "ch"):
        images = []
        image_names = []
        images = os.listdir(os.path.join(os.getcwd() + "\\" + f))
        #Debug prints
        #print(images)
        #print("These are the images")
        #print(f)
        for img in images:
            image_names.append(img[:-4])
        i = 1
        #print(image_names)
        pdf = FPDF()
        pdf.add_page()
        #print(images.__len__())
        while (i < images.__len__()):
            try:
                pdf.set_font('Arial', 'B', 16)
                #print(i)
                full_image_name = str(images[image_names.index(str(i))])
                image_path = os.path.join(os.getcwd() + "\\" + f + "\\" + full_image_name)
                pdf.add_page()
                #Debug print
                #print("adding image "+full_image_name)
                pdf.image(image_path, x=0, y=0, w=190, )

            except:
                #print("Unexpected error:", sys.exc_info()[0])
                num_errors=num_errors+1
                full_image_name = str(i);
                #errors.append(full_image_name + " from "+f)
                #pdf.cell(40, 10, "Error adding image " + full_image_name + " from " + f)
                #print("Error adding image " + full_image_name + " from " + f)
            i = i + 1
        try:
            pdf.close()
            pdf.output(f + ".pdf", "F")
        except:
            print("Error closing/Saving PDF :'(")

if num_errors>0:
    print("Finished with "+str(num_errors))
else:
    print("Finished with no errors :D")
