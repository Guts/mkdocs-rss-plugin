#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
from pathlib import Path
from typing import Union

# 3rd party
from setuptools import find_packages, setup

# package (to get version)
from mkdocs_rss_plugin import __about__

# ############################################################################
# ########## Globals #############
# ################################

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()

# ############################################################################
# ########### Functions ############
# ##################################


def load_requirements(requirements_files: Union[Path, list[Path]]) -> list:
    """Helper to load requirements list from a path or a list of paths.

    Args:
        requirements_files (Union[Path, List[Path]]): path or list to paths of
            requirements file(s)

    Returns:
        list: list of requirements loaded from file(s)
    """
    out_requirements = []

    if isinstance(requirements_files, Path):
        requirements_files = [
            requirements_files,
        ]

    for requirements_file in requirements_files:
        with requirements_file.open(encoding="UTF-8") as f:
            out_requirements += [
                line
                for line in f.read().splitlines()
                if not line.startswith(("#", "-")) and len(line)
            ]

    return out_requirements


# ############################################################################
# ########## Setup #############
# ##############################
setup(
    name="mkdocs-rss-plugin",
    version=__about__.__version__,
    author=__about__.__author__,
    author_email=__about__.__email__,
    description=__about__.__summary__,
    license=__about__.__license__,
    long_description=README,
    long_description_content_type="text/markdown",
    project_urls={
        "Docs": "https://guts.github.io/mkdocs-rss-plugin/",
        "Bug Reports": f"{__about__.__uri__}issues/",
        "Source": __about__.__uri__,
    },
    # packaging
    packages=find_packages(
        exclude=["contrib", "docs", "*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    include_package_data=True,
    # run
    entry_points={"mkdocs.plugins": ["rss = mkdocs_rss_plugin.plugin:GitRssPlugin"]},
    # dependencies
    python_requires=">=3.9, <4",
    extras_require={
        # tooling
        "dev": load_requirements(HERE / "requirements/development.txt"),
        "doc": load_requirements(HERE / "requirements/documentation.txt"),
        "test": load_requirements(HERE / "requirements/testing.txt"),
    },
    install_requires=load_requirements(HERE / "requirements/base.txt"),
    # metadata
    keywords="mkdocs rss git plugin",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
)
