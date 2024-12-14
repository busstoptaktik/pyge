default:
    just --list

check:
    ruff check
    ruff format --check
    pytest

fix:
    ruff check --fix
    ruff format
    pytest

commit:
    ruff check
    ruff format --check
    pytest
    git commit

status:
    git status

diff:
    git diff

# Do git add ... then just amend
amend:
    ruff check
    ruff format --check
    pytest
    git commit --amend
