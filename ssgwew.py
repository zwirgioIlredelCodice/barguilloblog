import markdown
import os
import sys
import glob
from distutils.dir_util import copy_tree, remove_tree


def createsite_folder(project_dir):
    # create folder for site output
    new_dir = os.path.join(os.getcwd(), "SITE")
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    site_dir = new_dir  # enter in SITE folder

    dir_list = os.listdir()

    folder_upper_list = []
    for i in dir_list:  # make a list of folder in uppercase
        if os.path.isdir(i) and i.isupper() and i != "SITE":
            folder_upper_list.append(i)

    for i in folder_upper_list:
        # copy all folder in UPPERCASE and is content in site_dir
        copy_tree(os.path.join(project_dir, i), os.path.join(site_dir, i))

    # create PAGES folder with subfolder
    if os.path.isdir(os.path.join(project_dir, "pages")):
        copy_tree(os.path.join(project_dir, "pages"),
                  os.path.join(site_dir, "pages"))

    else:
        print(" \"site\" folder is missing\nEXIT")
        quit()

    # list of .md file in site copied folder to delate
    file_to_remove = glob.glob('SITE/pages/**/*.md', recursive=True)
    for i in file_to_remove:
        os.remove(i)


def read_makesite(project_dir):
    with open(os.path.join(project_dir,'makesite.txt'), 'r') as makesite:
        # make a list ["file","arg1","file","arg1",..]
        makesite_data = makesite.readlines()

    makesite_list = []
    for i in makesite_data:
        # make a list [["file","arg1",..],["file","arg1",..]]
        makesite_list.append(i.split())
    
    return makesite_list


def md_to_HTML(makesite_list,project_dir,out_dir):
    for commands in makesite_list:
        # finde the file writtn in makefile.txt
        file_list = glob.glob(os.path.join(project_dir,commands[0]), recursive=True)

        for i in file_list:
            with open(i, "r", encoding="utf-8") as input_file:
                text = input_file.read()
                html = markdown.markdown(text)

            # change extenzion to html and put in SITE folder
            namefile_md = os.path.split(i)[1]
            namefile_html = os.path.splitext(namefile_md)[0]+".html"
            html_dir = os.path.join(out_dir, namefile_html)
            #newdir = os.path.splitext(newdir)[0]+".html"
            print(html_dir)
            with open(html_dir, "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
                output_file.write(html)

def clean(out_dir):
    remove_tree(out_dir)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        project_dir = os.path.join(os.getcwd(),sys.argv[1])
        out_dir = os.path.join(os.getcwd(),"SITE")

        if sys.argv[1] == "clean":
            clean(out_dir)
        else:
            createsite_folder(project_dir)  # to test it
            #makesite_list = read_makesite(project_dir)
            #md_to_HTML(makesite_list,project_dir,out_dir)  # for testing
    else:
        print("no args or to many ERROR :(")