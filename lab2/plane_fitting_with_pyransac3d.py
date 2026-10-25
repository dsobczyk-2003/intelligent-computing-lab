# lab2 - sprawdzenie DBSCAN zamiast k-means i pyransac3d zamiast RANSAC
import numpy as np
from sklearn.cluster import DBSCAN
import csv
import pyransac3d as pyrsc

# ----------- wczytywanie pliku z punktami -----------
points = []
with open('C:/Users/User/Desktop/intelligent-computing-lab/lab1/LidarData.xyz', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, y, z in reader:
        points.append((float(x), float(y), float(z)))

# ------ DBSCAN - sam znajduje liczbę grup oraz punkty lezace blisko siebie ------
# eps - zasięg w którym znajduje sąsiadów, min_samples - minimalna gestosc (kiedy za duzy chmury beda szumem)
clusterer = DBSCAN(eps=1, min_samples=2)
X = np. array(points)
y_pred = clusterer.fit_predict(X)
print(np.unique(y_pred, return_counts=True))
plane = pyrsc.Plane()


for label in range(3):
    cloud = X[y_pred == label]
    print('Cloud', label)
    best_eq, best_inliers = plane.fit(cloud, thresh=0.1, maxIteration=100)
    print(best_eq, len(best_inliers))

    ratio = len(best_inliers)/len(cloud)

    if ratio < 0.5:
        print('Powierzchnia cylindryczna')
    elif abs(best_eq[2]) > 0.9:
        print('Powierzchnia płaska pozioma')
    elif abs(best_eq[2]) < 0.1:
        print('Powierzchnia płaska pionowa')
    else:
        print('Płaszczyzna nie wykryta')
