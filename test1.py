def a(n):
    res = 0
    cnt = [0] * 10
    while (n > 0):
        rem = n % 10
        cnt[rem] += 1
        n = n // 10
    for i in range(10):
        if (cnt[i] > 1):
            res += 1
    return res


n =
print(a(n))
