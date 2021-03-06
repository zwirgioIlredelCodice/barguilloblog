import commonmark
import os
import sys
import glob 
import re
from distutils.dir_util import copy_tree, remove_tree


def createsite_folder(project_dir, out_pages_dir):

    folder_upper_list = listdir_upper(project_dir)

    for i in folder_upper_list:
        # copy all folder in UPPERCASE and is content in site_dir
        copy_tree(os.path.join(project_dir, i), os.path.join(out_pages_dir, i))

    # create pages folder with subfolder
    if os.path.isdir(os.path.join(project_dir, "pages")):
        copy_tree(os.path.join(project_dir, "pages"),
                  os.path.join(out_pages_dir, "pages"))

    else:
        print(" \"site\" folder is missing\nEXIT")
        quit()

    # list of .md file in site copied folder to rename with .html
    file_to_rename = glob.glob('SITE/pages/**/*.md', recursive=True)
    file_renamed = []
    for i in file_to_rename:
        file_renamed.append(os.path.splitext(i)[0]+".html")

    for i in range(len(file_renamed)):
        os.rename(file_to_rename[i], file_renamed[i])

    return file_renamed


def read_makesite(project_dir):
    with open(os.path.join(project_dir, 'makesite.txt'), 'r') as makesite:
        # make a list ["file","arg1","file","arg1",..]
        makesite_data = makesite.readlines()

    makesite_list = []
    for i in makesite_data:
        # make a list [["file","arg1",..],["file","arg1",..]]
        makesite_list.append(i.split())

    return makesite_list


def fix_extern_HTML(html_text, link_prefix):
    html = html_text

    tag_openhref = 'href="'
    tag_closehref = '">'

    tag_opensrc = 'src="'
    tag_closesrc = '"'
    
    # for href
    open_href = [m.start() for m in re.finditer(tag_openhref, html_text)]
    close_href = []

    for i in open_href:
        close_href.append(html_text.find(tag_closehref,i))

    # for src
    open_src = [m.start() for m in re.finditer(tag_opensrc, html_text)]
    close_src = []
    
    for i in open_src:
        close_src.append(html_text.find(tag_closesrc,i+len(tag_opensrc)+1))

    # for href
    for i in range(len(close_href)):
        link_address = html_text[open_href[i]:close_href[i]]

        base_link = link_address + tag_closehref

        link_address = link_address.replace(tag_openhref, "")

        if not (link_address.startswith("https://") or link_address.startswith("http://")): #if is a local link
            link_address = link_prefix + link_address

        link_replace = tag_openhref + link_address + tag_closehref

        html = html.replace(base_link, link_replace)
    
    # for src
    for y in range(len(open_src)):
        link_address = html_text[open_src[y]:close_src[y]]

        base_link = link_address + tag_closesrc

        link_address = link_address.replace(tag_opensrc, "")

        if not (link_address.startswith("https://") or link_address.startswith("http://")): #if is a local link
            link_address = link_prefix + link_address

        link_replace = tag_opensrc + link_address + tag_closesrc

        html = html.replace(base_link, link_replace)

    return html


def interprete_command(list_command):

    html_output = ""

    for command in list_command:

        if command.endswith(".html"): #if is an html file es head.html
            with open(os.path.join(project_dir, command), "r") as file_head:
                # Reading form a file
                html_output = html_output + file_head.read()
        
        elif command.startswith('"') and command.endswith('"'): #if is a html text es "<p> hello </p>"
            html_output = html_output + command[1:-1] #remove " " from text string

        elif command.startswith('[') and command.endswith(']'): #if is a command es [autotitle]
            #list of command

            if command == "[ssgwew]":
                html_output = html_output + "<p>made with ssgwew</p>"
            
            else:
                print("command ", command, "not recognise WARNING :|")
        
        else:
            print(command, "is not an html file, html string or command WARNING :|")
    return html_output


def md_to_HTML(makesite_list, project_dir, file_output_dir):

    link = makesite_list[0][0]

    for line_command in range(1, len(makesite_list), 3):
        file_in = os.path.join(project_dir, makesite_list[line_command][0])

        command_head_list = makesite_list[line_command+1]
        head_html = interprete_command(command_head_list)

        command_tail_list = makesite_list[line_command+2]
        tail_html = interprete_command(command_tail_list)

        file_in_list = glob.glob(file_in, recursive=True)

        if len(file_in_list) > 0:

            for i in range(len(file_in_list)):

                file_content_out = ""

                with open(file_in_list[i], "r", encoding="utf-8") as input_file:
                    text = input_file.read()
                    file_content_out = head_html + commonmark.commonmark(text) + tail_html
                    file_content_out = fix_extern_HTML(file_content_out, link)
                
                with open(file_output_dir[i], "w", encoding="utf-8") as output_file:
                    output_file.write(file_content_out)

        else:
            print("no file found with rule ", file_in)


def listdir_upper(directory):
    dir_list = os.listdir(project_dir)

    folder_upper_list = []
    for i in dir_list:  # make a list of folder in uppercase
        if os.path.isdir(os.path.join(project_dir, i)) and i.isupper():
            folder_upper_list.append(i)
    return folder_upper_list


def clean(out_pages_dir):
    remove_tree(out_pages_dir)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        project_dir = os.path.join(os.getcwd(), sys.argv[1])
        out_pages_dir = os.path.join(os.getcwd(), "SITE")

        if sys.argv[1] == "clean":
            clean(out_pages_dir)
        else:
            if not os.path.exists(out_pages_dir):  # create SITE folder
                os.makedirs(out_pages_dir)

            file_output_dir = createsite_folder(
                project_dir, out_pages_dir)  # to test it

            makesite_list = read_makesite(project_dir)
            md_to_HTML(makesite_list, project_dir, file_output_dir)  # for testing
    else:
        print("no args or to many ERROR :(")
