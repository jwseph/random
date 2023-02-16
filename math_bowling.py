from math import log10 as log, sqrt, factorial, gamma, isclose

# fact = lambda x: gamma(x+1)
fact = lambda x: factorial(x) if x.is_integer() and x >= 0 else float('nan')
fact_log = lambda x: fact(log(x))

comm_ops = '+', '*'
ops = '-', '/', '^'
funcs = ('', ''), ('log(', ')'), ('sqrt(', ')'), ('fact(', ')'), ('fact(sqrt(', '))')

def get_exps(nums: set[int]):
    assert len(nums) > 0
    if len(nums) == 1:
        return [
            f'{f_l}{next(iter(nums))}{f_r}'
            for f_l, f_r in funcs
        ]
    
    res = []
    for num in nums:
        a_res = get_exps({num})
        b_res = get_exps(nums-{num})
        for op in comm_ops:
            for a in a_res:
                for b in b_res:
                    res.append(a+op+b)
        for op in ops:
            for a in a_res:
                for b in b_res:
                    res.append(a+op+b)
                    res.append(b+op+a)
    return [
        f'{f_l}{_}{f_r}'
        for _ in res
        for f_l, f_r in funcs
    ]

print(eval('((5)+((2)/fact_log(7)))'))
print(eval('5+2/fact_log(7)'))
print(eval('fact_log(7)'))

# print(len(get_exps({2, 5, 7})))
for exp in get_exps({2, 5, 7}):
    try:
        if isclose(eval(exp), 5):
            print(exp)
            break
    except:
        ...