# Double Up version 1 - finished on 7 May 2018

# input username
username = raw_input("Please enter your name:")
print username, ", welcome to Double Up! Let's play!"
money = 1

# provide Q&A
user_answer = raw_input("Is the earth flat?")
answer = "n"
if user_answer.lower() == answer:
    money *= 2
    print "Correct answer, your money has been doubled."
    print "Now you have $"+str(money)

else:
    print "Incorrect answer, your money has been reset to $1."
    money = 1

# print end message
print "GAME OVER"
print "Thank you for playing Double Up, ", username
print "You have won $"+str(money)
