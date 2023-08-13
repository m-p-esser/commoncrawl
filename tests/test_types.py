from urllib.parse import ParseResult

import src.commoncrawl.types as cc_types


def test_url_parsed_sucessfully():
    link = "https://test.org"
    l = cc_types.Link(link)
    assert isinstance(l._url, ParseResult)
    assert len(l._url) > 0


def test_hostname_parsed_sucessfully():
    link = "https://test.org"
    l = cc_types.Link(link)
    assert isinstance(l.hostname, str)
    assert l.hostname == "test.org"


def test_protocol_parsed_sucessfully():
    link = "https://test.org"
    l = cc_types.Link(link)
    assert isinstance(l.protocol, str)
    assert l.protocol == "https"


def test_path_parsed_sucessfully():
    link = "https://test.org/random-path"
    l = cc_types.Link(link)
    assert isinstance(l.path, str)
    assert l.path == "/random-path"


def test_count_number_links():
    lc = cc_types.LinkCollection(
        warc_target_uri="dummy_uri",
        warc_record_id="dummy_id",
        links=["https://example.com", "https://test.org"],
    )
    assert lc.count_number_links() == 2
