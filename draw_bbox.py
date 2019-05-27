import cv2
import os
import argparse

def show_pic(img, label, bboxes=None):
    
    cv2.imwrite('./1.jpg', img)
    img = cv2.imread('./1.jpg')
    colors = [(0,255,0),(0,0,255)]
    for i in range(len(bboxes)):
        bbox = bboxes[i]
        x_min = bbox[0]
        y_min = bbox[1]
        x_max = bbox[2]
        y_max = bbox[3]
        cv2.rectangle(img,(int(x_min),int(y_min)),(int(x_max),int(y_max)),colors[i],3) 
        cv2.putText(img, label, (int(x_min), int(y_min)), cv2.FONT_HERSHEY_SIMPLEX, 1, colors[i], 2)
    cv2.namedWindow('pic', 0)  
    cv2.moveWindow('pic', 0, 0)
    cv2.resizeWindow('pic', 600,600)  
    cv2.imshow('pic', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    os.remove('./1.jpg')

def calculateIoU(candidateBound, groundTruthBound):
    cx1 = candidateBound[0]
    cy1 = candidateBound[1]
    cx2 = candidateBound[2]
    cy2 = candidateBound[3]

    gx1 = groundTruthBound[0]
    gy1 = groundTruthBound[1]
    gx2 = groundTruthBound[2]
    gy2 = groundTruthBound[3]

    carea = (cx2 - cx1) * (cy2 - cy1) #C的面积
    garea = (gx2 - gx1) * (gy2 - gy1) #G的面积

    x1 = max(cx1, gx1)
    y1 = max(cy1, gy1)
    x2 = min(cx2, gx2)
    y2 = min(cy2, gy2)
    w = max(0, x2 - x1)
    h = max(0, y2 - y1)
    area = w * h #C∩G的面积

    iou = area / (carea + garea - area)

    return iou

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--draw', default=False, action='store_true',
        help='input bbox by hand'
    )

    FLAGS = parser.parse_args()

    classes = ["Atelectasis", "Cardiomegaly"]
    
    if FLAGS.draw:
        img_dir = input('Please input image dir: ')

        bboxes = []
        while True:
            bbox = input('Please input bbox with xmin, ymin, xman, ymax: ')
            if bbox == 'q':
                break
            else: 
                bbox = eval(bbox) 
                print(bbox)
                bboxes.append(bbox)
        label = input('Please input label id: ')
        class_name = classes[int(label)]
        
        img = cv2.imread(img_dir)
        show_pic(img, class_name, bboxes)
    
    else:

        source_pic_root_path = '../dataset/images/'
        source_bbox_root_path = './train_sample.txt'
        

        txtFile = open(source_bbox_root_path, 'r')
        lines = txtFile.readlines()

        trainFile = open(new_bbox_path, 'a')

        for line in lines:
            lst = line.split()
            img_dir = lst[0]
            bbox_and_label = lst[1]

            bbox = [int(i) for i in bbox_and_label.split(',')[:4]]
            bboxes = []
            bboxes.append(bbox)
            label = bbox_and_label.split(',')[4]
            class_name = classes[int(label)]
            img_name = str(lines.index(line))
            # print(bboxes, label)
            
            cnt = 0
            img = cv2.imread(img_dir)
            show_pic(img, class_name, bboxes)
            img_path = new_img_path + img_name
            cv2.imwrite(img_path+".png", img)