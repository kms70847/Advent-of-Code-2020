def iter_game(nums):
    d = {}
    turn = 0
    last = None
    while True:
        if turn < len(nums):
            value = nums[turn]
        elif last not in d:
            value = 0
        else:
            value = turn - 1 - d[last]
        d[last] = turn - 1
        yield value
        last = value
        turn += 1

def state(nums, turn):
    i = 0
    for x in iter_game(nums):
        i += 1
        if i == turn:
            return x

assert state([0,3,6], 2020) ==  436
assert state([1,3,2], 2020) ==    1
assert state([2,1,3], 2020) ==   10
assert state([1,2,3], 2020) ==   27
assert state([2,3,1], 2020) ==   78
assert state([3,2,1], 2020) ==  438
assert state([3,1,2], 2020) == 1836

print(state([0,8,15,2,12,1,4], 2020))
print(state([0,8,15,2,12,1,4], 30_000_000))
