#lab2 - dopasowanie płaszczyzn do chmur (k-means +RANSAC)
import csv
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np


# ----------- wczytywanie pliku z punktami -----------
points = []
with open('C:/Users/User/Desktop/intelligent-computing-lab/lab1/LidarData.xyz', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, y, z in reader:
        points.append((float(x), float(y), float(z)))

# ---------- podział na 3 rozłączne chmury k-means -------
clusterer = KMeans(n_clusters=3)
X = np. array(points)
y_pred = clusterer.fit_predict(X)


red = y_pred == 0
blue = y_pred == 1
cyan = y_pred == 2

# -------- wykres 2D z punktami (ośXY) --------------
plt.figure()
plt.scatter(X[red, 0], X[red, 1], c="r")
plt.scatter(X[blue, 0], X[blue, 1], c="b")
plt.scatter(X[cyan, 0], X[cyan, 1], c="c")
plt.show()



def ransac(cloud, thresh=0.1, iterations=100):
    best_inliers = []
    best_W = None #wektor normalny
    best_D = None #przesunięcie

    for i in range(iterations):
        idx = np.random.choice(len(cloud), 3, replace=False)

        numer_a = idx[0]
        numer_b = idx[1]
        numer_c = idx[2]

        A = cloud[numer_a]
        B = cloud[numer_b]
        C = cloud[numer_c]

        vec_A = A - C
        vec_B = B - C

        vec_uA = vec_A / np.linalg.norm(vec_A)
        vec_uB = vec_B / np.linalg.norm(vec_B)

        W = np.cross(vec_uA, vec_uB)
        W = W / np.linalg.norm(W)
        D = -np.sum(np.multiply(W, C))
        distance_all_points = (W[0] * cloud[:, 0] + W[1] * cloud[:, 1] + W[2] * cloud[:, 2] + D) / np.linalg.norm(W)
        inliers = np.where(np.abs(distance_all_points) <= thresh)[0]

        if len(inliers) > len(best_inliers):
            best_inliers = inliers
            best_W = W
            best_D = D

    print(best_W, best_D, len(best_inliers))
    return best_W, best_D, best_inliers

# ------- sprawdzenie każdej z chmur ----------
for label in range(3):
    cloud = X[y_pred == label]
    print('Cloud', label)
    best_W, best_D, best_inliers = ransac(cloud)

    ratio = len(best_inliers)/len(cloud)

    if ratio < 0.5:
        print('Powierzchnia cylindryczna')
    elif abs(best_W[2]) > 0.9:
        print('Powierzchnia płaska pozioma')
    elif abs(best_W[2]) < 0.1:
        print('Powierzchnia płaska pionowa')
    else:
        print('Płaszczyzna nie wykryta')



