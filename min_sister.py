#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import os
import re
import shutil
import unittest

from bs4 import BeautifulSoup

class MinSisterTest(unittest.TestCase):
    longMessage = True

    def setUp(self):
        return

    def test_min_keyword(self):
        ''' make wget command string
        '''
        rset = set()

        for i in range(1, 145):
        # for i in range(10, 11):
            r = open('html/%d.html' % i)
            content = r.read()
            soup = BeautifulSoup(content, "html.parser")
            selector = ".html-attribute-value.html-external-link"
            result = soup.select(selector)
            for r in result:
                m = re.match(r'\d+\.201\d+', r.text)
                if m:
                    rset.add('wget http://www.mediagaon.or.kr/jsp/sch/common/popup/newsviewpopup.jsp?newsId={id} -O list/{id}.html'.format(id=r.text))
            r.close()
        sorted_rset = sorted(rset)
        for i in sorted_rset:
            print i

    def test_all_in_one(self):
        lists = [os.path.join('list', i) for i in os.listdir('list')]
        result_map = {}
        for i in lists:
            r = open(i)
            content = r.read()
            r.close()
            soup = BeautifulSoup(content, "html.parser")
            selector = ".news_view span"
            result = soup.select(selector)
            items = result[0].text.replace('[', '').replace(']', '').split()

            title_selector = '.news_view h3'
            title = soup.select(title_selector)[0].text.encode('UTF-8')
            text_selector = '.news_view p'
            text = [t.encode('UTF-8') for t in soup.select(text_selector)[0].text.split('.')]

            key = '{0}.{1}.{2}'.format(items[0], items[4].replace('·', '.'), items[5].replace(',', '.'))
            if key in result_map:
                result_map[key].append({
                    'content': content,
                    'title': title,
                    'text': text,
                })
            else:
                result_map[key] = [{
                    'content': content,
                    'title': title,
                    'text': text,
                }]

        all_in_one = 'all-in-one.md'
        all_in_one_content = []
        aw = open(all_in_one, 'w')

        for key, li in result_map.items():
            for idx, item in enumerate(li):
                # create html
                file_name = '{0}.{1}.html'.format(key, idx)
                file_path = os.path.join('list_with_title', file_name)

                w = open(file_path, 'w')
                w.write(item['content'])
                w.close()

                # create text only file
                text_file_name = '{0}.{1}.txt'.format(key, idx)
                text_file_path = os.path.join('list_with_text', text_file_name)

                tw = open(text_file_path, 'w')
                tw.write(item['title']+'\n')
                for br in item['text']:
                    tw.write(br+'\n')
                tw.close()

                all_in_one_content.append('# {0}\n\n'.format(file_name))
                all_in_one_content.append('- 제목 : `{0}`\n'.format(item['title']))

                all_in_one_content.append('- 본문\n\n')
                all_in_one_content.append('```\n')
                for br in item['text']:
                    all_in_one_content.append(br)
                    all_in_one_content.append('.\n')
                all_in_one_content.append('```\n')
                all_in_one_content.append('\n\n')

        aw.writelines(all_in_one_content)
        aw.close()
        shutil.copy(all_in_one, 'all-in-one.txt')

if __name__ == '__main__':
    unittest.main(verbosity=2)
