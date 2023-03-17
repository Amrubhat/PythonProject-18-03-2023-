with open("attendance.txt", 'r') as r, open('file.txt', 'w') as o:
    for line in r:
        #strip() function
        if line.strip():
            o.write(line)
f = open("file.txt", "r")
print("New text file:\n",f.read())