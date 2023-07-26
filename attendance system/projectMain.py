import pandas as pd
import os
import requests

# ======================================================= Fetch current location coordinates
def get_current_coordinates():
    try:
        # Send a request to the ip-api service
        response = requests.get('http://ip-api.com/json?fields=lat,lon&precision=8')
        
        if response.status_code == 200:
            data = response.json()
            latitude = data['lat']
            longitude = data['lon']
            return latitude, longitude
        else:
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Get and print current coordinates
current_coordinates = get_current_coordinates()
if current_coordinates:
    latitude , longitude = current_coordinates
    #print(f"Latitude: {latitude}")
    #print(f"Longitude: {longitude}")
else:
    print("Unable to fetch current coordinates.")


# Ask for user's name and student ID
name = input("Enter your name: ")
student_id = input("Enter your student ID: ")


# Create a dictionary with the attendance information
attendance_data = {
    "Student ID": [student_id],
    "Name": [name],
    "Latitude": [latitude],
    "Longitude": [longitude]
}

# Convert the dictionary to a DataFrame
df = pd.DataFrame(attendance_data)

# Check if the attendance file exists
if os.path.isfile("attendance.csv"):
    # Append the new attendance data to the existing file
    existing_df = pd.read_csv("attendance.csv")
    updated_df = existing_df._append(df, ignore_index=True)
    
    updated_df.to_csv("attendance.csv", index=False)
   # updated_df = updated_df.sort_values("Student ID")

else:
    # Create a new file with the attendance data
    df.to_csv("attendance.csv", index=False)




import cv2
import tkinter as tk
from PIL import Image, ImageTk

# Create a folder if it doesn't exist
if not os.path.exists("face_img"):
    os.makedirs("face_img")

# Initialize webcam
camera = cv2.VideoCapture(0)

# Create a Tkinter window
window = tk.Tk()

# Create a label to display the webcam feed
image_label = tk.Label(window)
image_label.pack()

# Flag to indicate if picture is to be taken or not
take_picture = False

# Function to capture an image from the webcam
def capture_image():
    global take_picture

    # Read the current frame from the webcam
    ret, frame = camera.read()

    if ret:
        # Save the image with the student ID
        img_path = f"face_img/{student_id}.jpg"
        cv2.imwrite(img_path, frame)
        print(f"Image saved as {img_path}")
        take_picture = False

        # Release the webcam after capturing the image
        camera.release()

        # Close the Tkinter window
        window.destroy()

# Create a button to capture the image
capture_button = tk.Button(window, text="Capture", command=capture_image)
capture_button.pack()

# Function to update the frame
def update_frame():
    # Read the current frame from the webcam
    ret, frame = camera.read()

    if ret:
        # Resize the frame to a smaller size
        frame = cv2.resize(frame, (400, 300))

        # Convert the frame to RGB color space
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a PIL ImageTk object
        image = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))

        # Update the image in the Tkinter window
        image_label.configure(image=image)
        image_label.image = image

    if not window.winfo_exists():
        # Release the webcam if the window is closed
        camera.release()

    else:
        # Schedule the next frame update
        image_label.after(10, update_frame)

# Start updating the frame
update_frame()

# Start the Tkinter event loop
window.mainloop()



print("Attendance data saved successfully.")

#==============================================Location Value =====================================================
import pandas as pd
from sklearn.cluster import DBSCAN

# Read the CSV file into a DataFrame
df = pd.read_csv('attendance.csv')

# Extract latitude and longitude columns
coordinates = df[['Latitude', 'Longitude']].values

# Perform DBSCAN clustering
epsilon = 0.0001  # Adjust the epsilon value as needed
min_samples = 3  # Adjust the minimum number of samples as needed
dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)
clusters = dbscan.fit_predict(coordinates)

# Mark values as 'A' for anomalies and 'P' for non-anomalies
df['LocationValue'] = 'P'
df.loc[dbscan.labels_ == -1, 'LocationValue'] = 'A'

# Save the updated DataFrame to the CSV file
df.to_csv('attendance.csv', index=False)


#==================================================== Face Value ====================================

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
    #img_filename = img_filename.split(".",1)
    #img_filename = img_filename[0]
    # Update the "Face Value" column in the attendance DataFrame if a match is found
    if results[0]:
       
        attendance_df.loc[attendance_df["Student ID"] ==int(student_id), "Face Value"] = "P"
        
    else:
        print(f"{img_filename} and {img_filename} are different people.")

# Save the updated attendance DataFrame back to the CSV file
attendance_df.to_csv("attendance.csv", index=False)



#============================================================= Final result ==============================

# Read the attendance.csv file into a DataFrame
df = pd.read_csv('attendance.csv')

# Create a mask to check if any column is 'A'
mask = (df['Face Value'] == 'A') | (df['LocationValue'] == 'A') | (df['Face Value'] == ' ') | (df['LocationValue'] == ' ' ) 

# Update the "FinalAttendance" column based on the mask
df['FinalAttendance'] = 'P'
df.loc[mask, 'FinalAttendance'] = 'A'

# Save the updated DataFrame back to the attendance.csv file
df.to_csv('attendance.csv', index=False)
