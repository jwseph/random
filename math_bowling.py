# Todo speed optimization: sort all the exps in order from shortest to longest, then break after all the numbers have been solved
# - Around the same speed for difficult cases but much faster for easy cases

from math import isclose, factorial, sqrt as s
import re
import time

f = lambda x: factorial(int(x)) if x.is_integer() and 0 <= x <= 6 else float('nan')

comm_ops = '+', '*'
ops = '-', '/', '**', '%'

funcs1 = [('', ''), ('s(', ')')], [('', ''), ('s(', ')'), ('f(', ')')]

funcs2 = [('', ''), ('(', ')'), ('s(', ')')], [('', ''), ('(', ')'), ('s(', ')'), ('f(', ')')]

def get_exps(nums: set[int], mode: int):
    assert len(nums) > 0
    if len(nums) == 1:
        num = next(iter(nums))
        return dict.fromkeys(
            f'{f_l}{num}{f_r}'
            for f_l, f_r in funcs1[mode]
        )
    
    res = {}
    for num in nums:
        a_res = get_exps({num}, mode)
        b_res = get_exps(nums-{num}, mode)
        for op in comm_ops:
            for a in a_res:
                for b in b_res:
                    res[a+op+b] = None
        for op in ops:
            for a in a_res:
                for b in b_res:
                    res[a+op+b] = None
                    res[b+op+a] = None
    return dict.fromkeys(
        f'{f_l}{_}{f_r}'
        for _ in res
        for f_l, f_r in (funcs2 if len(nums) < 3 else funcs1)[mode]
    )

def reverse_fact(exp):
    res = ''
    s = []
    for ch in exp:
        if ch == 'f':
            s.append('f')
            continue
        if ch == '(': s.append('(')
        if ch == ')': s.pop()
        res += ch
        if s and s[-1] == 'f':
            res += '!'
            s.pop()
    return res

def solve(nums: set[int], *, mode: int):
    t = time.perf_counter()

    exps = get_exps(nums, mode)
    print('Evaluating', len(exps), 'expressions...')

    res = {(i+1): None for i in range(10)}
    for exp in exps:
        try:
            ev = eval(exp)
            num = int(ev+.5)
            exp = exp.replace('**', '^').replace('.0', '')
            exp = re.sub(r'(s|f)\((\d)\)', r'\1\2', exp)
            if mode == 1: exp = reverse_fact(exp)
            if not isclose(ev, num) or not num in res: continue
            if res[num] is None or len(exp) < len(res[num]):
                res[num] = exp
        except:
            pass
    for num, exp in res.items():
        if res[num] is None: exp = ''
        res[num] = exp.replace('s', '√')

    w = max(len(f'{num} = {exp}') for num, exp in res.items())
    print('+'+'-'*(2+w)+'+')
    print('\n'.join(
        '| '+f'{num} = {exp}'.ljust(w)+' |'
        for num, exp in res.items()
    ))
    print('+'+'-'*(2+w)+'+')
    print(f'Time taken: {time.perf_counter()-t:.3f}s')

if __name__ == '__main__':
    # nums = {float(_) for _ in input('Enter nums (space-separated): ').split()}
    # solve(nums, mode=1)
    # exit()
    for a in range(1, 10):
        for b in range(a+1, 10):
            for c in range(b+1, 10):
                print([a, b, c])
                solve({a, b, c}, mode=1)