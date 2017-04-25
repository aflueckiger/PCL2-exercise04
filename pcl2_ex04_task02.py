#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PCL II, exercise 04, spring 2017
# Task 2
# Authors: Nora Lötscher & Alex Flückiger
# Student-ID.: 09-110-552 & 12-452-223

"""
This module provides functions to download a Wikipedia dump and sample k titles
out of all article with the Reservoir Sampling algorithm.
"""

import urllib.request
import lxml.etree as ET
import bz2
import random
import sys


def progress_reporting(count, blocksize, totalsize):
    """
    This function reports the progress of downloaded blocks in console

    Args:
        count (int)
        blocksize (int)
        totalsize (int)
    """

    percent = int(count * blocksize / totalsize * 100)
    sys.stdout.write(f'\rDowloaded {percent:0d}% of requested file.')
    sys.stdout.flush()


def corpus_download(src_url, trg_xml):
    """
    This function downloads a source file from the internet and saves it locally.

    Args:
        src_url (str): URL of remote location
        trg_xml (str): local destination to save file
    """

    with open(trg_xml, 'w', encoding='utf-8') as f_xml:
        urllib.request.urlretrieve(
            src_url, filename=trg_xml, reporthook=progress_reporting)
        print(f'Corpus was downloaded successfully\n {trg_xml}')


def gettitles(infile, testfile, trainfile, k):
    """
    This functions iterates over Wikipedia-Dump and saves k random items
    into a testfile and all other elements into a trainfile.

    As sampling method the algorithm R is used (reservoir sampling).

    Args:
        infile (str or filehandler): file from which will be sampled
        testfile (str): file in which k random elements will be written
        trainfile (str): file in which all other elements will be written
        k (int): number of sample
    """

    # reservoir shows currently sampled items
    reservoir = []
    # t counts seen elements regardless whether they are sampled or not
    t = 0
    with open(testfile, 'w', encoding='utf-8') as f_test, \
            open(trainfile, 'w', encoding='utf-8') as f_train:
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

            # Some cleaning up to prevent memory issues
            element.clear()
            while element.getprevious() is not None:
                del element.getparent()[0]

        # write sampled items into file
        for article in reservoir:
            f_test.write(article + '\n')


def main():
    """
    Call functions to test script.
    """

    src_url = 'https://dumps.wikimedia.org/dewiki/latest/dewiki-latest-pages-articles.xml.bz2'
    trg_xml = 'dewiki-latest-pages-articles.xml.bz2'
    testfile = 'wikipedia_articles_testfile.txt'
    trainfile = 'wikipedia_articles_trainfile.txt'

    # corpus_download(src_url, trg_xml)

    with bz2.open(trg_xml, mode='r') as f_corpus:
        gettitles(f_corpus, testfile, trainfile, 26)


if __name__ == '__main__':
    main()
