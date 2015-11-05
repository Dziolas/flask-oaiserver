# -*- coding: utf-8 -*-
#
# This file is part of Flask-OAIServer
# Copyright (C) 2015 CERN.
#
# Flask-OAIServer is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

from __future__ import absolute_import
from unittest import TestCase
from flask import g
from flask_oaiserver.oai import app
from flask_oaiserver.config import *
import re


class FlaskTestCase(TestCase):

    """Mix-in class for creating the Flask application"""

    def setUp(self):
        self.app = app
        self.app.testing = True
        pass

    def tearDown(self):
        pass


class TestVerbs(FlaskTestCase):

    """Tests OAI-PMH verbs"""

    def test_no_verb(self):
        with self.app.test_client() as c:
            result = c.get('/oai2d', follow_redirects=True)
            response_date = getattr(g, 'response_date', None)
            expected = """<?xmlversion="1.0"encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{0}</responseDate>
    <error code="badValue">This is not a valid OAI-PMH verb:None</error>
</OAI-PMH>""".format(response_date)
            result_data = result.data.decode("utf-8")
            result_data = re.sub(' +', '', result_data.replace('\n', ''))
            expected = re.sub(' +', '', expected.replace('\n', ''))
            self.assertEqual(result_data, expected)

    def test_wrong_verb(self):
        with self.app.test_client() as c:
            result = c.get('/oai2d?verb=Aaa', follow_redirects=True)
            response_date = getattr(g, 'response_date', None)
            expected = """<?xmlversion="1.0"encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{0}</responseDate>
    <error code="badValue">This is not a valid OAI-PMH verb:Aaa</error>
</OAI-PMH>""".format(response_date)
            result_data = result.data.decode("utf-8")
            result_data = re.sub(' +', '', result_data.replace('\n', ''))
            expected = re.sub(' +', '', expected.replace('\n', ''))
            self.assertEqual(result_data, expected)

    def test_identify(self):
        ########
        # TODO - remove all placeholder values
        ########
        with self.app.test_client() as c:
            result = c.get('/oai2d?verb=Identify', follow_redirects=True)
            response_date = getattr(g, 'response_date', None)
            expected = """<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{0}</responseDate>
    <request verb="Identify">{1}</request>
    <Identify>
        <repositoryName>{2}</repositoryName>
        <baseURL>http://memory.loc.gov/cgi-bin/oai</baseURL>
        <protocolVersion>2.0</protocolVersion>
        <adminEmail>{3}</adminEmail>
        <earliestDatestamp>1990-02-01T12:00:00Z</earliestDatestamp>
        <deletedRecord>transient</deletedRecord>
        <granularity>YYYY-MM-DDThh:mm:ssZ</granularity>
        <compression>deflate</compression>
     </Identify>
</OAI-PMH>""".format(response_date, oai_url, CFG_SITE_NAME, CFG_ADMIN_EMAIL)
            result_data = result.data.decode("utf-8")
            result_data = re.sub(' +', '', result_data.replace('\n', ''))
            expected = re.sub(' +', '', expected.replace('\n', ''))
            self.assertEqual(result_data, expected)

    def test_identify_with_additional_args(self):
        with self.app.test_client() as c:
            result = c.get('/oai2d?verb=Identify&notAValidArg=True',
                           follow_redirects=True)
            response_date = getattr(g, 'response_date', None)
            expected = """<?xmlversion="1.0"encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{0}</responseDate>
    <request verb="Identify" notAValidArg="True">{1}</request>
    <error code="badArgument">
        You have passed too many arguments together withEXLUSIVE argument.
    </error>
</OAI-PMH>""".format(response_date, oai_url)
            result_data = result.data.decode("utf-8")
            result_data = re.sub(' +', '', result_data.replace('\n', ''))
            expected = re.sub(' +', '', expected.replace('\n', ''))
            self.assertEqual(result_data, expected)

    def test_list_sets(self):
        with self.app.test_client() as c:
            result = c.get('/oai2d?verb=ListSets',
                           follow_redirects=True)
            response_date = getattr(g, 'response_date', None)
            expected = """<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{0}</responseDate>
    <requestverb="ListSets">{1}</request>
    <ListSets>
        <set>
            <setSpec>music</setSpec>
            <setName>Music collection</setName>
            <setDescription>
                <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                           xmlns:dc="http://purl.org/dc/elements/1.1/"
                           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                           xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
                           http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                    <dc:description>This is a collection of wide range of music.</dc:description>
                </oai_dc:dc>
            </setDescription>
        </set>
        <set>
            <setSpec>music:(chopin)</setSpec>
            <setName>Chopin collection</setName>
            <setDescription>
                <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                           xmlns:dc="http://purl.org/dc/elements/1.1/"
                           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                           xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
                           http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                    <dc:description>Collection of music composed by Chopin</dc:description>
                </oai_dc:dc>
            </setDescription>
        </set>
        <set>
            <setSpec>music:(techno)</setSpec>
            <setName>Techno music collection</setName>
        </set>
        <set>
            <setSpec>pictures</setSpec>
            <setName>Pictures collection</setName>
        </set>
    </ListSets>
</OAI-PMH>""".format(response_date, oai_url)
            result_data = result.data.decode("utf-8")
            result_data = re.sub(' +', '', result_data.replace('\n', ''))
            expected = re.sub(' +', '', expected.replace('\n', ''))
            self.assertEqual(result_data, expected)

    def test_list_sets_with_resumption_token(self):
        with self.app.test_client() as c:
            result = c.get('/oai2d?verb=ListSets',
                           follow_redirects=True)
            response_date = getattr(g, 'response_date', None)
            expected = """<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>{0}</responseDate>
    <requestverb="ListSets">{1}</request>
    <ListSets>
        <set>
            <setSpec>music</setSpec>
            <setName>Music collection</setName>
            <setDescription>
                <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                           xmlns:dc="http://purl.org/dc/elements/1.1/"
                           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                           xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
                           http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                    <dc:description>This is a collection of wide range of music.</dc:description>
                </oai_dc:dc>
            </setDescription>
        </set>
        <set>
            <setSpec>music:(chopin)</setSpec>
            <setName>Chopin collection</setName>
            <setDescription>
                <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                           xmlns:dc="http://purl.org/dc/elements/1.1/"
                           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                           xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
                           http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                    <dc:description>Collection of music composed by Chopin</dc:description>
                </oai_dc:dc>
            </setDescription>
        </set>
        <set>
            <setSpec>music:(techno)</setSpec>
            <setName>Techno music collection</setName>
        </set>
        <set>
            <setSpec>pictures</setSpec>
            <setName>Pictures collection</setName>
        </set>
        <resumptionToken expirationDate="{2}" completeListSize="{3}" cursor="{4}">{5}</resumptionToken>
    </ListSets>
</OAI-PMH>""".format(response_date, oai_url, exp_date, list_size, coursor, token)
            result_data = result.data.decode("utf-8")
            result_data = re.sub(' +', '', result_data.replace('\n', ''))
            expected = re.sub(' +', '', expected.replace('\n', ''))
            self.assertEqual(result_data, expected)

    def test_list_sets_with_extra_argument(self):
        pass
