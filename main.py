import cv2
import face_recognition
import pickle
import numpy as np
import streamlit as st
from firebase_util import save_attendance, get_attendance


# Load the face recognition model and student data
file = open('encoded_imgs.p', 'rb')
encode_list_with_names_and_ids = pickle.load(file)
file.close()
encode_list, student_names, student_ids = encode_list_with_names_and_ids


def home_page():
    st.title('Face Recognition Attendance')
    st.markdown('')

    st.write('Click the button below to take attendance.')

    if st.button('Take Attendance'):
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        # Create an empty placeholder for the webcam feed
        placeholder = st.empty()
        
        # Main loop to capture frames from the webcam
        while True:
            success, frame = cap.read()

            if not success:
                break

            img = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Perform face detection and recognition
            current_frame = face_recognition.face_locations(img)
            encode_frame = face_recognition.face_encodings(img, current_frame)

            for encode_face, face_location in zip(encode_frame, current_frame):
                matches = face_recognition.compare_faces(encode_list, encode_face)
                face_distance = face_recognition.face_distance(encode_list,encode_face)
                match_index = np.argmin(face_distance)

                if matches[match_index]:
                    top, right, bottom, left = face_location  # Extract face coordinates
                    name = student_names[match_index]
                    id = student_ids[match_index]

                    # Draw a rectangle around the detected face
                    cv2.rectangle(frame, (left*4, top*4), (right*4, bottom*4), (0, 255, 0), 2)

                    # Display the name above the rectangle
                    cv2.putText(frame, name, (left*4, top*4 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    # Save attendance to firebase
                    save_attendance(student_id=id, student_name=name, st=st)
                    cap.release()
                    cv2.destroyAllWindows()
                    break

            # Display the frame in the Streamlit app
            placeholder.image(frame, channels="BGR", use_column_width=True)

            # Check for key press to stop the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        
def attendance_history():
    st.title('Attendance record')
    get_attendance(st=st)


def about_page():
    st.write('This is a Streamlit web application for face recognition based attendance system.')


def main():
    st.sidebar.title('Menu')
    page = st.sidebar.radio('Go to', ['Home', 'Attendance record', 'About'])

    if page == 'Home':
        home_page()
    elif page == 'Attendance record':
        attendance_history()
    elif page == 'About':
        about_page()

if __name__ == '__main__':
    main()
