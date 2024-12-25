import argparse
import os



def openFolder(folder, indentation):
    '''Listing all the files inside the current directory and returning a tree structure.'''
    file_tree = ''  # Initialize an empty string to accumulate the tree
    try:
        subFolders = os.listdir(folder)  # List the contents of the folder
    except PermissionError:
        file_tree += indentation + '- [Permission Denied]\n'
        return file_tree
    except FileNotFoundError:
        file_tree += indentation + '- [Folder Not Found]\n'
        return file_tree
    except OSError as e:
        file_tree += indentation + f'- [Error: {e}]\n'
        return file_tree

    folder_name = os.path.basename(folder)  # Get just the folder name, not the full path
    file_tree += indentation + '|' + folder_name + '\n'  # Add the current folder to the file_tree
    indentation += '|---'  # Increase the indentation for the next level

    # Recursively list files and folders
    for subFolder in subFolders:
        subFolderPath = os.path.join(folder, subFolder)  # Get the full path to the subfolder
        if os.path.isdir(subFolderPath):  # If it's a directory, recurse into it
            file_tree += openFolder(subFolderPath, indentation)
        else:  # If it's a file, just list it
            file_tree += indentation + '-' + subFolder + '\n'
    return file_tree

def main():
    parser = argparse.ArgumentParser(description="This script lists files and directories in a given folder, " 
                    "and optionally writes the tree structure to a file.")
    parser.add_argument("-f","--file", type=str, help="Name of file to write to !")
    parser.add_argument("-s","--silent", help="To silent i.e., not print on console", action='store_true')
    parser.add_argument("-d","--dir", type=str, help="Root Folder")
    args = parser.parse_args()

    folder = args.dir if args.dir else os.getcwd()
    file_tree = openFolder(folder, '')

    # Printing whole file tree in command-line
    if not args.silent:
    	print(file_tree)

    # Write the output to a file
    if args.file:
        print(f"Writing files of {folder} in {args.file}")
        with open(args.file, 'w', encoding='utf-8') as file:  # Open the file in write mode ('w')
    	    file.write(file_tree)  # Write the tree structure to the file

if __name__ == '__main__':
    main()