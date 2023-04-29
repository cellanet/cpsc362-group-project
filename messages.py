import random

def reply_message(string):
    p_string = string.lower()

    reply_list = [
                  "W/n - (Simple love - obito) ( Remix) , Cover Duongg , Titie", 
                  "Heartbreaker - GDragon",
                  "On My own - Ashes Remain", 
                  "Black Swan - BTS", 
                  "Bo Xi Bo - Hoang Thuy Linh", 
                  "Rumble - Skillrex",
                  "Hey Jude - The Beatles",
                  "Pink + White - Frank Ocean", 
                  "Runaway - Kanye West"
                  ]
    
    if p_string == '!help':
        return "Toss me a string and I will give you a music genre"
    else:
        return random.choice(reply_list)

