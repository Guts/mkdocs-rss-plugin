#! python3  # noqa: E265

"""Usage from the repo root folder:

.. code-block:: python

    # for whole test
    python -m unittest tests.test_rss_util

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# 3rd party
from requests.exceptions import SSLError
from validator_collection import checkers

# plugin target
from mkdocs_rss_plugin.util import Util


# #############################################################################
# ########## Classes ###############
# ##################################
class TestRssUtil(unittest.TestCase):
    """Test plugin tools."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        cls.config_files = sorted(Path("tests/fixtures/").glob("**/*.yml"))
        cls.feed_image = "https://github.com/Guts/mkdocs-rss-plugin/blob/main/docs/assets/logo_rss_plugin_mkdocs.png?raw=true"
        cls.plg_utils = Util()

    def setUp(self):
        """Executed before each test."""
        pass

    def tearDown(self):
        """Executed after each test."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        pass

    # -- TESTS ---------------------------------------------------------
    def test_build_url(self):
        """Test URL builder."""
        # without URL parameters
        item_url = self.plg_utils.build_url(
            base_url="https://guts.github.io/mkdocs-rss-plugin/", path="changelog"
        )
        self.assertTrue(checkers.is_url(item_url))

        # with URL parameters
        item_url = self.plg_utils.build_url(
            base_url="https://guts.github.io/mkdocs-rss-plugin/",
            path="changelog",
            args_dict={"utm_source": "test_rss"},
        )
        print(item_url)
        self.assertTrue(checkers.is_url(item_url))

    def test_local_image_ok(self):
        """Test local image length calculation."""
        img_length = self.plg_utils.get_local_image_length(
            page_path="docs/index.md", path_to_append="assets/rss_icon.svg"
        )
        self.assertIsInstance(img_length, int)

    def test_local_image_none(self):
        """Test local image length calculation on non-existing image."""
        img_length = self.plg_utils.get_local_image_length(
            page_path="docs/index.md", path_to_append="inexisting_image.svg"
        )
        self.assertIsNone(img_length)

    def test_remote_image_ok(self):
        """Test remote image length calculation."""
        img_length = self.plg_utils.get_remote_image_length(image_url=self.feed_image)
        self.assertIsInstance(img_length, int)

    def test_remote_image_none(self):
        """Test remote image length calculation on unreachable image."""
        img_length = self.plg_utils.get_remote_image_length(
            image_url="https://guts.github.io/mkdocs-rss-plugin/inexisting.svg"
        )
        self.assertIsNone(img_length)

    def test_remote_image_ssl_error_not_retried(self):
        """TLS failures must not be retried, especially without verification."""
        with patch.object(
            self.plg_utils.req_session, "request", side_effect=SSLError("bad cert")
        ) as mock_request:
            img_length = self.plg_utils.get_remote_image_length(
                image_url="https://self-signed.example.org/image.png"
            )

        self.assertIsNone(img_length)
        mock_request.assert_called_once()
        self.assertNotIn("verify", mock_request.call_args.kwargs)

    def test_authors_invalid_type_logs_warning(self):
        """An invalid authors type must log a warning, not raise an exception."""
        page = MagicMock()
        page.file.abs_src_path = "docs/page.md"
        page.meta = {"authors": 42}

        with self.assertLogs("properdocs.plugins.[RSS-plugin]", "WARNING") as logs:
            authors = self.plg_utils.get_authors_from_meta(in_page=page)

        self.assertIsNone(authors)
        self.assertIn("docs/page.md", logs.output[0])
        self.assertIn("int", logs.output[0])

    def test_get_value_from_dot_key(self):
        param_list = [
            {
                "meta": {"date": "2021-09-01"},
                "value_location": "date",
                "value": "2021-09-01",
            },
            {
                "meta": {"date": {"created": "2021-09-01"}},
                "value_location": "date.created",
                "value": "2021-09-01",
            },
            {
                "meta": {"date": "2021-09-01"},
                "value_location": "date.created",
                "value": None,
            },
            {
                "meta": {True: "bool_as_key"},
                "value_location": True,
                "value": "bool_as_key",
            },
            {
                "meta": {"date": "2021-09-01"},
                "value_location": True,
                "value": None,
            },
        ]
        for param in param_list:
            with self.subTest(param=param):
                result = self.plg_utils.get_value_from_dot_key(
                    param["meta"], param["value_location"]
                )
                self.assertEqual(result, param["value"])


class TestFeedDescription(unittest.TestCase):
    """Test description sources and comment removal before excerpt truncation."""

    def setUp(self):
        self.utils = Util(use_git=False)
        self.page = MagicMock()
        self.page.meta = {}
        self.page.content = None
        self.page.markdown = ""
        self.page.file.src_uri = "page.md"

    def test_strip_html_comments(self):
        cases = [
            ("", ""),
            ("<p>Visible</p>", "<p>Visible</p>"),
            ("Before<!-- internal -->after", "Beforeafter"),
            ("Before<!-- internal\nmultiline -->after", "Beforeafter"),
            ("<!-- first --><p>Visible</p><!-- second -->", "<p>Visible</p>"),
            ("&lt;!-- example --&gt;", "&lt;!-- example --&gt;"),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(self.utils.strip_html_comments(source), expected)

    def test_truncation_does_not_expose_partial_comment(self):
        self.page.markdown = (
            "Début. <!-- note interne très longue qui sera coupée -->\n\nFin."
        )
        self.assertEqual(
            self.utils.get_description_or_abstract(self.page, chars_count=25),
            "<p>Début. </p>\n<p>Fin.</p>",
        )

    def test_comments_do_not_consume_character_limit(self):
        self.page.markdown = f"<!-- {'x' * 80} -->Visible content"
        self.assertEqual(
            self.utils.get_description_or_abstract(self.page, chars_count=50),
            "<p>Visible content</p>",
        )

    def test_visible_content_is_still_truncated(self):
        self.page.markdown = "<!-- internal -->" + "0123456789" * 8
        self.assertEqual(
            self.utils.get_description_or_abstract(self.page, chars_count=20),
            "<p>01234567890123456...</p>",
        )

    def test_delimiter_is_located_before_stripping_comments(self):
        for delimiter in ("<!-- more -->", "[CUT]"):
            for chars_count in (0, 5, 160):
                with self.subTest(delimiter=delimiter, chars_count=chars_count):
                    self.page.markdown = (
                        f"Intro <!-- internal -->text.\n\n{delimiter}\n\nAfter."
                    )
                    self.assertEqual(
                        self.utils.get_description_or_abstract(
                            self.page,
                            chars_count=chars_count,
                            abstract_delimiter=delimiter,
                        ),
                        "<p>Intro text.</p>",
                    )

    def test_empty_or_missing_delimiter_uses_character_limit(self):
        self.page.markdown = "<!-- internal -->0123456789"
        for delimiter in (None, "", "<!-- more -->"):
            with self.subTest(delimiter=delimiter):
                self.assertEqual(
                    self.utils.get_description_or_abstract(
                        self.page, chars_count=8, abstract_delimiter=delimiter
                    ),
                    "<p>01234...</p>",
                )

    def test_metadata_descriptions(self):
        for meta in (
            {"description": "<b>Visible</b><!-- internal\nnote -->"},
            {
                "description": "SEO description",
                "rss": {"feed_description": "<b>Visible</b><!-- internal\nnote -->"},
            },
        ):
            with self.subTest(meta=meta):
                self.page.meta = meta
                self.page.markdown = "Unused <!-- more -->body"
                self.assertEqual(
                    self.utils.get_description_or_abstract(
                        self.page, chars_count=5, abstract_delimiter="<!-- more -->"
                    ),
                    "<b>Visible</b>",
                )

    def test_full_content_takes_precedence_over_metadata_and_delimiter(self):
        self.page.meta = {"description": "Unused description"}
        self.page.markdown = "Unused <!-- more -->markdown"
        self.page.content = "<p>Visible</p><!-- internal\nnote --><p>After</p>"
        self.assertEqual(
            self.utils.get_description_or_abstract(
                self.page, chars_count=-1, abstract_delimiter="<!-- more -->"
            ),
            "<p>Visible</p><p>After</p>",
        )

    def test_full_content_falls_back_to_markdown(self):
        self.page.markdown = "Before<!-- internal\nnote -->after"
        self.assertEqual(
            self.utils.get_description_or_abstract(self.page, chars_count=-1),
            "<p>Beforeafter</p>",
        )

    def test_comment_examples_in_markdown_excerpts_are_removed(self):
        self.page.markdown = "```html\n<!-- example -->\n```\n\nVisible"
        description = self.utils.get_description_or_abstract(self.page)
        self.assertNotIn("example", description)
        self.assertIn("Visible", description)

    def test_escaped_code_examples_in_full_content_are_preserved(self):
        self.page.content = (
            "<pre><code>&lt;!-- example --&gt;</code></pre><!-- internal -->"
        )
        self.assertEqual(
            self.utils.get_description_or_abstract(self.page, chars_count=-1),
            "<pre><code>&lt;!-- example --&gt;</code></pre>",
        )

    def test_empty_descriptions(self):
        for source, chars_count in (("", 160), ("Visible", 0)):
            with self.subTest(source=source, chars_count=chars_count):
                self.page.markdown = source
                self.assertEqual(
                    self.utils.get_description_or_abstract(
                        self.page, chars_count=chars_count
                    ),
                    "",
                )


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
