import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendancesystem-ba445-default-rtdb.firebaseio.com/'
})

firebase_db = db.reference('/')

# Function to save attendance data to Firebase
def save_attendance(student_id, student_name, st):
    # Get current data from time
    now = datetime.now()
    date_time = now.strftime('%Y-%m-%d %H:%M:%S')

    # Check if attendance already exists for the current day
    attendance_data = firebase_db.child('attendance').get()
    if attendance_data:
        for _, data in attendance_data.items():
            if data['student_id'] == student_id and data['date'][:10] == now.strftime('%Y-%m-%d'):
                st.warning('Attendance already taken for ' + student_name + ' today.')
                return
    
    data = {'student_id': student_id, 'student_name': student_name, 'date': date_time}
    firebase_db.child('attendance').push(data)
    st.success('Attendance taken for ' + student_name + ' at ' + date_time)


def get_attendance(st):
    # Fetch previous attendance records
    with st.spinner('Loading...'):
        attendance_data = firebase_db.child('attendance').get()
    st.success('Attendance records loaded.')

    if attendance_data:
        st.subheader('Previous Attendance Records')
        attendance_list = [{'Name': data['student_name'], 'ID': data['student_id'], 'Date': data['date']} for data in attendance_data.values()]
        st.table(attendance_list)
        