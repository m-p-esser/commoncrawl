import src.commoncrawl.types as cc_types


def test_number_links():
    lc = cc_types.LinkCollection(
        warc_target_uri="dummy_uri",
        warc_record_id="dummy_id",
        links=["https://example.com", "https://test.org"],
    )
    assert lc.number_links() == 2


def test_parse_urls():
    lc = cc_types.LinkCollection(
        warc_target_uri="dummy_uri",
        warc_record_id="dummy_id",
        links=["https://example.com/path", "https://test.org"],
    )
    parsed_urls = lc.parse_urls()
    assert len(parsed_urls) == 2
    assert parsed_urls[0].netloc == "example.com"
    assert parsed_urls[0].path == "/path"
    assert parsed_urls[1].netloc == "test.org"


def test_extract_hostnames():
    lc = cc_types.LinkCollection(
        warc_target_uri="dummy_uri",
        warc_record_id="dummy_id",
        links=["https://example.com", "https://test.org"],
    )
    lc.extract_hostnames()
    assert lc.hostnames == ["example.com", "test.org"]


def test_extract_protocols():
    lc = cc_types.LinkCollection(
        warc_target_uri="dummy_uri",
        warc_record_id="dummy_id",
        links=["https://example.com", "http://test.org"],
    )
    lc.extract_protocols()
    assert lc.protocols == ["https", "http"]


def test_extract_path_from_url():
    lc = cc_types.LinkCollection(
        warc_target_uri="dummy_uri",
        warc_record_id="dummy_id",
        links=["https://example.com/path1", "https://test.org/path2"],
    )
    lc.extract_path_from_url()
    assert lc.paths == ["/path1", "/path2"]
