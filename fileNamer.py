import sys
import os


def main():
    fileIndex=1
    name="random"
    index=0
    names=[["stick",0,9],["character",0,9],["dot",0,9],["wind",0,4],["dragon",0,3],["flower",0,4],["season",0,4]]
    directory=sys.argv[1]
    if not os.path.isdir(directory):
        raise FileNotFoundError("Directory not found: "+ directory)
    sfiles = os.listdir(directory)
    files=sorted(
    sfiles,
    key=lambda f: int(''.join(filter(str.isdigit, f))) if any(c.isdigit() for c in f) else float('inf')
)
    print(files)
    for file in files:
        if names[index][1]==names[index][2]:
            index+=1
            fileIndex=1
        if(index>=len(names)):
         exit(0)
        name=names[index][0]
        extension= "."+file.split(".")[-1]
        ren=name+"_"+str(fileIndex)+extension
        fullName=os.path.join(directory,file)
        newName=os.path.join(directory,ren)
        try:
            os.rename(fullName,newName)
        except Exception as e:
            print("File couldn't be renamed: "+ e)

        names[index][1]+=1
        fileIndex+=1
       
        
if __name__=="__main__":
    main()