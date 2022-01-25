
#return the contents of the file ../../../flag.txt


import os


def main():

    # get the path to the flag file
    flag_path = os.path.join("", './flag')

    # open the flag file and read the contents
    with open(flag_path, 'r') as f:
        content = f.read()

        print(content)

    # return the contents of the flag file
    return content

main()