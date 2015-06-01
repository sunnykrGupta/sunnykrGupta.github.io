Title: Pelican Python Blogging Framework
Date: 2014-05-26 17:23:31
Category: Blog
Tags: pelican,python
Author: Sunny Kr Gupta

Hello, Everyone! This is 2nd blog post about Pelican framework in python.

### Deployment of Pelican : Blog Frameworks

Pelican is a static site generator, written in Python. It strikes as
a very interesting method as you can write your content purely in your favourite editor (in Markdown Flavour) and commit your post or style changes using Git. You can design your blog and deploy on [Github-Pages](https://pages.github.com/) very quickly.

#### Installation's :

How to setup Pelican?? [Go ahead](http://ntanjerome.org/blog/how-to-setup-github-user-page-with-pelican).

Variety of themes available [Click](https://github.com/getpelican/pelican-themes).

#### Note's :
1. Always activate your virtual server **source v_env_name/bin/activate** before creating post.
2. Follow Markdown syntax to write post.
3. Deploy your page by following and check your gitpage-url : 

    $ ghp-import output

    $ git checkout master

    $ git merge gh-pages

    $ git push --all


![Responsive Blog](|filename|/images/Pelican.jpg "Pelican Image")
