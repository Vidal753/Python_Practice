def un_pack():
    """Unpack: In python you unpack passing the same amount of element of the list in variables.
     You can unpack the information of list, tuple and dictionary with this form"""

    dictionary_example = {"hey": 1, "hello": 2, "hi": 3}
    list_example = [1, 2, 3]
    tuple_example = (1, 2, 3)
    a, b, c = dictionary_example
    print(a, b, c)


if __name__ == '__main__':
    un_pack()
