import csv
import face_recognition
import os

# Path to the folders containing the images
img_folder_path = "face_img/"
data_folder_path = "face_img_data/"

# Path to the attendance CSV file
attendance_file_path = "attendance.csv"

# Read the attendance CSV file and update the "faceValue" column
updated_attendance_data = []

with open(attendance_file_path, "r") as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames  # Get the field names from the header row
    for row in reader:
        # Get the student ID and image filename
        student_id = row["Student ID"]
        img_filename = f"{student_id}.jpg"

        # Construct the paths to the image and data
        img_path = os.path.join(img_folder_path, img_filename)
        data_path = os.path.join(data_folder_path, img_filename)

       
                     # Load the images using the face_recognition library
        img = face_recognition.load_image_file(img_path)
        data_img = face_recognition.load_image_file(data_path)

                # Encode the faces in the images
        img_encoding = face_recognition.face_encodings(img)
        data_encoding = face_recognition.face_encodings(data_img)

                # Compare the face encodings
        if img_encoding and data_encoding:
            results = face_recognition.compare_faces(img_encoding, data_encoding[0])
            if any(results):
                row["faceValue"] = "P"  # Set faceValue as "P" for matching images

        updated_attendance_data.append(row)

# Write the updated attendance data back to the CSV file
with open(attendance_file_path, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_attendance_data)

print("Attendance data updated successfully.")
