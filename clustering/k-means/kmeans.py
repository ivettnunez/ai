import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans


# import dataset
data = pd.read_csv("./players5.csv")

# K-Means clustering setup
km = KMeans(n_clusters=3, #number of clusters
            init='k-means++', # initialization method
            n_init=10, # number of times the k-means algorithm will be run with different centroid seeds
            max_iter=300, # maximum number of iterations for each run
            tol = 1e-4, #tolerance for convergence
            random_state=0 # to control the random number generator
            ).fit(data) # compute K-Means clustering


# print class assgined for each sample
#print(km.labels_)
# print cluster centers
#print(km.cluster_centers_)

# get cluster labels for new data
new_data = pd.read_csv("./players6.csv")
y_km = km.fit_predict(new_data)
X = new_data


# plot Shots respect Time on ice
plt.scatter(X[y_km==0]['TOI/GP'], X[y_km==0]['S'], label='Cluster 1', c='lightgreen', marker='o')
plt.scatter(X[y_km==1]['TOI/GP'], X[y_km==1]['S'], label='Cluster 2', c='purple', marker='o')
plt.scatter(X[y_km==2]['TOI/GP'], X[y_km==2]['S'], label='Cluster 3', c='orange', marker='o')
plt.scatter(km.cluster_centers_[:,0] ,km.cluster_centers_[:,1], color='black',  marker='*')

plt.legend()
plt.xlabel('Time on ice (min)')
plt.ylabel('Shots')
plt.show()

#plot Points per game respect Time on ice
plt.scatter(X[y_km==0]['TOI/GP'], X[y_km==0]['P/GP'], label='Cluster 1', c='lightgreen', marker='o')
plt.scatter(X[y_km==1]['TOI/GP'], X[y_km==1]['P/GP'], label='Cluster 2', c='purple', marker='o',)
plt.scatter(X[y_km==2]['TOI/GP'], X[y_km==2]['P/GP'], label='Cluster 3', c='orange', marker='o')

plt.legend()
plt.xlabel('Time on ice (min)')
plt.ylabel('Points per game')
plt.show()

#plot Points respect Time on ice
plt.scatter(X[y_km==0]['TOI/GP'], X[y_km==0]['Points'], label='Cluster 1', c='lightgreen', marker='o')
plt.scatter(X[y_km==1]['TOI/GP'], X[y_km==1]['Points'], label='Cluster 2', c='purple', marker='o')
plt.scatter(X[y_km==2]['TOI/GP'], X[y_km==2]['Points'], label='Cluster 3', c='orange', marker='o')

plt.legend()
plt.xlabel('Time on ice (min)')
plt.ylabel('Points')
plt.show()
