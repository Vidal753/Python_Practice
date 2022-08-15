import pandas


def iterate_2d_pandas():
    """
    With iterrows() method you can have acces to the label and the row of the pandas dictionary
    """
    score = {'phone': ['S10', 'S20', 'S21', 'S22'], 'storage': [128, 128, 256, 512], 'price': [300, 600, 800, 1200]}
    pd_score = pandas.DataFrame(score, index=['VIDAL', 'OSCAR', 'CESAR', 'KEYLING'])

    for lab, row in pd_score.iterrows():
        print(f'{lab}: {row["phone"]}')


def add_columns_pandas():
    score = {'phone': ['S10', 'S20', 'S21', 'S22'], 'storage': [128, 128, 256, 512], 'price': [300, 600, 800, 1200]}
    pd_score = pandas.DataFrame(score, index=['VIDAL', 'OSCAR', 'CESAR', 'KEYLING'])

    for lab, row in pd_score.iterrows():
        pd_score.loc[lab, 'phone_lower'] = row['phone'].lower()

    print(pd_score)


def add_columns_pandas_apply():
    """
    You can apply changes for columns or rows using apply, in this example we applied lower.
    """
    score = {'phone': ['S10', 'S20', 'S21', 'S22'], 'storage': [128, 128, 256, 512], 'price': [300, 600, 800, 1200]}
    pd_score = pandas.DataFrame(score, index=['VIDAL', 'OSCAR', 'CESAR', 'KEYLING'])

    pd_score['phone_lower'] = pd_score['phone'].apply(str.lower)

    print(pd_score)


def max_with_2_parameters():
    """
    When you pass 2 parameter to max function, the first is the smaller value that you want,
    and the other parameter is the change that you apply to the variable.
    """
    num = 4
    for x in range(5):
        num = max(1, num - 1)
        print(num)


if __name__ == '__main__':
    max_with_2_parameters()
