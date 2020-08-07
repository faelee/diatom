import sys, os
import pandas as pd
import math
from PIL import Image

def imgOperation(opType, savePath, imageName, labelName, width, height):
    newImgName = ""
    opType = opType.lower ()
    labelPath = os.path.join (savePath, labelName)
    
    #flip or flop
    if opType == "flop" or opType == "flip":
        newImgName = str(opType) + "_"+ imageName 
        myCommand = "convert " + os.path.join (savePath, imageName) + " -" + str(opType) + " " + os.path.join (savePath, newImgName)
        newLabelPath = os.path.join (savePath, str(opType) + "_" + labelName)

        f = open(newLabelPath, "w+")
        with open(labelPath) as fp:
            lines = fp.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            valueList=(line.split())
            #print(valueList)

            #class_number, box_x_ratio, box_y_ratio, box_width_ratio, box_heigh_ratio
            (a,b,c,d,e) = valueList[0], valueList[1], valueList[2], valueList[3], valueList[4]
            if opType == "flop":
                f.write(a + " " + str(1- float(b)) + " " + c + " " + d + " " + e + "\n")
            else:
                f.write(a + " " + b + " " + str(1-float(c)) + " " + d + " " + e + "\n")
        f.close ()
        
        return myCommand, newImgName
        
    #scaling
    if opType[0:6] == "scale-":
        opType = opType[6:]
        newImgName =  "scl_" + str(opType) + "_" + imageName
        myCommand = "convert " + " -resize " + str(opType) + "%" + " " + os.path.join (savePath, imageName) + " " + os.path.join (savePath, newImgName)
        newLabelPath = "scl_" + str(opType) + "_" + labelName
        newLabelPath = os.path.join (savePath, newLabelPath)

        f = open(newLabelPath, "w+")
        with open(labelPath) as fp:
            lines = fp.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            valueList=(line.split())
            #print(valueList)
            (a,b,c,d,e) = valueList[0], valueList[1], valueList[2], valueList[3], valueList[4]
            f.write(a + " " + b + " " + c + " " + d + " " + e + "\n")
        f.close ()

        return myCommand, newImgName
  
    #rotating
    if opType[0:7] == "rotate-":
        opType = opType[7:]
        newImgName = "rot_" + str(opType) + "_deg_"+ imageName
        myCommand = "convert " + os.path.join (savePath, imageName) + " -rotate -" + str(opType) + " " + os.path.join (savePath, newImgName)
        newLabelPath = "rot_" + str(opType) + "_deg_" + labelName
        newLabelPath = os.path.join (savePath, newLabelPath)

        f = open(newLabelPath, "w+")
        with open(labelPath) as fp:
            lines = fp.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue
            valueList=(line.split())
            # print(valueList)
            (a, b, c, d, e) = valueList[0], valueList[1], valueList[2], valueList[3], valueList[4]

            if opType == "270":
                f.write(a + " " + str(1-float(c)) + " " + b + " " + e + " " + d + "\n")
            elif opType == "180":
                f.write(a + " " + str(1- float(b)) + " " + str(1-float(c)) + " " + d + " " + e + "\n")
            elif opType == "90":
                f.write(a + " " + c + " " + str(1- float(b)) + " " + e + " " + d + "\n")
            else:
                (a, b, c, d, e) = int(valueList[0]), float(valueList[1]), float(valueList[2]), float(valueList[3]), \
                                  float(valueList[4])
                degree = float (opType)
                degree = degree % 180
                if degree > 90:
                    degree = 180 - degree

                degree = degree * math.pi / 180
                wcos = width * math.cos(degree)
                wsin = width * math.sin(degree)
                hcos = height * math.cos(degree)
                hsin = height * math.sin(degree)

                boxx = float ((b * wcos + c * hsin) / (wcos + hsin))
                boxy = float ((c * hcos + (1 - b) * wsin) / (hcos + wsin))
                boxWidth = float ((d * wcos + e * hsin) / (wcos + hsin))
                boxHeight = float ((e * hcos + d * wsin) / (hcos + wsin))

                f.write(str (a) + " " + str(boxx) + " " + str(boxy) + " " + str(boxWidth) + " " + str(boxHeight) + "\n")
        f.close ()

        return myCommand, newImgName

    #blur
    if opType == "blur":
        newImgName = "blur_" + imageName
        myCommand = "convert " + os.path.join (savePath, imageName) + " -blur 2x2 " + os.path.join (savePath, newImgName)
        newLabelPath = "blur_" + labelName
        newLabelPath = os.path.join (savePath, newLabelPath)

        f = open(newLabelPath, "w+")
        with open(labelPath) as fp:
            lines = fp.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue
            valueList=(line.split())
            print(valueList)
            a,b,c,d,e = valueList[0], valueList[1], valueList[2], valueList[3], valueList[4]

            if opType == "blur":
                f.write(a + " " + b + " " + c + " " + d + " " + e + "\n")
        f.close()
                                
        return myCommand, newImgName



# The program reads the images from the given directory and save the new images in the same directory
# The label files are supposed to be available in the same directory
# The list of all image file names will be saved in list.txt
if len (sys.argv) != 2:
    print ("Usage: {} directory")
    quit ()

# The directory where original images sit
imageDir = sys.argv[1]
orgImageList = []

for file in os.listdir(imageDir):
    (filename, file_extension) = os.path.splitext(file)
    file_extension = file_extension.lower()
    if file_extension == ".jpg" or file_extension == ".png" or file_extension == ".jpeg" or file_extension == ".gif":
        orgImageList.append (file)

#dump out the names of images and labeling files into txt
listFilePath = os.path.join (imageDir, "list.txt")
resultImgList = []
resultImgList.extend(orgImageList)

for imageName in orgImageList:
    txtName = os.path.splitext (imageName)[0] + '.txt'
    if not os.path.isfile(os.path.join (imageDir, txtName)):
        print (f"Label file does not exist for {imageName} in {imageDir}.")
        quit ()

    trackImgList = [imageName]

    for ops in [ ["rotate-" + str(x) for x in range (10, 360,10)],
                 ['blur'], ["flop","flip"], ["scale-50", "scale-200"]]:
        tmpImgList = []
        for i in range(0, len(trackImgList)):
            # Read image's width and height
            image = Image.open(os.path.join (imageDir, trackImgList[i]))
            (width, height) = image.size
            for op in ops:
                imgNameInProc = trackImgList[i]
                txtNameInProc = os.path.splitext (imgNameInProc)[0] + '.txt'
                (myCommand, newImgName) = imgOperation(op, imageDir, imgNameInProc, txtNameInProc, width, height)
                tmpImgList.append(newImgName)
                #print("file #: ",str(i +1))
                #print(myCommand)
                #time.sleep(5)
                os.system(myCommand)
        trackImgList.extend(tmpImgList)

    resultImgList.extend(trackImgList)

outputFile = open(listFilePath, "a")
for x in resultImgList:
    outputFile.write(x + "\n")
outputFile.close()


