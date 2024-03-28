import cv2
import pickle
import face_recognition
import os

img_path = 'dataset'
path_list = os.listdir(img_path)

img_list = []
student_names = []
student_ids = []

for path in path_list:
    image = cv2.imread(os.path.join(img_path, path))
    img_list.append(image)
    image_name, student_id= path.split('.')[0], path.split('.')[1]
    student_names.append(image_name)
    student_ids.append(student_id.replace('-','/'))


def encode_imgs(img_list):
    encode_list = []

    for img in img_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)

    return encode_list

encode_list = encode_imgs(img_list)
encode_list_with_names_and_ids = [encode_list, student_names, student_ids]

file = open('encoded_imgs.p', 'wb')
pickle.dump(encode_list_with_names_and_ids, file)
file.close()
print('File saved!')

