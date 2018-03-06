#!/usr/bin/env python3
# vim: set expandtab shiftwidth=4 tabstop=4 :
"""CIthon3"""

# http://pygithub.readthedocs.io/en/latest/github.html?highlight=search#github.MainClass.Github.search_repositories
# http://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository
# import github
import github3
import getpass
import itertools
import os

fmt = '- "%s"'
NEW_PY3_VERSIONS = [fmt % v for v in ('3.6', '3.7', 'nightly')]
PY3_VERSIONS = [fmt % v for v in '3.2 3.3 3.4 3.5'.split()] + NEW_PY3_VERSIONS


def repo_is_candidate(repo):
    def log(s):
        # pass
        print(repo.name + " " + s)
        # print('.', end='', flush=True)
        return False

    if not repo.language != 'python':
        return log('is not Python')

    if repo.fork:
        return log("is a fork")
    # if r.language != 'Python':
    #     log("is not a Python project (%s)" % r.language)
    #     return False
    if not list(repo.iter_pulls(state='closed')):
        return log("has no closed pull requests")
    travis_file = repo.contents('.travis.yml')
    if not travis_file:
        return log("has no travis file")
    travis_file = travis_file.decoded.decode('utf-8').lower()
    if 'language: python' not in travis_file:
        fmt = "has no reference to Python in travis file (%s)"
        return log(fmt % repo.language)
    if not any(version in travis_file for version in PY3_VERSIONS):
        return log("does not test Python 3")
    if any(version in travis_file for version in NEW_PY3_VERSIONS):
        return log("already tests recent Python versions")
    return True


if __name__ == "__main__":
    client_id = os.getenv('CLIENT_ID', getpass.getuser())
    client_secret = os.getenv('CLIENT_SECRET')
    login = os.getenv('GITHUB_LOGIN', getpass.getuser())
    password = os.getenv('GITHUB_PASSWORD', getpass.getpass(password = getpass('Password for %s: ' % login)))
    print("Using '%s'/'%s' // '%s'/'%s'" % (client_id, client_secret, login,
                                            password))
    gh = github3.login(login, password=password)
    gh_user = gh.user()
    repos = (repo for repo in gh.iter_repos(sort='stars')
             if repo_is_candidate(repo))
    for repo in itertools.islice(repos, 50):
        print('')
        print(repo, repo.html_url, repo.language)
        print('Calling git clone:', repo.clone_url)
        """
        f = gh_user.create_fork(r)
        if f in original_repos:
            print("%s already forked" % f)
        else:
            # call(["git", "clone", f.clone_url])
        """
