n = int(input())
fams = []
money = 0
done = False

for i in range(n):
    fams.append([int(i) for i in input().split()])

time = 0


def key(fam):
    global time
    left = fam[1] - time

    if left > 0:
        return fam[0] / left
    else:
        return 0


# fams.sort(reverse = True, key = key)
tt = 0
while tt < n:
    scores = [key(i) for i in fams]
    print(scores)
    maxi = scores.index(max(scores))
    print(maxi)
    if scores[maxi] != 0:
        money += fams[maxi][0]
        time += 1
        print("HO")
    tt += 1
print(money)