import pytest


def test_same_library_refresh_session_is_exclusive(tmp_path):
    from zotero_session import citation_session
    with citation_session(tmp_path, "synthetic-library", "first"):
        with pytest.raises(FileExistsError):
            with citation_session(tmp_path, "synthetic-library", "second"):
                pytest.fail("Concurrent session bypassed lease")
    with citation_session(tmp_path, "synthetic-library", "next"):
        pass


def test_distinct_libraries_do_not_share_lock(tmp_path):
    from zotero_session import citation_session
    with citation_session(tmp_path, "library-one", "first"):
        with citation_session(tmp_path, "library-two", "second"):
            pass
