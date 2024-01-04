# Developer workflow

## Commits

The commit message used in this project should have a following form:
```
<type>: <subject>
```

Type can be:
- build: changes related to building the code (e.x. adding dependencies)
- chore: changes that do not affect the external user (e.x. setting of linters)
- feat: a new feature
- fix: a bug fix
- docs: documentation related changes
- refactor: a code that neither add new feature nor fix bug (e.x. renaming variables)
- perf: a code that improves perfomance style (related to styling)
- test: adding new tests or changing existing tests
- git: anything related to git (e.x. gitignore, continuous integration and continuous delivery)

<!---
Taken from https://medium.com/@naandalist/creating-a-git-commit-message-convention-for-your-team-acb4b3edfc44
--->

## Branches

Names of the branches should correspond to what they will add to the code.
They should have the following form:
```
<type>/<subject>
```

Possible types:
- fix
- feature
- docs

## Testing

To test, lint and compile the code user have to have installed hatch
```bash
pip install hatch
```

To run the tests, run the following command in root directory of the project:
```bash
hatch run test
```
or
```bash
hatch run cov
```

To run linters, run the following:
```bash
hatch run lint:all
```

If linter finds errors, you can try to run the following command to repair them:
```bash
hatch run lint:fmt
```


