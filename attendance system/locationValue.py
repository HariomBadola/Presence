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
