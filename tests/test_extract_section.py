from unittest import TestCase
from src.interfaces.abstract_collector import HTTPInfo


class TestExtractSection(TestCase):

    @staticmethod
    def _build_http_info(path):
        return HTTPInfo(method='GET',
                        host='http://bing.it',
                        path=path,
                        content_length=100)

    def test_extract_section_1(self):
        http_info = TestExtractSection._build_http_info('/section/subsection')
        section = http_info.extract_section()
        self.assertEqual(section, http_info.host + '/section')

    def test_extract_section_2(self):
        http_info = TestExtractSection._build_http_info('/section')
        section = http_info.extract_section()
        self.assertEqual(section, http_info.host + '/section')

    def test_extract_section_3(self):
        http_info = TestExtractSection._build_http_info('/')
        section = http_info.extract_section()
        self.assertEqual(section, http_info.host + '/')

    def test_extract_section_4(self):
        http_info = TestExtractSection._build_http_info('')
        section = http_info.extract_section()
        self.assertEqual(section, http_info.host)

    def test_extract_section_5(self):
        http_info = TestExtractSection._build_http_info('/section/subsection/subsubsection')
        section = http_info.extract_section()
        self.assertEqual(section, http_info.host + '/section')

    def test_extract_section_6(self):
        http_info = TestExtractSection._build_http_info('//section')
        section = http_info.extract_section()
        self.assertEqual(section, http_info.host + '/')
