# ssgwew Static Site Generator

simple markdown to html static site geneartor written in python.

## how to use

### dependenies 
* python3 (tested with python3.8-3.9)
* python pakage `markdown`, install with `pip3 install markdon`

### to run
`python3 ssgwew.py sitefolder` sitefolder is the folder with the file used to construct the site

to clean (delate) the site created use `python3 ssgwew.py clean` to all times you rebuild the site

## instruction 
the imput foder must have inside `makesite.txt` file and `pages` foder that contain the markdown version of the site pages, all `UPPERCASE FOLDER` is copied with theor content in destination folder

example

imput foder
```
mySite
    |--makesite.txt
    |--pages
        |--index.md
        |--subfoder
            |--page1.md
    |--STYLE
        |--style.css
    |--IMAGES
        |--cat.jpg
        |--rock.jpg
    |--html_inserts
        |--head.html
        |--footer.html
    |--other_foder
        !--text.txt
```
output folder (create a folder called `SITE`)
```
SITE
    |--pages
        |--index.html
        |--subfoder
            |--page1.html
    |--STYLE
        |--style.css
    |--IMAGES
        |--cat.jpg
        |--rock.jpg
```
### makesite.txt?
is a text file that tell the static site generator how to assemble html pages

1. first line contain the link where the site is host es `https://github.com/zwirgioIlredelCodice/`
2. next 3 lines
    1. indicate the file or group of file Unix style pathname pattern expansion [glob](https://docs.python.org/3/library/glob.html)
    2. indicate html file (es `head.html`), html text (es `<p>html text</p>`) and command (es [autotitle]) to put before the page html
    3. indicate html file (es `head.html`), html text (es `<p>html text</p>`) and command (es [autotitle]) to put after the page html

example 
makesite.txt
```
https://mydomain/
pages/blog/*.md <- all the file with extension .md in blog foder
head.html
tail.html
pages/index.md
head.html
tail.html
```
head.html
```html
<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
</head>
<body>
```
tail.html
```html
</body>
</html>
```
OUTPUT for es pages/index.md is file SITE/pages/index.html
```html
<!-- start content head.html -->
<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
</head>
<body>
<!-- finish content head.html -->

<!-- start content index.html -->
<h1>This is a Heading</h1>
<p>This is a paragraph.</p>
<!-- finish content index.html -->

<!-- start content tail.html -->
</body>
</html>
<!-- end content tail.html -->
```
for now is all. stay tuned for updates :)

> is hard to do documentation.