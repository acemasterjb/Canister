# Canister

## TOC
* [About](#About)
* [Dependencies](#Dependencies)
* [Installation Instructions](#Installation)

## About
This is a fork of an (unregistered) blog app I have privately on my git. It's a Blog web app template with CRUD Admin controls with a modular design.

- **SQLAlchemy** is used to interface with the database
- **Flask Admin** is used for the CRUD, Admin control interface. Making it easy to manage Canister's "variables" such as it's users, the posts, the pages added to the base web app and comments to posts (and maybe pages later)
- **Summernote** is used to handle the post and page editing. It's a very comprehensive but easily pluggable WYSIWYG editor that supports inputting images and videos and format text
- **Flask Misaka** is used to render pages and posts created using the **Summernote** WYSIWYG editor

## Dependencies
* **Microsoft Visual C++ 14.0+** [instructions](https://stackoverflow.com/a/52467429/5049228)
* every module outlined in [requires.txt](/requires.txt)

## Installation
1. Install the Visual C++ requirement in the [Dependencies section](#Dependencies)
2. Clone this repository, then open a terminal directing to it's path
3. Install python dependencies `~\> pip install -r requires.txt`
4. Change your server secret key found in the [\_\_init\_\_.py file here](https://github.com/acemasterjb/Canister/blob/3cab009cac2b470ddde613cd7a4a4ec7e37ac2bc/blog/__init__.py#L33)
5. Set up flask environment. Follow [this guide](https://flask.palletsprojects.com/en/1.1.x/quickstart/) past the minimal application example, but don't run yet.
6. Run `~\> flask init-db` then `~\> flask run` and your server should be up and running!
