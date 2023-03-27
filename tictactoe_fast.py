win = [
    (0b000000111, 0b001001001, 0b100010001),
    (0b000000111, 0b010010010),
    (0b000000111, 0b100100100, 0b001010100),
    (0b000111000, 0b001001001),
    (0b000111000, 0b010010010, 0b100010001, 0b001010100),
    (0b000111000, 0b100100100),
    (0b111000000, 0b001001001, 0b001010100),
    (0b111000000, 0b010010010),
    (0b111000000, 0b100100100, 0b100010001),
    (),
]

# Use a<<9|b for dp hash in other languages
dp = {}
def sol(a=0, b=0, m=-1, M=1, l=9):
    if (a, b) in dp: return dp[a, b]
    for s in win[l]:
        if b&s == s: return -1
    if a|b == (1<<9)-1: return 0
    r = -2
    for i in range(9):
        if (a|b)&1<<i: continue
        r = max(r, -sol(b, a|1<<i, -M, -m, i))
        m = max(m, r)
        if m >= M: break
    dp[a, b] = r
    return r

def winner(a, b):
    for i in range(9):
        for s in win[l]:
            if a&s == s: return 1
            if b&s == s: return -1
    return 0

def tie(a, b):
    return a|b == (1<<9)-1

if __name__ == '__main__':
    import timeit
    print(timeit.Timer(sol).timeit(1))
