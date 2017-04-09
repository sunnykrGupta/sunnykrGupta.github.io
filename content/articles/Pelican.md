Title: Pelican Python Blogging Framework
Date: 2014-05-26 17:23:31
Category: Blog
Tags: pelican,python
Author: Sunny Kr Gupta

Hello, Everyone! This is 2nd blog post about Pelican framework in python.

#### Deployment of Pelican : Blog Frameworks

Pelican is a static site generator, written in Python. It strikes as
a very interesting method as you can write your content purely in your favourite editor (in Markdown Flavour) and commit your post or style changes using Git. You can design your blog and deploy on [Github-Pages](https://pages.github.com/) very quickly.

#### Installation's :

How to setup Pelican?? [Go ahead](http://docs.getpelican.com/en/stable/quickstart.html) and detailed explanation of kicking a small webpage and deploying using github-pages, [Creating-a-blog-on-GitHub-dot-io-with-Python](http://seanazlin.com/creating-a-blog-on-GitHub-dot-io-with-Python.html) by Sean Azlin. I got most of the help in building this blog from this.

Variety of [themes](https://github.com/getpelican/pelican-themes) available.

#### Note's :
1. Follow Markdown syntax to write post.
2. Deploy your page by following and check your gitpage-url :

    $ ghp-import output

    $ git checkout master

    $ git merge gh-pages

    $ git push --all


![Responsive Blog](|filename|/images/Pelican.jpg "Pelican Image")
