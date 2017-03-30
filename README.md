# Multi-repo-migration tool

This project is intended for migrating multiple Git repositories to Deveo. [Deveo](https://deveo.com/) is a code hosting solution that offers free private repository hosting for Git, Subversion and Mercurial repositories.

## Requirements:

Python, Gitpython and requests:

    pip install requests
    pip install gitpython

## Usage:

First step is to modify the migrate.py file. You need to specify COMPANY_KEY, ACCOUNT_KEY, COMPANY_NAME, USERNAME and PASSWORD from Deveo side. From your current code hosting solution side, you need to specify domain including HTTPS credentials, and project and repository names inside a python dictionary in the form of:

```
{ "PROJECT-NAME": ["repository1-name", "repository2-name"],
  "PROJECT2-NAME": ["repository3-name", "repository4-name"] }
```

After you have the modifications in place, you may execute the migration script as follows:

    python migrate.py

The script works as follows:

1. create a new project in Deveo
2. Loop through the projects and for each project
   1. Create a new project to Deveo and for each repository inside that project:
      1. clone your existing repository in to a temporary directory
      2. create corresponding repository to Deveo
      3. push the changes to Deveo repository
      4. Delete the tepomrary directory
