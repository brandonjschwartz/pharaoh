pharaoh
=======

Command line tools for rapid Pyramid development.

The problem
-----------

Pyramid is a very pay-for-what-you-eat framework. It doesn't impose any set design or layout on the developer and this is a Good Thing.

However, some developers have expressed an interest in a larger Pyramid menu. Most packages, with the exception of scaffolds, install in the upper level Python library - away from the developer, the application, the git repository, and any way to customize or build on to what exists.

I'm pretty new to Pyramid and Python. What I do, I teach myself and there have been a few frustrations.

First, every add on (not just specific to Pyramid) is kept away from me and is always independent of my application. The only exception to this is NodeJs where the modules are loaded into a node_modules directory within a local working directory. But even there, tying it to my application can be a weird challenge. I know all this helps with abstraction, but still.

Second, if I try to build apps that do more than one thing, layout and configuration bogs me down. It's probably due to my newness, but part of me likes how Django has a startapp command and a developer can just keep everything modularized. But Django's not my style for several reasons.

Third, there's not much of a Pyramid community. As mentioned in this thread, Python provides really straight forward ways of building out a website. But things aren't very modularized and we haven't seen any drop dead simple blog engines like a Python Wordpress. 

Pyramid is just Python, but it's also Pyramid too. It has a unique API.

I like how Wordpress and Drupal have a plugin/module system where you drop some files in place, connect them to the central application, fill in some basic configuration settings, and you're good to go. I also like how Meteor has developed their package manager to be centered around tight, modularized programs that can be dropped in and immediately exposed to the Meteor developer. It works because it was designed for Meteor, even though Meteor is just JavaScript.

I want something plug and play where I can run the command ```pharaoh add accounts``` and a module consisting of Python code, stylesheets, and templates drop into a directory and I add two lines in my applications __init__.py file; ```import accounts```, ```config.include(accounts)``` 

I also want something that accurately reflects Pyramid as a web application. Pyramid runs more than just Python; one can easily write C code, Java (through Jython), a pure client-side JavaScript app, or something else that sits on top of and is rendered by Pyramid.

The Solution
------------

Pharaoh, a command line tool just for Pyramid. I don't really care if people want to help or want to make re-usable apps for Pyramid. If you want to though, great, let's talk.

For the curious, installation of Pharaoh should be done by typing 

    pip install git+https://github.com/brandonjschwartz/pharaoh.git

Pharaoh supports the following commands.

    pharaoh -l

List of available starter apps, similar to Pyramid's scaffolds.

    pharaoh -s [starter-name] [directory]

Install a starter app in a directory. Right now the only starter app is alchemy. This uses SQLAlchemy, Chameleon, and URL Dispatch. Personally, I prefer Mako templates. To use Mako, you have to provide the full path to the templates folder when you render your views (see this feature request), whereas Chameleon will work with the example shown.

The Alchemy starter app comes with a directory for static and template files, and files for models, views, tests, routes, and factories.

Once you want to include your app in your main application, add the following lines to your __init__.py file:

```
import [app]
config.include([app])
```
