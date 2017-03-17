'''
'''
import sys
import re
from functools import partial

from bs4 import BeautifulSoup

import parse_lib as pl
from macro_utils import flatten_one_layer
from postprocess_mark_references import (get_reference_requests_from_pairs,
                                         get_reference_url_from_standard_location)


def find_reference_html_in_sections(refs_from_pairs, section_listing):
    refs_to_record = set(flatten_one_layer(refs_from_pairs))
    references = {get_reference_url_from_standard_location((page, sect_id)):
                  section_listing[page][sect_id]
                  for page, sect_id in refs_to_record}
    refs_with_resolved_resource_urls = {k: resolve_relative_resource_urls(v)
                                        for k, v in references.items()}
    cleaned_references = {k: pl.clean_html(v) for k, v in refs_with_resolved_resource_urls.items()}
    return cleaned_references

def resolve_relative_resource_urls(html_string):
    html = BeautifulSoup(html_string, 'html.parser')
    anchors = html.find_all('a', href=True)
    imgs = html.find_all("img", src=True)
    equations = html.find_all("object", data=True)
    list(map(resolve_anchor_href, anchors))
    list(map(partial(resolve_resource, 'src'), imgs))
    list(map(partial(resolve_resource, 'data'), equations))
    return str(html)

def resolve_anchor_href(anchor):
    if not has_protocol_prefix(anchor):
        try:
            page, fragment_id = anchor['href'].split('#')
            resolved_page = 'part03.html' if page == '' else page
            anchor['href'] = resolved_page + '#' + fragment_id
        except ValueError:
            pass
        anchor['href'] = pl.BASE_DICOM_URL + anchor['href']


def has_protocol_prefix(anchor):
    return re.match(r'(http)|(ftp)', anchor['href'])


def resolve_resource(url_attribute, resource):
    resource[url_attribute] = pl.BASE_DICOM_URL + resource[url_attribute]


if __name__ == '__main__':
    module_attr_pairs = pl.read_json_to_dict(sys.argv[1])
    section_listing = pl.read_json_to_dict(sys.argv[2])
    refs_to_record = get_reference_requests_from_pairs(module_attr_pairs)
    references = find_reference_html_in_sections(refs_to_record, section_listing)
    pl.write_pretty_json(references)
