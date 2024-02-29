class Polynomial(dict):
    def __getitem__(self, n):
        return self.get(n, 0)
    @property
    def degree(self):
        return max((n for n, a in self.items() if a), default=-1)
    @property
    def derivative(self):
        print(self.degree)
        if self.degree < 0: return self
        return Polynomial({n-1: n*a for n, a in self.items() if n*a})
    def at(self, x):
        return round(sum(a*x**n for n, a in self.items()), 14)

def sgn(x):
    return 1 if x > 0 else -1 if x < 0 else 0

inf = 10**20
def solve(p: Polynomial):
    assert p.degree >= 0, 'Infinitely many solutions'
    if p.degree == 0: return []
    X = [-inf] + solve(p.derivative) + [inf]
    res = set()
    for a, b in zip(X, X[1:]):
        if sgn(p.at(a))*sgn(p.at(b)) > 0: continue
        l, r = a, b
        while l < r:
            h = (l+r)/2
            if p.at(h) == 0: break
            if p.at(h)*sgn(p.at(b)) > 0: r = h
            else: l = h
        res.add(h)
    return sorted(res)

p = Polynomial({3: 3, 2: -6, 0: 1})
print(solve(p))