winning_states = [
    0b111000000,
    0b000111000,
    0b000000111,
    0b100100100,
    0b010010010,
    0b001001001,
    0b100010001,
    0b001010100,
]

dp = {}
def sol(a=0, b=0, m=-1, M=1):
    if (a, b) in dp: return dp[a, b]
    if m >= M: return M
    for state in winning_states:
        if a&state == state: return 1
        if b&state == state: return -1
    if a|b == (1<<9)-1: return 0
    for i in range(9):
        if a&1<<i|b&1<<i: continue
        m = max(m, -sol(b, a|1<<i, -M, -m))
    dp[a, b] = m
    return m