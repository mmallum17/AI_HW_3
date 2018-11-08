import csv
import random
import math


def read_csv_file():
    crime_data = []
    with open('hw3-crime_data.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_line = True
        for row in csv_reader:
            if not first_line:
                crime_data.append((float(row[2]), float(row[3]), float(row[4]), float(row[5])))
            first_line = False
    return crime_data


def init_seed_points(k):
    seed_points = random.sample(crime_data, k)
    return seed_points


def assign_data_to_clusters(k):
    temp_clusters = []
    for i in range(k):
        temp_clusters.append(set())

    for data in crime_data:
        min_cluster = find_nearest_seed_point(data)
        temp_clusters[min_cluster].add(data)

    return temp_clusters


def find_nearest_seed_point(data):
    i = 0
    min_dist = float("inf")
    min_cluster = 0

    # print(seed_points)
    for sp in seed_points:
        dist = get_euclidean_dist(data, sp)
        if dist < min_dist:
            min_dist = dist
            min_cluster = i
        i += 1

    return min_cluster


def get_euclidean_dist(data, sp):
    length = len(data)
    distance = 0
    # print(data)
    # print(sp)

    for i in range(length):
        data_one = data[i]
        data_two = sp[i]
        distance = distance + (data_one - data_two)**2

    # print(distance)
    distance = math.sqrt(float(distance))

    return distance


def get_new_seed_points():
    new_seed_points = []

    # print(clusters)
    for c in clusters:
        new_seed_points.append(get_mean_point(c))

    return new_seed_points


def get_mean_point(c):
    average = []
    data_length = 0

    for data in c:
        data_length = len(next(iter(c)))
        break

    for i in range(data_length):
        average.append(0.0)

    for data in c:
        for i in range(data_length):
            average[i] += data[i]

    average_tuple = ()
    for i in range(data_length):
        average[i] = average[i] / len(c)
        average_tuple = average_tuple + (average[i],)

    return average_tuple


def get_distortion():
    distortion = 0.0
    i = 0

    for c in clusters:
        for data in c:
            distortion = distortion + (get_euclidean_dist(data, seed_points[i]))**2
        i += 1

    return distortion


for k in range(2, 7):
    clusters = set()
    crime_data = read_csv_file()
    seed_points = init_seed_points(k)
    iterations = 0
    while True:
        iterations += 1
        new_clusters = assign_data_to_clusters(k)
        if new_clusters == clusters:
            break
        clusters = new_clusters
        seed_points = get_new_seed_points()
    distortion = get_distortion()
    print("K = " + str(k) + ", distortion = " + str(distortion) + ", iterations = " + str(iterations))
