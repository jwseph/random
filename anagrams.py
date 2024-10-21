A = {}

def get(s):
    return A.setdefault(' '.join(sorted(s)), [])

for s in open('word_hunt.txt').read().split():
    get(s).append(s)

print('Loaded words')

while True:
    s = input()
    B = get(s)[:]
    if s in B: B.remove(s)
    print(' '.join(B) or 'No solution')