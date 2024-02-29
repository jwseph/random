S = input('Enter the coordinates of the vertices of a polygon\nExample (5x5 square): (0, 0), (0, 5), (5, 5), (5, 0)\n> ')
X = map(float, ''.join(filter('0123456789,'.__contains__, S)).split(','))
V = list(zip(*2*[iter(X)]))
A = .5*abs(sum(a*d-b*c for (a, b), (c, d) in zip(V, V[1:]+[V[0]])))
print(f'Area: {A}')