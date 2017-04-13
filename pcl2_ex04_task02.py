#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PCL II, exercise 04, spring 2017
# Task 2
# Authors: Nora Lötscher & Alex Flückiger
# Student-ID.: 09-110-552 & 12-452-223

"""
Module Description XXXX
"""

import urllib.request
import lxml.etree as ET
import bz2
import random
import sys


def progress_reporting(count, blocksize, totalsize):
    percent = int(count * blocksize / totalsize * 100)
    sys.stdout.write(f'\rDowloaded {percent:0d}% of requested file.')
    sys.stdout.flush()


def corpus_download(src_url, trg_xml):
    with open(trg_xml, 'w', encoding='utf-8') as f_xml:
        urllib.request.urlretrieve(
            src_url, filename=trg_xml, reporthook=progress_reporting)
        print(f'Corpus was downloaded successfully\n {trg_xml}')


def gettitles(infile, testfile, trainfile, k):
    """
    Returns @param k random nodes from @param iterable.
    """
    reservoir = []
    t = 0
    with open(testfile, 'w', encoding='utf-8') as f_test, open(trainfile, 'w', encoding='utf-8') as f_train:
        elements = ET.iterparse(infile)
        for _, element in elements:
            if element.tag == '{http://www.mediawiki.org/xml/export-0.10/}title':
                if t < k:
                    reservoir.append(element.text)
                else:
                    m = random.randint(0, t)
                    if m < k:
                        f_train.write(reservoir[m] + '\n')
                        reservoir[m] = element.text 
                    else:
                        f_train.write(element.text + '\n')
                t += 1
            element.clear()
            while element.getprevious() is not None:
                del element.getparent()[0]
        """
        elements = ET.iterparse(infile, tag == '{http://www.mediawiki.org/xml/export-0.10/}title')
        for t, node in enumerate(elements):
            elem_title = node[1]
            if t < k:
                reservoir.append(elem_title.text)
            else:
                m = random.randint(0, t)
                if m < k:
                    f_train.write(reservoir[m] + '\n')
                    reservoir[m] = elem_title.text 
                else:
                    f_train.write(elem_title.text + '\n')
            elem_title.clear()
            while elem_title.getprevious() is not None:
                del elem_title.getparent()[0]
        """
        for article in reservoir:
            f_test.write(article + '\n')


def main():
    """
    Call functions to test script.
    """
    src_url = 'https://dumps.wikimedia.org/dewiki/latest/dewiki-latest-pages-articles.xml.bz2'
    trg_xml = '/home/alex/dewiki-latest-pages-articles.xml.bz2'
    testfile = '/home/alex/wikipedia_articles_testfile.txt'
    trainfile = '/home/alex/wikipedia_articles_trainfile.txt'
    # corpus_download(src_url, trg_xml)

    with bz2.open(trg_xml, mode='r') as f_corpus:
        gettitles(f_corpus, testfile, trainfile, 100)


if __name__ == '__main__':
    main()
