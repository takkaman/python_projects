# Double Up version 4 - finished on 7 May 2018

# input username
username = raw_input("Please enter your name:")
print username, ", welcome to Double Up! Let's play!"
money = 1

# init count
corr_num = 0
incorr_num = 0
skip_num = 0
has_incorr_answer = False

# provide file name
qa_file = "DoubleUpQuestions-by-StudentNumber.txt"
rpt_file = "DoubleUpReport-by-StudentNumber.txt"
question_list = []
answer_list = []
# store questions/answers in list

i = 0
with open(qa_file) as fp:
    for line in fp.readlines():
        line = line.strip("\n")
        if i % 2 == 0: # question line
            question_list.append(line)
        else: # answer line
            answer_list.append(line)
        i+=1
    fp.close()

# user_answer = raw_input("Is the earth flat?")
# answer = "n"
# # process multiple questions

for i in range(len(question_list)):
    # provide Q&A
    user_answer = raw_input(question_list[i])
    answer = answer_list[i]
    if user_answer.lower() == answer:
        money *= 2
        corr_num += 1
        print "Correct answer, your money has been doubled."
        print "Now you have $"+str(money)
    elif user_answer.lower() == 's':
        skip_num += 1
        print "Question skipped."
        print "Now you have $"+str(money)
    else:
        has_incorr_answer = True
        incorr_num += 1
        money = 1
        print "Incorrect answer, your money has been reset to $1."

    if has_incorr_answer: break

# print end message
print "GAME OVER!"


# write report into file
with open(rpt_file, 'a') as fp:
    print "Thank you for playing Double Up, ", username
    print "You have won $"+str(money)
    print "You answered "+str(corr_num) + " questions correctly."
    print "You answered "+str(incorr_num) + " questions incorrectly."
    print "You skipped "+str(skip_num) + " questions."
    fp.write("Thank you for playing Double Up, "+username+"\n")
    fp.write("You have won $"+str(money)+"\n")
    fp.write("You answered "+str(corr_num) + " questions correctly."+"\n")
    fp.write("You answered "+str(incorr_num) + " questions incorrectly."+"\n")
    fp.write("You skipped "+str(skip_num) + " questions."+"\n")
    fp.close()


