# -*- coding: utf-8 -*-
"""
Created on Sat May  4 14:35:46 2019

@author: SAM
"""

from os import system

def check(s):
    if len(s) != 4 :
        return False
    
    for i in range(4):
        for j in range (i + 1, 4):
            if s[i] == s[j]:
                return False
    return True
    
main_word = input("Main word: ")
while not(check(main_word)):
    main_word = input(" Invalid Word, Enter Main word: ")

won = False
system("cls")
a =""
counter = 1
try:    
        while a != main_word and counter <= 10:
            
            if(counter <= 10):
                cows=bulls=0
                
                print("Try", counter, ": ")
                a = input()
                if a == main_word:
                    won = True
                while not(check(a)):
                    a = input(" Invalid Word, Enter your try: ")
                for i in range(4):
                    for j in range(4):
                        if a[i] == main_word[j]:
                            if i == j:
                                bulls += 1

                            else:
                                cows += 1
                        else:
                            continue
                counter += 1
                print (cows, "Cows, ", bulls, "Bulls\n")
            else:
                print("Destiny arrives all the same. I hope they remember you")
   
            
finally:
    if won:
        print ("Victory Royale! You took ",counter-1," tries") 
    else:
        print("Destiny arrives all the same. I hope they remember you. The word is: ", main_word)
    input()
