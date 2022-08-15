def enumerate_use():
    """
    Enumerate function allow get the index of iterable container like list, tuple and dictionary.
    """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for index, day in enumerate(days):
        print(f'Position: {index}, Day: {day}')


def iterate_2d_list():
    phones = [['S10', 300], ['S20', 600], ['S21', 800], ['S22', 1300]]
    for name, price in phones:
        print(f'Phone model: {name}, Price: ${price}')


def iterate_dictionary():
    """
    You need use the method items to get the key and the value at the same time
    in a dictionary.
    """
    computer = {'asus': 1000, 'msi': 1200, 'alienware': 1500}

    for name, price in computer.items():
        print(f'Computer mark: {name}, Price: {price}')


if __name__ == '__main__':
    enumerate_use()
