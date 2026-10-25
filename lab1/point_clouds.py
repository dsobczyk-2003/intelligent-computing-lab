from scipy.stats import norm, uniform
from csv import writer
import numpy as np
# norm to rozkład normalny, wartości skupiają się wokół środka (loc) a scale mówi jak bardzo się rozrzucają
# uniform rozkład jednostajny, loc to początek przedziału a scale to długość

def generate_horizontal_plane(width, length, num_points:int=2000):
    distribution_x = uniform(loc=-width/2, scale=width)
    distribution_y = uniform(loc=-length/2, scale=length)
    distribution_z = norm(loc=0.2, scale=0.05)

    x = distribution_x.rvs(size=num_points)
    y = distribution_y.rvs(size=num_points)
    z = distribution_z.rvs(size=num_points)

    points = zip (x, y, z)
    return points


def generate_vertical_plane(width, height, num_points:int=2000):
    distribution_x = uniform(loc=-width/2, scale=width)
    distribution_y = norm(loc=20, scale=0.05)
    distribution_z = uniform(loc=0, scale=height)

    x = distribution_x.rvs(size=num_points)
    y = distribution_y.rvs(size=num_points)
    z = distribution_z.rvs(size=num_points)

    points = zip (x, y, z)
    return points


def generate_cylinder(radius, height, num_points:int=2000):
    distribution_theta= uniform(loc=0, scale=np.pi * 2)
    distribution_z = uniform(loc=0, scale=height)

    theta = distribution_theta.rvs(size=num_points)
    z = distribution_z.rvs(size=num_points)

    x = np.cos(theta) * radius +15 #dodaje 15 żeby odsunąć od pozostałych chmur
    y = np.sin(theta) * radius +15

    points = zip(x, y, z)
    return points


if __name__ == '__main__':
    cloud_points_horizontal = generate_horizontal_plane(10, 5, 2000)
    cloud_points_vertical = generate_vertical_plane(10, 20, 2000)
    cloud_points_cylinder = generate_cylinder(5, 15, 2000)
    with open ('LidarData.xyz', 'w', encoding='utf-8', newline='\n') as csvfile:
        csvwriter = writer(csvfile)
        for h in cloud_points_horizontal:
            csvwriter.writerow(h)
        for v in cloud_points_vertical:
            csvwriter.writerow(v)
        for c in cloud_points_cylinder:
            csvwriter.writerow(c)
