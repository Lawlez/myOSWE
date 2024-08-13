import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import fcluster
import pandas as pd

# Load the distance matrix
distance_matrix = np.load('distance_matrix.npy')

# Make the distance matrix symmetric
symmetric_distance_matrix = (distance_matrix + distance_matrix.T) / 2

# Define a smaller subset size
subset_size = 200

# Extract a subset of the distance matrix
subset_distance_matrix = symmetric_distance_matrix[:subset_size, :subset_size]

# Plotting the heatmap of the subset distance matrix
plt.figure(figsize=(12, 10))
plt.imshow(subset_distance_matrix, cmap='viridis', interpolation='nearest')
plt.colorbar(label='Distance')
plt.title('Subset Distance Matrix Heatmap')
plt.xlabel('Index')
plt.ylabel('Index')
plt.show()

# Convert the subset distance matrix to a condensed form
condensed_subset_distance_matrix = squareform(subset_distance_matrix)

# Perform hierarchical clustering
linked_subset = sch.linkage(condensed_subset_distance_matrix, method='ward')

# Plotting the dendrogram for the subset
plt.figure(figsize=(12, 8))
sch.dendrogram(linked_subset)
plt.title('Dendrogram of Subset Similarity Measures')
plt.xlabel('Index')
plt.ylabel('Distance')
plt.show()

# Creating clusters for the subset
clusters_subset = fcluster(linked_subset, t=1.5, criterion='distance')

# Plot the subset distance matrix with cluster highlights
plt.figure(figsize=(12, 10))
plt.imshow(subset_distance_matrix, cmap='viridis', interpolation='nearest')
plt.colorbar(label='Distance')
plt.title('Subset Distance Matrix with Cluster Highlights')
plt.xlabel('Index')
plt.ylabel('Index')

# Overlay the clusters
unique_clusters_subset = np.unique(clusters_subset)
for cluster_number in unique_clusters_subset:
    cluster_indices = np.where(clusters_subset == cluster_number)
    for index in cluster_indices[0]:
        plt.scatter(index, index, label=f'Cluster {cluster_number}', s=10)

plt.legend()
plt.show()

# Display the clusters
cluster_data_subset = pd.DataFrame({'Index': range(len(clusters_subset)), 'Cluster': clusters_subset})
print(cluster_data_subset.head())
