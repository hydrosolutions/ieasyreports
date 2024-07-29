# Development
This is a short guide for the maintainers of the library.

## Local development setup
- clone the GitHub repository as per instructions in the [installation guide](installation.md)
- create a new virtual environment to install the dependencies
- after activating the environment and cloning the repository, run `pip install .` which will install the dependencies

### Installing as an editable package inside another project
If you wish to install the library into an existing project, you can also follow the instruction in
the [installation guide](installation.md). However, if you wish to have the best developing experience, it's
recommended to install the library as an editable package. To do so, run the standard `pip install` command
alongside the `-e` flag and the path to where you've cloned the library, for example:
`pip install -e /home/developer/projects/ieasyreports`

Doing like so will enable you to make changes to the code of the library and your project instantly having the
latest changes.

## Documentation
All the documentation lives in the `docs` folder as `.md` files.
To be able to view the documentation as a nicely formatted document, you need to build it. To do so, position
yourself in the `docs` folder and run the following command:
`make html`

This will build the documentation in the `_build` sub-folder inside the `docs` folder. Navigate to the `_build`
sub-folder and open `index.html` inside the `html` sub-folder in your favourite browser and enjoy reading the docs.

