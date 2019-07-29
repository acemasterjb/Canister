# Canister

## About
This is an (unregistered) fork of a blog app I have privately on my git. It's a Blog web app template with CRUD Admin controls with a modular design.

- **SQLAlchemy** is used to interface with the database
- **Flask Admin** is used for the CRUD, Admin control interface. Making it easy to manage Canister's "variables" such as it's users, the posts, the pages added to the base web app and comments to posts (and maybe pages later)
- **Summernote** is used to handle the post and page editing. It's a very comprehensive but easily pluggable WYSIWYG editor that supports inputting images and videos and format text
- **Flask Misaka** is used to render pages and posts created using the **Summernote** WYSIWYG editor
