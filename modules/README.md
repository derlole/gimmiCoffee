# THE MODULES

## the modules in this folder are used to make a more viewable server code possible.
## code that is either needed in different filed over the server folder structure is placed in an module and imported by some other files or just code sections which are doing replicated things like reading or writing data to something.

## db.py
### in the DB module are some SQLite commands in functions. Each of them returns datasets according to it names so e.g. in Blueprint routing u only have to call a function to get your dataset which leads to more structured code.

## persistence
### the persistence module contains just some functions to manage the in the persistence given JSON objects

## socketio
### socketio is the main socket/flask server instance and some functions to manage communication