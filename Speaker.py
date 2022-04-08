import os
import shutil

files = os.listdir()
curr = os.getcwd()
pdflst = list()
imglst = list()

for file in files:
    if ".pdf" in file:
        pdflst.append(file)
    if ".jpg" in file:
        imglst.append(file)

for file in pdflst:
    if os.path.isfile("./PDFs/" + file):
        t=0
        k=0
        while t==0:
            k+=1
            if os.path.isfile("./PDFs/" + file[:-4]+str(k)+file[-4:]):
                continue
            shutil.move("./"+file, "./PDFs/"+file[:-4]+str(k)+file[-4:])
            t=1
    else:
        shutil.move("./"+file, "./PDFs/",file)


for file in imglst:
    if os.path.isfile("./Images/" + file):
        t=0
        k=0
        while t==0:
            k+=1
            if os.path.isfile("./Images/" + file[:-4]+str(k)+file[-4:]):
                continue
            shutil.move("./"+file, "./Images/"+file[:-4]+str(k)+file[-4:])
            t=1
    else:
        shutil.move("./"+file, "./Images/", file)
