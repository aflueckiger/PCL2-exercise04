#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PCL II, exercise 04, spring 2017
# Task 1
# Authors: Nora Lötscher & Alex Flückiger
# Student-ID.: 09-110-552 & 12-452-223

"""
This module provides functions to extract the 20 most common sentences
from multiple XML-files. To achieve this in an efficient way, XML-files
are parsed iteravely as well as generators and hashes are used.
"""

import glob
from lxml import etree as ET


def getfreqwords(indir, outfile):
    """
    This functions coordinates the extractions of sentences from multiple
    XML-files. Each unique sentence gets hashed and will be counted
    over the entire corpus. The 20 most frequent sentences will be written
    into a textfile.

    Args:
        indir (str): directory that contains XML-files
        outfile (str): textfile in which most common sentences will be written

    Return:
        None
    """
    count_sents = dict()
    # Asterisk is used as wildcard.
    file_pattern = indir + 'SAC-Jahrbuch_*_mul.xml'
    files = glob.glob(file_pattern)
    for file in files:
        for sent_lemm in extract_sents(file):
            unique_id = hash(sent_lemm)
            if unique_id in count_sents:
                counter = count_sents[unique_id][1]
                count_sents[unique_id] = (sent_lemm, counter + 1)
            else:
                count_sents[unique_id] = (sent_lemm, 1)

    # write 20 most common sentences into textfile
    with open(outfile, 'w', encoding='utf-8') as out_f:
        for key in sorted(count_sents, key=lambda x: count_sents[x][1],
                          reverse=True)[:20]:
            out_f.write(count_sents[key][0] + '\n')
            print(count_sents[key])


def extract_sents(file):
    """
    This function iterates over all sentences of an XML-file and
    yields each sentence consisting of lemmatized forms.
    However, only sentences with a minimu of 6 tokens are returned.

    Args:
        file (str): name of XML-file

    Yield:
        sent_processed (str): extracted sentence
    """

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
            yield ' '.join(current_sent)

        # Some cleaning up to prevent memory issues
        sent.clear()
        # Delete parent node of sentences if there is more than one sentence
        # Does not have any significant impact in this example
        while sent.getprevious() is not None:
            del sent.getparent()[0]


def main():
    """
    Call functions to test this module.
    """

    indir = 'Text+Berg_Release_152_v01/Corpus_XML/SAC/'
    outfile = 'frequent_lemmatized_sentences.txt'
    getfreqwords(indir, outfile)


if __name__ == '__main__':
    main()
