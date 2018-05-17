# Double Up version 2 - finished on 7 May 2018

# input username
username = raw_input("Please enter your name:")
print username, ", welcome to Double Up! Let's play!"
money = 1

# init count
corr_num = 0
incorr_num = 0
skip_num = 0

# provide Q&A
user_answer = raw_input("Is the earth flat?")
answer = "n"
if user_answer.lower() == answer:
    money *= 2
    corr_num += 1
    print "Correct answer, your money has been doubled."
    print "Now you have $"+str(money)
elif user_answer.lower() == 's':
    print "Question skipped."
    print "Now you have $"+str(money)
    skip_num += 1
else:
    incorr_num += 1
    money = 1
    print "Incorrect answer, your money has been reset to $1."

# print end message
print "GAME OVER!"
print "Thank you for playing Double Up, ", username
print "You have won $"+str(money)
print "You answered "+str(corr_num) + " questions correctly."
print "You answered "+str(incorr_num) + " questions incorrectly."
print "You skipped "+str(skip_num) + " questions."

