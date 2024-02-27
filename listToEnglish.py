def listToEnglish(l):
    for i in range(len(l)):
        if i != len(l) - 1:
            print(str(l[i])+ ', ', end='')
        else:
            print('and ' + l[i] + '.')

listToEnglish(['dogs',2,-17.5, 'cats'])
