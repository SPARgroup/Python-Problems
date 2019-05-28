from time import sleep

def animatedPrint(s, speed, rate):
    rate /= 1000
    for char in s:
        print (char, end="", flush=True)
        if char != ' ':
            sleep(1/speed)

        speed += speed * rate

def custom_input(string, speed = 20, rate = 5):
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