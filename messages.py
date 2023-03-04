import random

def reply_message(string):
    p_string = string.lower()

    reply_list = ["Have you tried polka? It's a real crowd-pleaser.", "I recommend silence. It's the most underrated genre out there.",
                  "Definitely go for something super mainstream and generic. You'll fit right in.", "Here: Jazz! NOW LEAVE ME ALONE.", 
                  "You HAVE to try synthwave! It's the perfect blend of nostalgia and futuristic vibes.", "Why bother? It's all just noise anyway.",
                  "Uhhh, I don't know... what kind of music do you like?", "Have you heard of Mongolian throat singing? It's... interesting, to say the least.",
                  "How about sea shanties? They're making a comeback, you know.", "Why not just listen to whatever's on the radio?"]
    
    if p_string == '!help':
        return "Toss me a string and I will give you a music genre"
    else:
        return random.choice(reply_list)

