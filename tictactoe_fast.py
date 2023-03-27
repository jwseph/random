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
    if m >= M: return m
    for s in win[l]:
        if b&s == s: return -1
    if a|b == (1<<9)-1: return 0
    for i in range(9):
        if a&1<<i|b&1<<i: continue
        m = max(m, -sol(b, a|1<<i, -M, -m, i))
        if m >= M: break
    dp[a, b] = m
    return m

import timeit
print(timeit.Timer(sol).timeit(1))