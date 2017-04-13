#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PCL II, exercise 04, spring 2017
# Task 1
# Authors: Nora Lötscher & Alex Flückiger
# Student-ID.: 09-110-552 & 12-452-223

"""
Module Description XXXX
"""

import glob
from lxml import etree as ET
from collections import Counter


def getfreqwords(indir, outfile):
    count_sents = Counter()
    file_pattern = indir + 'SAC-Jahrbuch_*_mul.xml'
    files = glob.glob(file_pattern)
    for file in files:
        count_sents.update(extract_sents(file))

    with open(outfile, 'w', ) as out_f:
        for sent, _ in count_sents.most_common(20):
            out_f.write(sent + '\n')

    # Call control function to print output in console
    print_sents(count_sents)


def print_sents(count_sents):
    print('Anzahl einmalige Sätze: ', len(count_sents))
    print('20 häufigste Sätze:')
    for sent in count_sents.most_common(20):
        print(sent)


def extract_sents(file):
    for _, sent in ET.iterparse(file, tag='s'):
        current_sent = []
        for word in sent.iterfind('.//w'):
            try:
                lemma = word.attrib['lemma']
                current_sent.append(lemma)
            except KeyError:
                # Continue if lemma does not exist for a specific word
                # In our SAC corpus there are several Swiss german words
                # without lemmas
                pass

        if len(current_sent) >= 6:
            # print(current_sent)
            yield ' '.join(current_sent)
        sent.clear()
        # Delete parent node of sentences if there is more than one sentence
        # Does not have any significant impact in this example
        while sent.getprevious() is not None:
            del sent.getparent()[0]


def main():
    """
    Call functions to test script.
    """

    indir = '/home/alex/Text+Berg_Release_152_v01/Corpus_XML/SAC/'
    outfile = 'frequent_lemmatized_sentences.txt'
    getfreqwords(indir, outfile)


if __name__ == '__main__':
    main()
