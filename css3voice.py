import cv2
import face_recognition
import csv
import pyttsx3
from datetime import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load known face encodings and names
known_face_encodings = []
known_face_names = []

# Load known face
known_person1_image = face_recognition.load_image_file(r"D:\cs project content\nikhil cs.jpg")
known_person2_image = face_recognition.load_image_file(r"F:\MyProject\rish.jpg")
known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]
known_person2_encoding = face_recognition.face_encodings(known_person2_image)[0]

known_face_encodings.append(known_person1_encoding)
known_face_encodings.append(known_person2_encoding)
known_face_names.append("Nikhil")
known_face_names.append("Rishabh")

# Track names already logged during this session
logged_names = set()

# Open webcam
video_capture = cv2.VideoCapture(0)

# Open CSV file to write attendance
with open("attendance.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Time"])

    while True:
        ret, frame = video_capture.read()

        # Find face locations and encodings
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                # Log attendance + voice only once
                if name not in logged_names:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    writer.writerow([name, current_time])
                    logged_names.add(name)

                    # Speak greeting
                    engine.say(f"Hello {name}, you are marked present")
                    engine.runAndWait()

                    print(f"{name} marked present at {current_time}")

            # Draw box and label
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Show the frame
        cv2.imshow("Video", frame)

        # Break with 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()
