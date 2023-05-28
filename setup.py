#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pathlib

# 3rd party
from setuptools import find_packages, setup

# package (to get version)
from mkdocs_rss_plugin import __about__

# ############################################################################
# ########## Globals #############
# ################################

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

with open(HERE / "requirements/base.txt") as f:
    requirements = [
        line
        for line in f.read().splitlines()
        if not line.startswith(("#", "-")) and len(line)
    ]

with open(HERE / "requirements/development.txt") as f:
    requirements_dev = [
        line
        for line in f.read().splitlines()
        if not line.startswith(("#", "-")) and len(line)
    ]


with open(HERE / "requirements/documentation.txt") as f:
    requirements_docs = [
        line
        for line in f.read().splitlines()
        if not line.startswith(("#", "-")) and len(line)
    ]


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
    python_requires=">=3.8, <4",
    extras_require={
        "dev": requirements_dev,
        "doc": requirements_docs,
    },
    install_requires=requirements,
    # metadata
    keywords="mkdocs rss git plugin",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
)
