import markdown
import os
import sys
import glob
from distutils.dir_util import copy_tree, remove_tree


def createsite_folder(project_dir, out_pages_dir):

    folder_upper_list = listdir_upper(project_dir)

    for i in folder_upper_list:
        # copy all folder in UPPERCASE and is content in site_dir
        copy_tree(os.path.join(project_dir, i), os.path.join(out_pages_dir, i))

    # create pages folder with subfolder
    if os.path.isdir(os.path.join(project_dir, "pages")):
        copy_tree(os.path.join(project_dir, "pages"),os.path.join(out_pages_dir, "pages"))

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
    
    print(makesite_list)
    return makesite_list


def md_to_HTML(makesite_list,project_dir,out_pages_dir,name_project):

    for commands in makesite_list:
        # finde the file writtn in makefile.txt

        file_content_out = ""
        file_out_list = []

        file_list = glob.glob(commands[0], recursive=True)

        if len(file_list) > 0: #if 

            for i in file_list:
                # change extension to html and put in SITE folder
                namefile_md = i.replace(os.path.commonpath([i,out_pages_dir]),"").replace('/'+name_project+'/'+"pages"+'/',"") #è orribile da fare megio 
                namefile_html = os.path.splitext(namefile_md)[0]+".html"
                html_dir = os.path.join(out_pages_dir, namefile_html)
                
                file_out_list.append(html_dir) #make a list of file.html
            
            for argument in commands[1::]:

                argument_path = os.path.join(project_dir,argument)

                if argument_path.endswith(".html"): #if is an html file append at the output file

                    if os.path.isfile(argument_path):
                        with open(argument_path, "r", encoding="utf-8") as input_file:
                            file_content_out = file_content_out + input_file.read()
                    else:
                        print(argument," file not found WARNING")

                if argument_path = "page":

                    for i in file_list:
                        with open(i, "r", encoding="utf-8") as input_file:
                            text = input_file.read()
                            file_content_out = file_content_out + markdown.markdown(text)
                
                else:
                    print(argument_path," file not found WARNING")            


        else:
            print(commands[0]," file not found WARNING")        

        for argument in commands[1::]:

            argument_path = os.path.join(project_dir,argument)

            if argument_path.endswith(".html"): #if is an html file append at the output file

                if os.path.isfile(argument_path):
                    with open(argument_path, "r", encoding="utf-8") as input_file:
                        file_content_out = file_content_out + input_file.read()
                else:
                    print(argument," file not found WARNING")

            if argument_path.endswith(".md"): #if is an markdown file

                file_list = glob.glob(argument_path, recursive=True)

                if len(file_list) > 0: #if 

                    for i in file_list:
                        with open(i, "r", encoding="utf-8") as input_file:
                            text = input_file.read()
                            file_content_out = file_content_out + markdown.markdown(text)
                
                else:
                    print(argument_path," file not found WARNING")

                

            # change extension to html and put in SITE folder
            namefile_md = i.replace(os.path.commonpath([i,out_pages_dir]),"").replace('/'+name_project+'/'+"pages"+'/',"") #è orribile da fare megio 
            
            namefile_html = os.path.splitext(namefile_md)[0]+".html"
            html_dir = os.path.join(out_pages_dir, namefile_html)
            with open(html_dir, "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
                output_file.write(file_content_out)

def listdir_upper(directory):
    dir_list = os.listdir(project_dir)

    folder_upper_list = []
    for i in dir_list:  # make a list of folder in uppercase
        if os.path.isdir(os.path.join(project_dir,i)) and i.isupper():
            folder_upper_list.append(i)
    return folder_upper_list


def clean(out_pages_dir):
    remove_tree(out_pages_dir)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        project_dir = os.path.join(os.getcwd(),sys.argv[1])
        out_pages_dir = os.path.join(os.getcwd(),"SITE")

        if sys.argv[1] == "clean":
            clean(out_pages_dir)
        else:
            if not os.path.exists(out_pages_dir): #create SITE folder
                os.makedirs(out_pages_dir)
            
            createsite_folder(project_dir, out_pages_dir)  # to test it

            out_pages_dir = os.path.join(out_pages_dir,"pages")

            makesite_list = read_makesite(project_dir)
            md_to_HTML(makesite_list,project_dir,out_pages_dir,sys.argv[1])  # for testing
    else:
        print("no args or to many ERROR :(")