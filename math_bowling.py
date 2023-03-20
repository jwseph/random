from math import isclose, factorial, sqrt as s
import re
import time

f = lambda x: factorial(int(x)) if x.is_integer() and 0 <= x <= 6 else float('nan')

comm_ops = '+', '*'
ops = '-', '/', '**', '%'

funcs1 = {
    False: [('(', ')'), ('s(', ')')],
    True: [('(', ')'), ('s(', ')'), ('f(', ')')],
}
funcs2 = {
    False: [('', ''), ('(', ')'), ('s(', ')')],
    True: [('', ''), ('(', ')'), ('s(', ')'), ('f(', ')')],
}

def get_exps(nums: set[int], use_fact: bool) -> dict:
    assert len(nums) > 0
    if len(nums) == 1:
        num = next(iter(nums))
        return dict.fromkeys(
            f'{f_l}{num}{f_r}'
            for f_l, f_r in funcs1[use_fact]
        )
    
    res = {}
    for num in nums:
        a_res = get_exps({num}, use_fact)
        b_res = get_exps(nums-{num}, use_fact)
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
        for f_l, f_r in (funcs2 if len(nums) < 3 else funcs1)[use_fact]
    )

def reverse_fact(exp: str) -> str:
    '''
    Converts a string in the format `f(3+5)*f2` to `(3+5)!*2!` (slow!)
    '''
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

def solve(nums: set[int], *, use_fact: bool = True):
    '''
    Prints shortest solutions to `nums` for the integers [1, 10]
    :param use_fact: (False) sqrt only or (True) sqrt and factorial
    '''
    t = time.perf_counter()
    exps = list(get_exps(nums, use_fact))
    print('Sorting', len(exps), 'expressions...')
    exps.sort(key=lambda exp: len(exp)-exp.count('**')-2*int(exp.startswith('(')))
    # Sorting drastically improves speed for most cases,
    # while worsening speed for unsolvable cases

    print('Evaluating', len(exps), 'expressions...')
    res = {(i+1): None for i in range(10)}
    left = len(res)
    for exp in exps:
        try:
            ev = eval(exp)
            num = int(ev+.5)
            if not isclose(ev, num) or not num in res: continue
            if res[num] is None:
                res[num] = exp
                left -= 1
                if left == 0: break
        except:
            pass
    for num, exp in res.items():
        if exp is None: exp = ' '
        exp = exp.replace('**', '^').replace('s', '√')
        exp = re.sub(r'\((\d)\.0\)', r'\1', exp)
        if exp[0] == '(' and exp[-1] ==')':
            exp = exp[1:-1]
        if use_fact: exp = reverse_fact(exp)
        res[num] = exp

    w = max(len(f'{num} = {exp}') for num, exp in res.items())
    print('+'+'-'*(2+w)+'+')
    print('\n'.join(
        '| '+f'{num} = {exp}'.ljust(w)+' |'
        for num, exp in res.items()
    ))
    print('+'+'-'*(2+w)+'+')
    print(f'Completed in {time.perf_counter()-t:.3f}s')


if __name__ == '__main__':
    nums = {float(_) for _ in input('Enter nums (space-separated): ').split()}
    solve(nums, use_fact=True)
