import face_recognition
import os
import pandas as pd

# Path to the folders containing the images
img_folder_path = "face_img/"
data_folder_path = "face_img_data/"

# Load the existing attendance data from the CSV file
attendance_df = pd.read_csv("attendance.csv")

# Get the list of image filenames from the img_folder_path
img_filenames = os.listdir(img_folder_path)

# Create a column to store the face values (initialized as "A" for all records)
attendance_df["Face Value"] = "A"

for img_filename in img_filenames:
    # Extract the student ID from the image filename without the file extension
    student_id = os.path.splitext(img_filename)[0]

    # Construct the paths to the two images
    img_path = os.path.join(img_folder_path, img_filename)
    data_path = os.path.join(data_folder_path, img_filename)

    # Check if the image exists in the data folder
    if not os.path.exists(data_path):
        print(f"No matching image found for {img_filename} in the data folder.")
        continue

    # Load the images using the face_recognition library
    img = face_recognition.load_image_file(img_path)
    data_img = face_recognition.load_image_file(data_path)

    # Encode the faces in the images
    img_encoding = face_recognition.face_encodings(img)[0]
    data_encoding = face_recognition.face_encodings(data_img)[0]

    # Compare the face encodings
    results = face_recognition.compare_faces([img_encoding], data_encoding)

    # Update the "Face Value" column in the attendance DataFrame if a match is found
    if results[0]:
        attendance_df.loc[attendance_df["Student ID"] == student_id, "Face Value"] = "P"
        print(f"{img_filename} and {img_filename} are the same person.")
    else:
        print(f"{img_filename} and {img_filename} are different people.")

# Save the updated attendance DataFrame back to the CSV file
attendance_df.to_csv("attendance.csv", index=False)
