import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import fcluster
from sklearn.ensemble import IsolationForest
import pandas as pd

# Load the distance matrix
distance_matrix = np.load('distance_matrix.npy')

# Make the distance matrix symmetric
symmetric_distance_matrix = (distance_matrix + distance_matrix.T) / 2

# Plotting the heatmap of the symmetric distance matrix
plt.figure(figsize=(12, 10))
plt.imshow(symmetric_distance_matrix, cmap='viridis', interpolation='nearest')
plt.colorbar(label='Distance')
plt.title('Symmetric Distance Matrix Heatmap')
plt.xlabel('Index')
plt.ylabel('Index')
plt.show()

# Convert the symmetric distance matrix to a condensed form
condensed_symmetric_distance_matrix = squareform(symmetric_distance_matrix)

# Perform hierarchical clustering
linked = sch.linkage(condensed_symmetric_distance_matrix, method='ward')

# Plotting the dendrogram
plt.figure(figsize=(12, 8))
sch.dendrogram(linked)
plt.title('Dendrogram of Similarity Measures')
plt.xlabel('Index')
plt.ylabel('Distance')
plt.show()

# Creating clusters
clusters = fcluster(linked, t=1.5, criterion='distance')

# Anomaly detection using Isolation Forest
clf = IsolationForest(contamination=0.05)
clf.fit(symmetric_distance_matrix)
anomalies = clf.predict(symmetric_distance_matrix)
anomalies_indices = np.where(anomalies == -1)[0]

# Plot the symmetric distance matrix with anomaly highlights
plt.figure(figsize=(12, 10))
plt.imshow(symmetric_distance_matrix, cmap='viridis', interpolation='nearest')
plt.colorbar(label='Distance')
plt.title('Symmetric Distance Matrix with Anomaly Highlights')
plt.xlabel('Index')
plt.ylabel('Index')

# Overlay the anomalies
plt.scatter(anomalies_indices, anomalies_indices, color='red', label='Anomalies', s=50)
plt.legend()
plt.show()

# Display the anomalies
anomalies_data = pd.DataFrame({'Index': anomalies_indices, 'Anomaly': 'Yes'})
print(anomalies_data.head())

# Saving the anomalies data to a CSV file for further analysis
anomalies_data.to_csv('anomalies_data.csv', index=False)
