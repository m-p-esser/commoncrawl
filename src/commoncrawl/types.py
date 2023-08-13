""" Common Crawl Data types """

from dataclasses import dataclass, field
from urllib.parse import ParseResult, urlparse


@dataclass(slots=True)
class Link:
    """Class to store Link data"""

    link: str
    _url: ParseResult = field(init=False, repr=False)
    hostname: str = field(init=False, default_factory=str)
    protocol: str = field(init=False, default_factory=str)
    path: str = field(init=False, default_factory=str)

    def __post_init__(self) -> ParseResult:
        """Extract different URL components"""
        self._url = urlparse(self.link)
        self.hostname = self._url.netloc
        self.protocol = self._url.scheme
        self.path = self._url.path


@dataclass(kw_only=True, slots=True)
class LinkCollection:
    """Generic Class for collecting links from a single WAT file"""

    warc_target_uri: str
    warc_record_id: str
    links: list[Link] = field(default_factory=list)

    def count_number_links(self) -> int:
        """Count Number of Links"""
        return len(self.links)


@dataclass
class InternalLinkCollection(LinkCollection):
    """These links navigate to a different section of the same page or to another page within the same website"""


@dataclass
class ExternalLinkCollection(LinkCollection):
    """These links navigate to a different website. They are used to reference external resources or websites"""


@dataclass
class AnchorLinkCollection(InternalLinkCollection):
    """These are links that point to a specific part of a webpage using an anchor (#). They are often used for "jump to" functionality"""


#    # /products/books/sci-fi
#    path_pattern = re.compile(r'^https?:\/\/[^\/]+(\/[^\?#]*)?')

#    # https://*
#    # ftp://*"
#    # mailto//*
#    protocol_pattern = re.compile(r'^([a-zA-Z][a-zA-Z0-9+.-]*):')

#    # www.example.org
#    host_name_pattern = re.compile(r'^https?://([^:/?#]+)')

#    # 123.123.123.123
#    ip_pattern = re.compile(r'^(?:www\.)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\Z')

#    http_redirect_pattern = re.compile(b'^HTTP\\s*/\\s*1\\.[01]\\s*30[12378]\\b')

#    robotstxt_warc_path_pattern = re.compile(r'.*/robotstxt/')
#    robotstxt_sitemap_pattern = re.compile(b'^Sitemap:\\s*(\\S+)',
#                                            re.IGNORECASE)
