file = open("journal.txt", "w+")
file.write("hello world \n")
file.close()

file = open("journal.txt", "a+") #plus sign means will create file if it does
#not exist alr
for i in range(2):
    file.write("yay \n")

file = open("journal.txt", "r")
if (file.mode == "r"):
    contents = file.read()
    print(contents)

date = open("date.txt", "r")
reading = date.read()
print(reading)
#how to store entries in journal:
#store month and date, if restart, add new date to journal.txt
#each entry gets stored as a new line
#idk how to associate each entry w a day though..
#f = open("journal.txt", "a+")

#for journal... how should i increase date
#have var that stores previous date? or add the previous date to the end