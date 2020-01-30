"""Linting and return score as system code"""

from os import system
from pylint.lint import Run

results = Run(["leaf"], do_exit=False)
score = round(results.linter.stats["global_note"], 2)
system('echo "::set-output name=score::' + str(score) + '"')
