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
from mkdocs.config.base import Config

# package
from mkdocs_rss_plugin.plugin import GitRssPlugin

# #############################################################################
# ########## Classes ###############
# ##################################


class BaseTest(unittest.TestCase):
    """Base test class to be inherited by MkDocs plugins tests."""

    def get_plugin_config_from_mkdocs(
        self, mkdocs_yml_filepath: Path, plugin_name: str
    ) -> Config:
        """Load a mkdocs.yml and returns the configuration for the specified plugin.

        :param mkdocs_yml_filepath: path to MkDocs configuration file
        :type mkdocs_yml_filepath: Path
        :param plugin_name: plugin name (as mentionned into the mkdocs.yml)
        :type plugin_name: str

        :return: plugin configuration loaded by MkDocs. Empty if specified plugin is \
        not enabled into the mkdocs.yml.
        :rtype: Config
        """
        # instantiate plugin
        cfg_mkdocs = load_config(str(mkdocs_yml_filepath.resolve()))

        plugins = cfg_mkdocs.plugins
        rss_plugin_instances = [
            plg for plg in plugins.items() if isinstance(plg[1], GitRssPlugin)
        ]
        if not len(rss_plugin_instances):
            logging.warning(
                f"Plugin {plugin_name} is not part of enabled plugin in the MkDocs "
                "configuration file: {mkdocs_yml_filepath}"
            )
            return cfg_mkdocs

        if len(rss_plugin_instances) == 1:
            plugin = rss_plugin_instances[0][1]
            self.assertIsInstance(plugin, GitRssPlugin)
        elif len(rss_plugin_instances) >= 1:
            plugin = rss_plugin_instances[1][1]
            self.assertIsInstance(plugin, GitRssPlugin)

        logging.info(f"Fixture configuration loaded: {plugin.on_config(cfg_mkdocs)}")

        return plugin.config

    def build_docs_setup(
        self,
        testproject_path: Path,
        mkdocs_yml_filepath: Path,
        output_path: Path,
        strict: bool = True,
    ):
        """Runs the `mkdocs build` command.

        :param testproject_path: Path to test project
        :type testproject_path: Path
        :param mkdocs_yml_filepath: filepath to the MkDocs configuration file (.yml) \
        passed as parameter to the `--config-file` argument.
        :type mkdocs_yml_filepath: Path
        :param output_path: folder path where to store the built website \
        passed as parameter to the `--site-dir` argument.
        :type output_path: Path

        :return: Object with results of command
        :rtype: click.testing.Result
        """
        cmd_args = [
            "--clean",
            "--config-file",
            f"{mkdocs_yml_filepath}",
            "--site-dir",
            f"{output_path}",
            "--verbose",
        ]
        if strict:
            cmd_args.append("--strict")

        try:
            runner = CliRunner()
            run = runner.invoke(build_command, cmd_args)
            return run
        except Exception as err:
            logging.critical(err)
            return False

    def setup_clean_mkdocs_folder(
        self, mkdocs_yml_filepath: Path, output_path: Path
    ) -> Path:
        """Sets up a clean mkdocs directory:

            outputpath/testproject
            ├── docs/
            └── mkdocs.yml

        :param mkdocs_yml_filepath: Path of mkdocs.yml file to use
        :type mkdocs_yml_filepath: Path
        :param output_path: Path of folder in which to create mkdocs project
        :type output_path: Path

        :return: Path to test project
        :rtype: Path
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
        shutil.copyfile(mkdocs_yml_filepath, testproject_path / "mkdocs.yml")

        return testproject_path

    # def validate_mkdocs_file(self, temp_path: Path, mkdocs_yml_filepath: str):
    #     """
    #     Creates a clean mkdocs project
    #     for a mkdocs YML file, builds and validates it.

    #     Args:
    #         temp_path (PosixPath): Path to temporary folder
    #         mkdocs_yml_filepath (PosixPath): Path to mkdocs.yml file
    #     """
    #     testproject_path = self.setup_clean_mkdocs_folder(
    #         mkdocs_yml_filepath=mkdocs_yml_filepath, output_path=temp_path
    #     )
    #     # setup_commit_history(testproject_path)
    #     # result = build_docs_setup(testproject_path)
    #     # assert result.exit_code == 0, "'mkdocs build' command failed"

    #     # # validate build with locale retrieved from mkdocs config file
    #     # validate_build(
    #     #     testproject_path, plugin_config=get_plugin_config_from_mkdocs(mkdocs_yml_filepath)
    #     # )

    #     return testproject_path


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """Quick and dirty tests"""
    import feedparser

    base = BaseTest()
    plg_cfg = base.get_plugin_config_from_mkdocs(Path("mkdocs.yml"), "rss")
    print(type(plg_cfg))
    # truc = base.setup_clean_mkdocs_folder(
    #     mkdocs_yml_filepath=Path("mkdocs.yml"), output_path=Path("tests/fixtures/")
    # )
    # print(truc)
    run_result = base.build_docs_setup(
        testproject_path="docs",
        mkdocs_yml_filepath=Path("mkdocs.yml"),
        output_path=Path("zoubi"),
    )
    print(type(run_result), run_result.exit_code)
    d = feedparser.parse("zoubi/feed_rss_created.xml")
    print(d.version)
