# vim: set expandtab shiftwidth=4 tabstop=4 :
"""CIthon"""

# http://pygithub.readthedocs.io/en/latest/github.html?highlight=search#github.MainClass.Github.search_repositories
# http://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository
import github
import os
import itertools
from subprocess import call

NEW_PY3_VERSIONS = [b'3.6', b'3.7', b'nightly']
PY3_VERSIONS = [b'3.2', b'3.3', b'3.4', b'3.5'] + NEW_PY3_VERSIONS


def repo_is_candidate(r):
    def log(s):
        # pass
        # print(str(r) + " " + s)
        print('.', end='', flush=True)
    if r.fork:
        log("is a fork")
        return False
    # if r.language != 'Python':
    #     log("is not a Python project (%s)" % r.language)
    #     return False
    if not r.get_pulls('closed'):
        log("has no closed pr")
        return False
    try:
        travis_file = r.get_contents('.travis.yml')
    except github.UnknownObjectException:
        log("has no travis file")
        return False
    decoded_travis = travis_file.decoded_content.lower()
    if b'language: python' not in decoded_travis:
        log("has no reference to python in travis file (%s)" % r.language)
        return False
    if not any(b'- "' + v + b'"' in decoded_travis for v in PY3_VERSIONS):
        log("does not use Python 3")
        return False
    if any(b'- "' + v + b'"' in decoded_travis for v in NEW_PY3_VERSIONS):
        log("already uses recent Python versions")
        return False
    return True


def get_candidates_repos(github):
    # for r in github.get_repos():
    for r in github.search_repositories('python', sort='stars', order='desc'):
        if repo_is_candidate(r):
            yield r

if __name__ == "__main__":
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    login = os.getenv('GITHUB_LOGIN')
    password = os.getenv('GITHUB_PASSWORD')
    print("Using '%s'/'%s' // '%s'/'%s'" %
          (client_id, client_secret, login, password))
    g = github.Github(
            client_id=client_id,
            client_secret=client_secret,
            login_or_token=login,
            password=password)
    u = g.get_user()
    original_repos = list(u.get_repos())
    for r in itertools.islice(get_candidates_repos(g), 50):
        print('')
        print(r, r.html_url, r.language)
        f = u.create_fork(r)
        if f in original_repos:
            print("%s already forked" % f)
        else:
            call(["git", "clone", f.clone_url])
