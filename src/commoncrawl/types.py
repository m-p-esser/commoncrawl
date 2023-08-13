""" Common Crawl Data types """

from dataclasses import dataclass
from urllib.parse import ParseResult, urlparse


@dataclass
class LinkCollection:
    """Generic Class for collecting links from a single WAT file"""

    warc_target_uri: str
    warc_record_id: str
    links: list[str]
    hostnames: list[ParseResult.hostname] = None
    protocols: list[ParseResult.scheme] = None
    paths: list[ParseResult.path] = None

    def number_links(self) -> int:
        """Count Number of Links"""
        return len(self.links)

    def parse_urls(self) -> list[ParseResult]:
        """Convert Links to URLs"""
        urls = [urlparse(link) for link in self.links]
        return urls

    def extract_hostnames(self) -> list[ParseResult.netloc]:
        """Extract hostnames from URLs"""
        self.hostnames = [url.netloc for url in self.parse_urls()]

    def extract_protocols(self) -> list[ParseResult.hostname]:
        """Extract Web Protocols from URLs"""
        self.protocols = [url.scheme for url in self.parse_urls()]

    def extract_path_from_url(self) -> list[ParseResult.path]:
        """Extract Paths (following hostnames) from URLs"""
        self.paths = [url.path for url in self.parse_urls()]


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
