def isItHonza(name):
    return name == 'Honza'


def honzaAction():
    return 'go to work!'


def isItLucie(name):
    return name == 'Lucie'


def lucieAction():
    return 'go to school!'


touples = [
    (isItHonza, honzaAction),
    (isItLucie, lucieAction),
    (lambda x: True, lambda:'nothing')
]


for condition, action in touples:
    if condition('Honza'):
        print(action())


print('end')
