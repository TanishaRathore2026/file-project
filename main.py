from pathlib import Path
import os

def createfile():
    try:
        name = input("enter ur name = ")
        path = Path(name)
        if not path.exists():
            with open(path,"w")as fs:
                data = input("wht u want to write = ")
                fs.write(data)
            print("file created successfully")
        else:
            print("error file name is already exists")

    except Exception as err:
        print(f"an error occur in {err}")


def readfile():
    try:
        name = input("tell me ur file name:- ")
        path = Path(name)
        if path.exists():
            with open(path,"r") as fs:
                content = fs.read()
                print(f"ur file content is \n {content}")
        else:
            print("no file exits") 
    except Exception as err:
        print(f"an error occured as {err}")

def updatefile():
    try:
        name = input("tell u want to update the file:- ")
        path = Path(name)
        if path.exists():
            print("operations ")
            print("1. Rename the file")
            print("2. append the content")
            print("3. over writing the file")

            choice = int(input("enter ur option: "))
            if choice==1:
                newname = input("tell me nnew name= ")
                new_path = Path(newname)
                if not new_path.exists():
                    path.rename(new_path)
                    print("reanmmed successfully")
                else:
                    print("file name already exists")
            elif choice==2:
                with open(path,"a") as fs:
                    data = input("wht do u want to append")
                    fs.write(" \n"+data)
                print("append successfully")
            elif choice==3:
                with open(path,"w") as fs:
                    data = input("wht do u want to overwrite")
                    fs.write(" \n"+data)
                print("over write successfully")
    except Exception as err:
        print(f"an error occured as {err}")  



def deletefile():
    try:
        name = input("enter the file name u want to delete:- ")
        path = Path(name)
        if path.exists():
            path.unlink()
            print("file deleted successfully")
        else:
            print("Error no such file exists")
    except Exception as err:
        print(f"an erroe occured as {err}")


print("pree 1 for creating a file")
print("pree 2 for reading a file")
print("pree 3 for update a file")
print("pree 4 for deleting a file")


a = int(input("\ntell your response :- "))
if a==1:
    createfile()
if a==2:
    readfile()
if a==3:
    updatefile()
if a==4:
    deletefile()

