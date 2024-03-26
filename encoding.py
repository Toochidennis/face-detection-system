import cv2
import pickle
import face_recognition
import os

img_path = 'dataset'
path_list = os.listdir(img_path)
#print(path_list)

img_list = []
student_names = []
student_ids = ["PAS/CSC/19/018", 'PAS/CSC/19/025', 'PAS/CSC/19/003', 'PAS/CSC/19/016', 'PAS/CSC/17/013']

for path in path_list:
    image = cv2.imread(os.path.join(img_path, path))
    img_list.append(image)
    image_name = os.path.splitext(path)[0]
    student_names.append(image_name)


def find_encodings(img_list):
    encode_list = []

    for img in img_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)

    return encode_list

encode_list = find_encodings(img_list)
encode_list_with_names_and_ids = [encode_list, student_names, student_ids]

file = open('encoded_imgs.p', 'wb')
pickle.dump(encode_list_with_names_and_ids, file)
file.close()
print('File saved!')

