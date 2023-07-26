import pandas as pd

# Read the attendance.csv file into a DataFrame
df = pd.read_csv('attendance.csv')

# Create a mask to check if any column is 'A'
mask = (df['Face Value'] == 'A') | (df['LocationValue'] == 'A') 

# Update the "FinalAttendance" column based on the mask
df['FinalAttendance'] = 'P'
df.loc[mask, 'FinalAttendance'] = 'A'

# Save the updated DataFrame back to the attendance.csv file
df.to_csv('attendance.csv', index=False)
