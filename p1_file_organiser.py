import os
import shutil


class File_Organiser:
    def __init__(self, dir):
        self.dir = dir


    def organise_file(self):
        if not os.path.exists(self.dir):
            print(f"The directory -> '{self.dir}' ,does not exist.")
            return
        
        files = [f for f in os.listdir(self.dir) if os.path.isfile(os.path.join(self.dir, f))]
        
        for file in files:
            file_extension = file.split('.')[-1]
            
            folder_path = os.path.join(self.dir, file_extension)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            shutil.move(os.path.join(self.dir, file), os.path.join(folder_path, file))
        
        print("Files are being organised....\nDONE")


def main():
    dir = input("\nThis program will organize the folder according to their extensions.\nEnter the path of the dir: ")
    organizer = File_Organiser(dir)
    organizer.organise_file()


if __name__ == "__main__":
    main()
