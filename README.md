# CIthon
Continuous Integration marathon to use the latest Python versions

One can easily help the Python community by running tests on in-development branches of CPython so that issues gets detected earlier rather than later. This is very well described in @brettcannon's article : https://snarky.ca/how-to-use-your-project-travis-to-help-test-python-itself/ .

This lead me to think that the best way to make people run their Continuous Integration on these CPython branches is to submit a pull-request to add them in the Continuous Integration config. This looks like a boring-yet-highly-automatisable task. Then:
 - the result would be provided directly : either there is a problem with the considered version of Python or everything is fine
 - in the former case, issue can easily be investigated by the repo's responsible so that they fix it and/or open a bug on the CPython bug tracker
 - in the latter, everything is fine and the repo's owner needs only one click to improve his CI config.
 
Thus my plan is to write a script to take care of this task. Along the way, I plan to learn a lot about the Github API, YAML files, Travis, git and a lot more :-)
 
To find relevant repository, one should probably focus on repos that:
  - are not forked
  - have a Travis config file
  - ... with at least one Python 3 version
  - ... but not the latest nor "nightly"
  - have accepted at least one pull-request in the past
  - have no pending pull-request about the latest Python version
