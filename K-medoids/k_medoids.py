import csv
import math
import random


def read_csv_file():
    data = []
    with open('iris.data', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) == 5:
                data.append((float(row[0]), float(row[1]), float(row[2]), float(row[3]), row[4]))
    return data


def calc_dist_sum():
    length = len(iris_data)
    distance_sum = 0
    for i in range(length - 1):
        for j in range(i + 1, length):
            distance_sum += get_euclidean_dist(iris_data[i], iris_data[j], 4)
    return distance_sum


def get_euclidean_dist(data_one, data_two, data_length):
    distance = 0

    for i in range(data_length):
        data_dim_one = data_one[i]
        data_dim_two = data_two[i]
        distance = distance + (data_dim_one - data_dim_two)**2

    distance = math.sqrt(float(distance))

    return distance


def calc_obj_dists(dist_sum):
    length = len(iris_data)
    dist_list = []

    for i in range(length):
        v_dist = 0.0
        for j in range(length):
            v_dist += get_euclidean_dist(iris_data[i], iris_data[j], 4) / dist_sum

        dist_list.append(v_dist)

    return dist_list


def get_cluster_labels():
    results = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    i = 0
    for c in clusters:
        index_one = i
        for data in c:
            index_two = iris_dict[data[4]]
            results[index_one][index_two] += 1
        i += 1

    labels = [0, 0, 0]
    labels[0] = results[0].index(max(results[0]))
    for i in range(len(results)):
        results[i][labels[0]] = 0
    labels[1] = results[1].index(max(results[1]))
    for i in range(len(results)):
        results[i][labels[1]] = 0
    labels[2] = results[2].index(max(results[2]))

    return labels


def assign_data_to_medoids(k):
    temp_medoids = []
    for i in range(k):
        temp_medoids.append(set())

    for data in iris_data:
        min_medoid = find_nearest_medoid(data)
        temp_medoids[min_medoid].add(data)

    return temp_medoids


def find_nearest_medoid(data):
    i = 0
    min_dist = float("inf")
    min_medoid = 0

    # print(seed_points)
    for m in medoids:
        dist = get_euclidean_dist(data, m, 4)
        if dist < min_dist:
            min_dist = dist
            min_medoid = i
        i += 1

    return min_medoid


def calc_obj_medoid_dist_sum():
    dist = 0.0
    i = 0

    for m in medoid_members:
        for data in m:
            dist += get_euclidean_dist(data, medoids[i], 4)
        i += 1

    return dist


def find_new_medoids():
    temp_medoids = []
    for m in medoid_members:
        temp_medoids.append(find_new_medoid(m))

    return temp_medoids


def find_new_medoid(m):
    min_medoid = None
    min_dist = float("inf")

    for test_medoid in m:
        new_dist = 0.0

        for data in m:
            new_dist += get_euclidean_dist(data, test_medoid, 4)

        if new_dist < min_dist:
            min_dist = new_dist
            min_medoid = test_medoid

    return min_medoid


def get_k_means_results(labels):
    results = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    i = 0
    for c in clusters:
        index_one = labels[i]
        for data in c:
            index_two = iris_dict[data[4]]
            results[index_one][index_two] += 1
        i += 1

    return results


def get_results():
    results = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    i = 0
    for m in medoid_members:
        index_one = iris_dict[medoids[i][4]]
        for data in m:
            index_two = iris_dict[data[4]]
            results[index_one][index_two] += 1
        i += 1

    return results


def display_results(results):
    labels = ['Iris-virginica', 'Iris-versicolor', 'Iris-setosa']
    row_format = "{:>20}" * (len(labels) + 1)
    print(row_format.format("", *labels))
    for label, row in zip(labels, results):
        print(row_format.format(label, *row))


def get_new_seed_points():
    new_seed_points = []

    # print(clusters)
    for c in clusters:
        new_seed_points.append(get_mean_point(c))

    return new_seed_points


def get_mean_point(c):
    average = []
    data_length = 0

    for i in range(4):
        average.append(0.0)

    for data in c:
        for i in range(4):
            average[i] += data[i]

    average_tuple = ()
    for i in range(4):
        average[i] = average[i] / len(c)
        average_tuple = average_tuple + (average[i],)

    return average_tuple


def init_seed_points(k):
    seed_points = random.sample(iris_data, k)
    return seed_points


def assign_data_to_clusters(k):
    temp_clusters = []
    for i in range(k):
        temp_clusters.append(set())

    for data in iris_data:
        min_cluster = find_nearest_seed_point(data)
        temp_clusters[min_cluster].add(data)

    return temp_clusters


def find_nearest_seed_point(data):
    i = 0
    min_dist = float("inf")
    min_cluster = 0

    # print(seed_points)
    for sp in seed_points:
        dist = get_euclidean_dist(data, sp, 4)
        if dist < min_dist:
            min_dist = dist
            min_cluster = i
        i += 1

    return min_cluster


iris_dict = {
    'Iris-virginica': 0,
    'Iris-versicolor': 1,
    'Iris-setosa': 2
}

iris_data = read_csv_file()

# K-Means
clusters = set()
seed_points = init_seed_points(3)
iterations = 0
while True:
    iterations += 1
    new_clusters = assign_data_to_clusters(3)
    if new_clusters == clusters:
        break
    clusters = new_clusters
    seed_points = get_new_seed_points()

labels = get_cluster_labels()
results = get_k_means_results(labels)
print("K-MEANS")
display_results(results)
print()

# K-Medoid
dist_sum = calc_dist_sum()
dist_list = calc_obj_dists(dist_sum)
length = len(dist_list)

for i in range(length):
    iris_data[i] += (dist_list[i],)

iris_data.sort(key=lambda tup: tup[5])

medoids = [iris_data[0], iris_data[1], iris_data[2]]
medoid_members = assign_data_to_medoids(3)
obj_medoid_dist_sum = calc_obj_medoid_dist_sum()


while True:
    medoids = find_new_medoids()
    medoid_members = assign_data_to_medoids(3)
    new_obj_medoid_dist_sum = calc_obj_medoid_dist_sum()
    if new_obj_medoid_dist_sum == obj_medoid_dist_sum:
        break
    obj_medoid_dist_sum = new_obj_medoid_dist_sum

results = get_results()
print("K-MEDOIDS")
display_results(results)
