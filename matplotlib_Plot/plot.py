import matplotlib.pyplot as plt


def plot():
    time = [1, 2, 3, 4, 5]
    activities = [10, 20, 40, 35, 30]
    plt.plot(time, activities)
    plt.show()


def scatter():
    time = [1, 2, 3, 4, 5]
    activities = [10, 20, 40, 35, 30]
    plt.scatter(time, activities)
    plt.show()


def hist():
    time = [1, 2, 3, 4, 5]
    activities = [10, 20, 30, 40, 50]
    plt.hist(time, bins=5)
    plt.show()


if __name__ == '__main__':
    hist()