import numpy as np
import matplotlib.pyplot as plt
from sklearn.covariance import EllipticEnvelope
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd

# Load the distance matrix
distance_matrix = np.load('path_to_your_distance_matrix.npy')

# Make the distance matrix symmetric
symmetric_distance_matrix = (distance_matrix + distance_matrix.T) / 2

# Define a smaller subset size for testing
subset_size = 200  # Adjust this based on available memory and processing power

# Extract a subset of the distance matrix
subset_distance_matrix = symmetric_distance_matrix[:subset_size, :subset_size]

# Standardize the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(subset_distance_matrix)

# Reduce dimensionality using PCA
pca = PCA(n_components=10)  # Use fewer components for faster processing
data_pca = pca.fit_transform(data_scaled)

# Elliptic Envelope
clf_ee = EllipticEnvelope(contamination=0.05)
anomalies_ee = clf_ee.fit_predict(data_pca)
anomalies_indices_ee = np.where(anomalies_ee == -1)[0]

# Define a function to plot anomalies
def plot_anomalies(anomalies_indices, title):
    plt.figure(figsize=(12, 10))
    plt.imshow(subset_distance_matrix, cmap='viridis', interpolation='nearest')
    plt.colorbar(label='Distance')
    plt.title(title)
    plt.xlabel('Index')
    plt.ylabel('Index')
    plt.scatter(anomalies_indices, anomalies_indices, color='red', label='Anomalies', s=50)
    plt.legend()
    plt.show()

# Plot anomalies
plot_anomalies(anomalies_indices_ee, 'Elliptic Envelope Anomalies after PCA')

# Display the anomalies
anomalies_data_ee = pd.DataFrame({'Index': anomalies_indices_ee, 'Anomaly': 'Yes'})
print(anomalies_data_ee.head())

# Save the anomalies data to a CSV file for further analysis
anomalies_data_ee.to_csv('elliptic_envelope_anomalies_after_pca.csv', index=False)
