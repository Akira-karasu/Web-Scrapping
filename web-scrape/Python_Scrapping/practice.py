def func(y):
    return y


long_text = str(input('Enter a long text to convert it into a List: '))

lst = list(map(func, long_text))

counter = {
    'vowels':0,
    'non-vowels':0,
    'upper_case':0,
    'lower_case':0
}

for x in lst:

    if x in ['A', 'E', 'I', 'O', 'U'] or x in ['a', 'e', 'i', 'o', 'u'] :
        counter['vowels'] += 1
    else:
        counter['non-vowels'] += 1

    if x in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
        counter['upper_case'] += 1
    else:
        counter['lower_case'] += 1

print('Vowels: ', counter['vowels'])
print('Non-Vowels: ', counter['non-vowels'])
print('Uppercase: ', counter['upper_case'])
print('Lowercase: ', counter['lower_case'])


