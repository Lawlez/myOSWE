import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.cluster import DBSCAN
from sklearn.covariance import EllipticEnvelope
from sklearn.preprocessing import StandardScaler

# Load the distance matrix
distance_matrix = np.load('distance_matrix.npy')

# Make the distance matrix symmetric
symmetric_distance_matrix = (distance_matrix + distance_matrix.T) / 2

# Standardize the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(symmetric_distance_matrix)

# Isolation Forest
clf_if = IsolationForest(contamination=0.05)
anomalies_if = clf_if.fit_predict(data_scaled)
anomalies_indices_if = np.where(anomalies_if == -1)[0]
anomalies_data_if = pd.DataFrame({'Index': anomalies_indices_if, 'Anomaly': 'Yes'})
anomalies_data_if.to_csv('isolation_forest_anomalies.csv', index=False)


# Local Outlier Factor
clf_lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
anomalies_lof = clf_lof.fit_predict(data_scaled)
anomalies_indices_lof = np.where(anomalies_lof == -1)[0]
anomalies_data_lof = pd.DataFrame({'Index': anomalies_indices_lof, 'Anomaly': 'Yes'})
anomalies_data_lof.to_csv('local_outlier_factor_anomalies.csv', index=False)

# One-Class SVM
clf_ocsvm = OneClassSVM(nu=0.05, kernel='rbf', gamma=0.1)
anomalies_ocsvm = clf_ocsvm.fit_predict(data_scaled)
anomalies_indices_ocsvm = np.where(anomalies_ocsvm == -1)[0]
anomalies_data_ocsvm = pd.DataFrame({'Index': anomalies_indices_ocsvm, 'Anomaly': 'Yes'})
anomalies_data_ocsvm.to_csv('one_class_svm_anomalies.csv', index=False)

# DBSCAN
clf_dbscan = DBSCAN(eps=3, min_samples=5)
clusters_dbscan = clf_dbscan.fit_predict(data_scaled)
anomalies_indices_dbscan = np.where(clusters_dbscan == -1)[0]
anomalies_data_dbscan = pd.DataFrame({'Index': anomalies_indices_dbscan, 'Anomaly': 'Yes'})
anomalies_data_dbscan.to_csv('dbscan_anomalies.csv', index=False)

print("Anomaly detection complete and results saved to CSV files.")


# Load anomaly data from CSV files
anomalies_if = pd.read_csv('isolation_forest_anomalies.csv')
anomalies_ee = pd.read_csv('elliptic_envelope_anomalies_after_pca.csv')
anomalies_lof = pd.read_csv('local_outlier_factor_anomalies.csv')
anomalies_ocsvm = pd.read_csv('one_class_svm_anomalies.csv')
anomalies_dbscan = pd.read_csv('dbscan_anomalies.csv')

# Combine all anomalies into a single DataFrame for summary
all_anomalies = {
    'IsolationForest': anomalies_if,
    'EllipticEnvelope': anomalies_ee,
    'LocalOutlierFactor': anomalies_lof,
    'OneClassSVM': anomalies_ocsvm,
    'DBSCAN': anomalies_dbscan
}

# Display summary of anomalies
for method, anomalies in all_anomalies.items():
    print(f"Anomalies detected by {method}:")
    print(anomalies.head(), "\n")
