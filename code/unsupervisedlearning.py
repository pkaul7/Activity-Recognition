# -*- coding: utf-8 -*-
"""UnsupervisedLearning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pvACi0MivRIcCMh1mPYox_-LWNeSGka7
"""

#from google.colab import files

"""Importing Libraries"""

import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import model_selection
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from mpl_toolkits.mplot3d import Axes3D


"""# PCA"""

import warnings
warnings.filterwarnings("ignore")
path = 'output_plots'
if not os.path.exists(path):
    os.makedirs(path)

def pca(X):
    X_centered = X-np.mean(X, axis = 0)
    U, S, V = np.linalg.svd(X_centered)
    return U, S, V
    
def intrinsic_dimension(S, recovered_variance=.99):
    S_total = np.sum(np.square(S))
    dim = 0
    temp_total = 0
    for i in np.square(S):
      temp_total += i
      if temp_total < (S_total * recovered_variance):
        dim += 1 
      else:
        return dim+1

def apply_PCA_on_data(X):
  U, S, V = pca(X)
  projection = np.matmul(X, V.T)
  intrinsic_dimensions = intrinsic_dimension(S, 0.99)
  X_pca = projection[:, :intrinsic_dimensions]
  return X_pca

"""# K Means"""

def pairwise_dist(x, y):
    new_y = y.reshape(y.shape[0], 1, y.shape[1])
    dist = np.zeros((x.shape[0], y.shape[0]))
    dist = np.transpose(np.linalg.norm(new_y - x, axis = 2))
    return dist

def init_centers(points, K):
    centers = np.zeros((K, points.shape[1]))
    sample_indices = np.random.randint(0, points.shape[0], K)
    index = 0
    for sample_index in sample_indices:
      centers[index] = points[sample_index]
      index += 1
    return centers

def update_assignment(centers, points):
    distances = pairwise_dist(centers, points)
    cluster_idx = np.argmin(distances, axis = 0)
    return cluster_idx

def update_centers(old_centers, cluster_idx, points):
    k = old_centers.shape[0]
    centers = np.zeros((k, old_centers.shape[1]))
    for cluster in range(k):
      centers[cluster] = np.mean(points[cluster_idx == cluster], axis = 0)
    return centers

def get_loss(centers, cluster_idx, points):
    k = centers.shape[0]
    losses = np.ndarray((k,))
    for cluster in range(k):
      losses[cluster] = np.square(np.linalg.norm(points[cluster_idx==cluster] - centers[cluster]))
    loss = np.sum(losses)
    return loss

def visualize(X, C, K):   
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(X[:,0], X[:,1], X[:,2], c=C,cmap='rainbow')
    plt.title('Visualization of K = '+str(K), fontsize=15)
    return plt
    pass


def main():
  dataset = pd.read_csv('train.csv')
  X, y = dataset.iloc[:, 0:-2], dataset.iloc[:, -1:]
  X_data, y_data = np.array(X), np.array(y)

  print("X shape: ", X_data.shape)
  print("y shape: ", y_data.shape)
  y_unique, y_unique_inverse = np.unique(y_data, return_inverse=True)
  print(y_unique)

  """# Feature Selection"""
  from matplotlib import pyplot as plt
  model = ExtraTreesClassifier()
  model.fit(X,y)
  feat_importances = pd.Series(model.feature_importances_, index=X.columns)
  feat_importances.nlargest(20).plot(kind='bar')
  plt.savefig("output_plots/Feature_Importance.png" , format = 'png')
  plt.clf()
  #fig = feat_importances.get_figure()
  #fig.savefig('feat_importances.png' , format = 'png')

  points = apply_PCA_on_data(X_data)
  max_iters=10000 
  abs_tol=1e-16
  rel_tol=1e-16
  centers = init_centers(points, y_unique.shape[0])

  for it in range(max_iters):
    cluster_idx = update_assignment(centers, points)
    centers = update_centers(centers, cluster_idx, points)
    loss = get_loss(centers, cluster_idx, points)
    K = centers.shape[0]
    if it:
      diff = np.abs(prev_loss - loss)
      if diff < abs_tol and diff / prev_loss < rel_tol:
        break
    prev_loss = loss

  plt  = visualize(points, cluster_idx, y_unique.shape[0])
  plt.savefig("output_plots/K_means.png" , format = 'png')
  plt.clf()
  """# Original mapping for comparison"""

  plt = visualize(points, y_unique_inverse, y_unique.shape[0])
  plt.savefig("output_plots/Before_K_means.png" , format = 'png')
  plt.clf()

if __name__ == "__main__":
  main()
