import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime
import mediapipe as mp

# Open the video capture object to access the webcam
video_capture = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Directory where the known face images are stored
directory = r"students"
file_list = os.listdir(directory)
names11 = []
names_alreadyPresent = []
known_face_encoding = []
known_face_names = []

# Iterate through the files in the directory
for filename in file_list:
    name = filename.split('.')[0]
    names11.append(name)
    personName = face_recognition.load_image_file(f"students/{filename}")
    personEncoding = face_recognition.face_encodings(personName)[0]
    known_face_encoding.append(personEncoding)
    known_face_names.append(name)

students = known_face_names.copy()

# Set up variables for face detection and recognition
face_locations = []
face_encoding = []
face_names = []
p = True

# Create a CSV file for attendance records
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date+'.csv', 'a+', newline='')
lnwriter = csv.writer(f)

# for finding already present members
f1 = open(current_date+'.csv', 'r')
lnreader = csv.reader(f1)
for row in lnreader:
    # print(row)
    names_alreadyPresent.append(row[0])
print("names_alreadyPresent : ", names_alreadyPresent)

while True:
    # Read a frame from the video capture
    _, frame = video_capture.read()
    frame = cv2.flip(frame, 1)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_height, frame_width, _ = frame.shape

    if True:
        # Locate faces in the frame and encode them
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)
        face_names = []

        # Compare the faces with known faces and recognize them
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                known_face_encoding, face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(
                known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distance)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            face_names.append(name)

            # Mark attendance for recognized individuals
            if name in known_face_names and name not in names_alreadyPresent:
                if landmark_points:
                    landmarks = landmark_points[0].landmark
                    left = [landmarks[145], landmarks[159]]
                    for landmark in left:
                        x = int(landmark.x * frame_width)
                        y = int(landmark.y * frame_height)
                        cv2.circle(frame, (x, y), 3, (0, 255, 255))
                    # print(left[0].y - left[1].y)
                    if (left[0].y - left[1].y) < 0.012:
                        print("Present")
                        # Draw a text overlay on the frame
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        bottomLeftCornerOfText = (10, 100)
                        fontScale = 1.5
                        fontColor = (19, 237, 63)
                        thickness = 3
                        lineType = 2

                        cv2.putText(frame, name+' Present',
                                    bottomLeftCornerOfText,
                                    font,
                                    fontScale,
                                    fontColor,
                                    thickness,
                                    lineType)

                        # Remove recognized individuals from the list of students
                        if name in students:
                            students.remove(name)
                            print(students)
                            current_time = now.strftime("%H:%M:%S")
                            lnwriter.writerow([name, current_time])

            elif name in names_alreadyPresent and name in known_face_names:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10, 100)
                fontScale = 1.5
                fontColor = (19, 237, 63)
                thickness = 3
                lineType = 2

                cv2.putText(frame, 'Already Present',
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            thickness,
                            lineType)

                print(name)
            else:
                while (p):
                    wish = input("Are you willing to join this class (Y/N): ")
                    if wish == 'Y' or wish == 'y':
                        ret, frame1 = video_capture.read()
                        if ret:
                            dir = r"students"
                            filename = input("Enter Your name : ")
                            file_path = os.path.join(dir, filename + ".jpg")
                            cv2.imwrite(file_path, frame1)
                            print("Image saved successfully", file_path)
                            current_time = now.strftime("%H:%M:%S")
                            lnwriter.writerow([filename, current_time])
                            break
                        p = False
                    elif wish == 'N' or wish == 'n':
                        p = False
                        break
                    print("done")
                    break

    cv2.imshow("attendance system", frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
video_capture.release()
cv2.destroyAllWindows()
f.close()
