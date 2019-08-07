for i in range(int(input())):
    n = int(input())
    c = [int(j) for j in input().split()]
    rad = [0]*n
    z = [int(k) for k in input().split()]
    for index in range(n):
        low = max(0,index-c[index])
        high = min(n-1,index+c[index])+1

        rad[low:high]=[m+1 for m in rad[low:high]]

