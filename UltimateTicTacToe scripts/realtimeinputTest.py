import msvcrt as ms

#Testing realtime input
while(1):
    print(ms.kbhit())
    if ms.kbhit():
        print(ms.getch().decode("utf-8"))
        input()
