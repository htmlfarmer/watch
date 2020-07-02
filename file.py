import os.path

# READ(filename, directory)


def READ(filename, *argv):
    directory = argv
    if directory is None or directory is ():
        directory = "./"
    else:
        directory = directory[0]
    file_path = os.path.join(directory, filename)
    text = None
    if os.path.exists(file_path): # read the old file
        file = open(file_path, "r") # for python 2.7 you need the full word "read"?
        text = file.read()
        file.close()
    return text


def WRITE(filename, directory, text):
    file_path = os.path.join(directory, filename)
    if not os.path.isdir(directory):
        os.mkdir(directory) # make a new directory
    file = open(file_path, "w")
    file.write(text)
    file.close()
    return
