import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import fcluster
from scipy.spatial.distance import squareform

file_name = "./distance_matrix.npy"



            
data = np.load(file_name)
print('Datatype:', data)
np.ndarray.view(data)
linked = sch.linkage(data, method='ward')

clusters = fcluster(linked, t=1.5, criterion='distance')

# Plot the distance matrix with cluster highlights
plt.figure(figsize=(10, 8))
plt.imshow(data, cmap='viridis', interpolation='nearest')
plt.colorbar(label='Distance')
plt.title('Distance Matrix with Cluster Highlights')
plt.xlabel('Index')
plt.ylabel('Index')

# Overlay the clusters
unique_clusters = np.unique(clusters)
for cluster_number in unique_clusters:
    cluster_indices = np.where(clusters == cluster_number)
    for index in cluster_indices[0]:
        plt.scatter(index, index, label=f'Cluster {cluster_number}')

plt.legend()
plt.show()

# Creating clusters (you can adjust the t value to change the number of clusters)
clusters = fcluster(linked, t=1.5, criterion='distance')

# Plot the clusters on the distance matrix
plt.figure(figsize=(10, 8))
plt.imshow(data, cmap='viridis', interpolation='nearest')
plt.colorbar(label='Distance')
plt.title('Distance Matrix with Clusters')
plt.xlabel('Index')
plt.ylabel('Index')

# Overlay the clusters
for cluster_number in np.unique(clusters):
    cluster_indices = np.where(clusters == cluster_number)
    plt.scatter(cluster_indices, cluster_indices, label=f'Cluster {cluster_number}')


# Plotting the dendrogram
plt.figure(figsize=(10, 7))
sch.dendrogram(linked)
plt.title('Dendrogram')
plt.xlabel('Index')
plt.ylabel('Distance')
plt.show()