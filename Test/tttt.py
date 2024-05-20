import sys
from math import sqrt

class Node:
    def __init__(self, idx, pre_val):
        self.idx = idx
        self.pre_val = pre_val


q = [Node(1, 0)]
sz = 0

def cal(x, i, val):
    global sz
    if x < 1 or x > sz:
        return 2e5 ** 4
    return q[x].pre_val + (i - q[x].idx + 1) ** 4 + val


def solve():
    global sz
    n, m = map(int, input().split())
    arr = [0] * (n + 1)
    f = [0] * (m + 1)
    idx = 1
    t = input().split()
    for i in t:
        arr[idx] = int(i)
        idx += 1

    sz = 1
    q.append(Node(1, 0))

    for i in range(1, m + 1):
        l, r = 1, sz
        while r > l:
            lmid = l + (r - l) // 3
            rmid = r - (r - l) // 3
            lans = cal(lmid, i, arr[i])
            rans = cal(rmid, i, arr[i])
            if lans <= rans:
                r = rmid - 1
            else:
                l = lmid + 1

        f[i] = int(min(cal(l, i, arr[i]), cal(r, i, arr[i])))

        while sz > 0 and q[sz].pre_val >= f[i]:
            q.pop()
            sz -= 1
        sz += 1
        q.append(Node(i + 1, f[i]))

    print(f[m])


if __name__ == "__main__":
    solve()