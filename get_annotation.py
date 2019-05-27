import os
import csv

wd = os.getcwd()

csv_dir = "../labels/BBox_List_2017.csv"
txt_dir = "./train_sample.txt"
img_set_dir = "../dataset/images/"
dic = {}
classes = ["Atelectasis", "Cardiomegaly"]

csvFile = open(csv_dir, "r")
reader = csv.reader(csvFile)
for line in reader:
    if reader.line_num == 1:
        continue
    xmin, ymin = float(line[2]), float(line[3])
    w, h = float(line[4]), float(line[5])
    xmax, ymax = xmin + w, ymin + h
    xmin, xmax, ymin, ymax = round(xmin), round(xmax), round(ymin), round(ymax)

    
    cls = line[1]
    if cls not in classes:
        continue
    cls_id = classes.index(cls)
    val = str(xmin) + "," + str(ymin) + "," + str(xmax) + "," + str(ymax) + "," + str(cls_id)

    img_dir = img_set_dir + line[0]

    if img_dir not in dic.keys():
        dic[img_dir] = [val]
    else:
        dic[img_dir].append(val)

csvFile.close()

txtFile = open(txt_dir, "w")
for img in dic.keys():
    txtFile.write("{}".format(img))
    for bbox in dic[img]:
        txtFile.write(" {}".format(bbox))
    txtFile.write("\n")
txtFile.close()


