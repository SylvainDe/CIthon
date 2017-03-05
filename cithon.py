# vim: set expandtab shiftwidth=4 tabstop=4 :
"""CIthon"""

# http://pygithub.readthedocs.io/en/latest/github.html?highlight=search#github.MainClass.Github.search_repositories
# http://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository
import github
import os

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
g = github.Github(client_id=client_id, client_secret=client_secret)

NEW_PY3_VERSIONS = [b'3.6', b'3.7', b'nightly']
PY3_VERSIONS = [b'3.2', b'3.3', b'3.4', b'3.5'] + NEW_PY3_VERSIONS


def repo_is_candidate(r):
    def log(s):
        print(str(r) + " " + s)
    if r.fork:
        log("is a fork")
        return False
    # if r.language != 'Python':
    #     log("is not a Python project (%s)" % r.language)
    #     return False
    prs = r.get_pulls('closed')
    try:
        pr = prs[0]
    except IndexError:
        log("has no closed pr")
        return False
    try:
        travis_file = r.get_contents('.travis.yml')
    except github.UnknownObjectException:
        log("has no travis file")
        return False
    decoded_travis = travis_file.decoded_content
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


def get_candidates_repos():
    # for r in g.get_repos():
    for r in g.search_repositories('python'):
        if repo_is_candidate(r):
            yield r

if __name__ == "__main__":
    for r in get_candidates_repos():
        print(r, r.html_url, r.language)
        input()
