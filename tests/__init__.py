# redirect every mkdocs.* import to properdocs.* before any test module (or the
# plugin itself) imports MkDocs, so that only ProperDocs classes are used.
import properdocs.replacement  # noqa: F401
