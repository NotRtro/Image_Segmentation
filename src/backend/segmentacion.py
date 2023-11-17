from librerias import *
from app.routes.login import app


#Labels of network.
classes = { 0: 'background',
    1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
    5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
    10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
    14: 'motorbike', 15: 'person', 16: 'pottedplant',
    17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor' }

net = cv2.dnn.readNetFromCaffe(prototxt, model)

@app.route('/procesar_subida', methods=['POST'])
def process_image():
    selected_classes = request.json.get('selected_classes', [])
    selected_classes = [int(class_id) for class_id in selected_classes if class_id.isdigit() and int(class_id) in classes]

    i=0
    for x in range(5):        
        image = cv2.imread("car"+str(x+1)+".jpg")

        height, width, _ = image.shape
        image_resized =cv2.resize(image, (300, 300))

        blob = cv2.dnn.blobFromImage(image_resized, 0.007843, (300,300), (127.5, 127.5, 127.5))
        print("blob.shape:",blob.shape)
        net.setInput(blob)
        detections = net.forward() 
        for detection in detections[0][0]:
            if  detection[2]>0.45:
                label_index = int(detection[1])
                if label_index in selected_classes:
                    label =classes[label_index]
                    box = detection[3:7] * [width, height, width, height]
                    x_start, y_start, x_end, y_end = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                    cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
                    cv2.putText(image,"Confg:{:.2f}".format(detection[2]*100), (x_start, y_start-5),1,1.2,(255,0,0),2)
                    cv2.putText(image,label,(x_start, y_start - 25),1,1.2,(255,0,0,0),2)
                    
                    roi = image[y_start:y_end, x_start:x_end]
                    cv2.imwrite("./temporal/"+str(i)+".jpg", roi)
                    i+=1
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


