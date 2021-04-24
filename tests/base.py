#! python3  # noqa E265

"""Base class for unit tests."""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import shutil
import unittest
from pathlib import Path

# 3rd party
from click.testing import CliRunner

# MkDocs
from mkdocs.__main__ import build_command
from mkdocs.config import load_config

# #############################################################################
# ########## Classes ###############
# ##################################


class BaseTest(unittest.TestCase):
    """Base test class to be inherited by MkDocs plugins tests."""

    @staticmethod
    def get_plugin_config_from_mkdocs(mkdocs_path: str, plugin_name: str) -> dict:
        """Load a mkdocs.yml and returns the configuration for the specified plugin.

        Args:
            mkdocs_path (str): path to MkDocs configuration file

        Returns:
            dict: plugin configuration loaded by MkDocs. Empty if specified plugin is \
            not enabled into the mkdocs.yml.
        """
        # instanciate plugin
        cfg_mkdocs = load_config(mkdocs_path)

        plugins = cfg_mkdocs.get("plugins")
        if "rss" not in plugins:
            logging.warning(
                f"Plugin {plugin_name} is not part of enabled plugin in the MkDocs "
                "configuration file: {mkdocs_path}"
            )
            return {}
        plugin_loaded = plugins.get("rss")

        cfg = plugin_loaded.on_config(cfg_mkdocs)
        logging.info("Fixture configuration loaded: " + str(cfg))

        return plugin_loaded.config

    def build_docs_setup(self, testproject_path: Path, mkdocs_yml_filepath: Path):
        """
        Runs the `mkdocs build` command

        Args:
            testproject_path (Path): Path to test project

        Returns:
            command: Object with results of command
        """
        try:
            runner = CliRunner()
            run = runner.invoke(build_command, ["--clean", "--config-file"])
            return run
        except Exception as err:
            logging.critical(err)
            raise

    def setup_clean_mkdocs_folder(
        self, mkdocs_yml_path: Path, output_path: Path
    ) -> Path:
        """
        Sets up a clean mkdocs directory

        outputpath/testproject
        ├── docs/
        └── mkdocs.yml

        Args:
            mkdocs_yml_path (Path): Path of mkdocs.yml file to use
            output_path (Path): Path of folder in which to create mkdocs project

        Returns:
            testproject_path (Path): Path to test project
        """

        testproject_path = output_path / "testproject"

        # Create empty 'testproject' folder
        if testproject_path.exists():
            logging.warning(
                """This command does not work on windows.
            Refactor your test to use setup_clean_mkdocs_folder() only once"""
            )
            shutil.rmtree(testproject_path)

        # Copy correct mkdocs.yml file and our test 'docs/'
        shutil.copytree("tests/fixtures/docs", testproject_path / "docs")
        shutil.copyfile(mkdocs_yml_path, testproject_path / "mkdocs.yml")

        return testproject_path

    def validate_mkdocs_file(self, temp_path: str, mkdocs_yml_file: str):
        """
        Creates a clean mkdocs project
        for a mkdocs YML file, builds and validates it.

        Args:
            temp_path (PosixPath): Path to temporary folder
            mkdocs_yml_file (PosixPath): Path to mkdocs.yml file
        """
        testproject_path = setup_clean_mkdocs_folder(
            mkdocs_yml_path=mkdocs_yml_file, output_path=temp_path
        )
        # setup_commit_history(testproject_path)
        # result = build_docs_setup(testproject_path)
        # assert result.exit_code == 0, "'mkdocs build' command failed"

        # # validate build with locale retrieved from mkdocs config file
        # validate_build(
        #     testproject_path, plugin_config=get_plugin_config_from_mkdocs(mkdocs_yml_file)
        # )

        return testproject_path


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    base = BaseTest()
    plg_cfg = base.get_plugin_config_from_mkdocs("mkdocs.yml", "rss")
    # print(plg_cfg)
    truc = base.setup_clean_mkdocs_folder(
        mkdocs_yml_path=Path("mkdocs.yml"), output_path=Path("tests/fixtures/")
    )
    print(truc)
