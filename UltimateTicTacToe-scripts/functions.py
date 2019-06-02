from time import sleep

def animatedPrint(s, speed, rate):
    rate /= 1000
    for char in s:
        print (char, end="", flush=True)
        if char != ' ':
            sleep(1/speed)

        speed += speed * rate

def custom_input(string, speed = 30, rate = 10):
    animatedPrint(string,speed, rate )
    k = input()
    return k

def ask_for_account():
    if n_1 in yes:
        jid = input("\nEnter your User ID: ")
        password = input("Enter Password: ")

    else:
        print("\nYou will have to make an XMPP/Jabber account to play the game...\n")
        print("Opening Registration link in 3 seconds...")
        time.sleep(3)
        web.open("https://www.xmpp.jp/signup")
        jid = func.custom_input("\nEnter your User ID: ")
        password = input("Enter Password: ")

def play_intro():
    intro = "Ultimate TicTacToe Online\n        v2.1"
    animatedPrint(intro, 30, 20)
    sleep(0.5)
    print("\n[Requires an internet connection to play a saved game]")
    sleep(0.2)
    creds = "\nCredits: Samarth Singla | Ashmit Chamoli | Rishabh Sharma | Abhivir Singh\n"
    animatedPrint(creds, 80, 5)
    sleep(0.5)