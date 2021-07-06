#!/usr/bin/env python3

"""
Package: oeis
SEQUENCE DATA FROM OEIS
http://psychedelic-geometry.blogspot.com/
Author: Enrique Pérez Herrero
Date:    14-Jun-2021
Updated: 14-May-2019
"""

import re
import requests

OEIS_URL = 'http://oeis.org/'

TEXT_TAGS = {
    'id': "%I",
    'description': "%N",
    'terms_tags': ["%S", "%T", "%U"],
    'comments': "%C",
    'links': "%H",
    'formula': "%F",
    'author': "%A",
    'keywords': "%K",
    'crossrefs': "%Y",
    'offset': "%O",
    'keywords': "%K"
}

def oeis_md_link(id_):
    return f'[{id_}]({OEIS_URL}{id_})'


class OEIS_Sequence:
    def __init__(self, id_):
        self.id = id_
        self.url = self.oeis_url(id_)
        self.text_url = self.oeis_text_url(id_)
        self.internal_format = self.oeis_internal_format(self.text_url)
        self.description = self.oeis_description(self.internal_format)
        self.terms = self.oeis_terms(self.internal_format)
        self.authors = self.oeis_authors(self.internal_format)
        self.keywords = self.oeis_keywords(self.internal_format)
        self.crossrefs = self.oeis_crossrefs(self.internal_format)
        self.comments = self.oeis_comments(self.internal_format)
        self.license = self.oeis_license(self.internal_format)

    @classmethod
    def oeis_url(cls, id_):
        return f"{OEIS_URL}{id_}"

    @classmethod
    def oeis_text_url(cls, id_):
        return f"{OEIS_URL}search?q=id:{id_}&fmt=text"

    @classmethod
    def oeis_internal_format(cls, text_url):
        internal_format = requests.get(text_url)
        # response.encoding = "utf-8"
        return internal_format.text

    @classmethod
    def oeis_text_lines(cls, internal_format, tag):
        internal_format = internal_format.split("\n")
        return [line for line in internal_format if TEXT_TAGS[tag] in line]

    @classmethod
    def oeis_text_line(cls, internal_format, tag):
        return cls.oeis_text_lines(internal_format, tag)[0]

    @classmethod
    def oeis_get_id(cls, internal_format):
        id_ = cls.oeis_text_line(internal_format, 'id')
        return id_.split(" ")[1]

    @classmethod
    def oeis_description(cls, internal_format):
        id_ = cls.oeis_get_id(internal_format)
        desc = cls.oeis_text_line(internal_format, 'description')
        return desc.split(id_)[1].strip()

    @classmethod
    def oeis_terms(cls, internal_format):
        id_ = cls.oeis_get_id(internal_format)
        terms = ""
        internal_format = internal_format.split("\n")
        for line_tag in TEXT_TAGS['terms_tags']:
            data_line = [line for line in internal_format if line_tag in line]
            if data_line:
                # when terms line exists
                data_line = data_line[0].split(id_)[1].strip()
                terms = terms + data_line
        return [int(x) for x in terms.split(",")]
    
    @classmethod
    def oeis_comments(cls, internal_format):
        id_ = cls.oeis_get_id(internal_format)
        comments = cls.oeis_text_lines(internal_format, "comments")
        comments  = [line.split(id_)[1].strip() for line in comments]
        return comments

    @classmethod
    def oeis_authors(cls, internal_format):
        id_ = cls.oeis_get_id(internal_format)
        authors_line = cls.oeis_text_line(internal_format, 'author')
        authors_line = authors_line.split(id_)[1]
        if "," in authors_line:
            authors_line = authors_line.split(",")[0]
        authors_line = authors_line.strip().replace("_", "")
        return authors_line

    @classmethod
    def oeis_keywords(cls, internal_format):
        id_ = cls.oeis_get_id(internal_format)
        keywords = cls.oeis_text_line(internal_format, 'keywords')
        keywords = keywords.split(id_)[1].strip()
        return keywords.split(",")

    @classmethod
    def oeis_crossrefs(cls, internal_format):
        id_ = cls.oeis_get_id(internal_format)
        crossrefs = cls.oeis_text_lines(internal_format, "crossrefs")
        crossrefs = [line.split(id_)[1] for line in crossrefs]
        crefs = []
        for line in crossrefs:
            crefs = crefs + re.findall(r"A\d{6}", line)
        return crefs

    @classmethod
    def oeis_license(cls, internal_format):
        return internal_format.split("\n")[-2].split("# ")[1]



