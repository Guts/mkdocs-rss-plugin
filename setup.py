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

# ############################################################################
# ########## Setup #############
# ##############################
setup(
    name="mkdocs-rss-plugin",
    version=__about__.__version__,
    author=__about__.__author__,
    author_email=__about__.__email__,
    description=__about__.__summary__,
    license="GPL3",
    long_description=README,
    long_description_content_type="text/markdown",
    project_urls={
        "Docs": "https://guts.github.io/mkdocs-rss-plugin/",
        "Bug Reports": "{}issues/".format(__about__.__uri__),
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
    python_requires=">=3.6, <4",
    extras_require={
        "dev": ["black", "flake8", "pre-commit"],
        "test": ["pytest", "pytest-cov"],
    },
    install_requires=[
        "GitPython==3.1.*",
        "Jinja2>=2,<3",
        "mkdocs>=1.1,<1.3",
    ],
    # metadata
    keywords="mkdocs rss git plugin",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
