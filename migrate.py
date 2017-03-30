import requests
import json
from git import Repo
import tempfile
import os.path as osp
import shutil

# DEVEO INFORMATION
DEVEO_URL = 'https://app.deveo.com/'
COMPANY_KEY = '<DEVEO COMPANY KEY>'
ACCOUNT_KEY = '<DEVEO ACCOUNT KEY>'
COMPANY_NAME = "<DEVEO COMPANY NAME>"
USERNAME = "DEVEO USERNAME FOR CLONING"
PASSWORD = "DEVEO PASSWORD"

# PROVIDER INFORMATION assuming https://domain.com/project/repo structure.
DOMAIN = "https://<USERNAME>:<PASSWORD>@domain.com/"
PROJECT_AND_REPO_NAMES = { "PROJECT1NAME": ["repository-name.git", "repository2-name"],
                           "PROJECT2NAME": ["repo-name.git", "repo-name"] }

def get_header(company_key, account_key):
    return {'Accept': 'application/vnd.deveo.v1',
            'Authorization': "deveo company_key='%s',account_key='%s'" % (company_key, account_key),
            'Content-type': 'application/json'}

def create_project_request(id, name):
    return { "id": id, "name": name }

def create_repository_request(id):
    return { "id": id, "type": "git" }

def create_project(id, name):
    payload = create_project_request(id, name)
    header = get_header(COMPANY_KEY, ACCOUNT_KEY)
    url = osp.join(DEVEO_URL, "api/projects")
    requests.post(url, headers=header, data=json.dumps(payload))

def create_deveo_repository(project, repo_id):
    payload = create_repository_request(repo_id)
    header = get_header(COMPANY_KEY, ACCOUNT_KEY)
    url = osp.join(DEVEO_URL, "api/projects", project, "repositories")
    requests.post(url, headers=header, data=json.dumps(payload))


for project, repos in PROJECT_AND_REPO_NAMES.iteritems():
    create_project(project, project.capitalize())
    for repo in repos:
        stripped_repo = repo.strip(".git")
        temp_dir = tempfile.mkdtemp()
        cloned_repo = Repo.clone_from(osp.join(DOMAIN, project, repo), temp_dir)
        create_deveo_repository(project, stripped_repo)
        with cloned_repo.remotes.origin.config_writer as cw:
            cw.set("pushurl", osp.join(DEVEO_URL.replace("https://","https://%s:%s@" % (USERNAME, PASSWORD)), COMPANY_NAME, "projects", project, "repositories", "git", stripped_repo))
        cloned_repo.remotes.origin.push(mirror=True)
        shutil.rmtree(temp_dir)
