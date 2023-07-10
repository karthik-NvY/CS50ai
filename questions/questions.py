import nltk
import sys
import os
import re
import string
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as sw

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens
    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    data = {}  # Dictionary to be returned.
    for filename in os.listdir(directory):  # Iterates over all files.
        if re.fullmatch(".+\.txt", filename):  # Matches .txt files
            with open(os.path.join(directory, filename), "r") as file:
                file_data = file.read()  # Reads the whole file.
                data[filename] = file_data
    return data


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = []  # List to be returned.
    for each in word_tokenize(document):  # Iterates over all words.
        if each not in string.punctuation:  # Removes all puncutations.
            """
            The following if-condition removes some unnecessary words.
            \\displaystyle and \\textstyle are unnecessary HTML elements.
            == is contained at side of headings after reading file.
            These elemenets are unnecessary so I took the liberty to remove them.
            """
            if "\\displaystyle" in each or "\\textstyle" in each or "==" in each:
                continue
            if each not in sw.words("english") and len(each):  # Removes stopwords.
                words.append(each.lower())  # Adds lowercase words.
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = {}  # Dictionary to be returned.
    no_of_doc = len(documents)  # Total number of documents.
    for file in documents:
        for word in documents[file]:
            if word not in words:
                count = 0
                for each in documents.values():
                    if word in each:
                        count += 1  # Counts documents with a word.
                words[word] = math.log(no_of_doc/count)  # idf formula.
    return words


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_scores = {}  # Dictionary containing each file's score i.e tf_idf
    for file in files:
        score = 0
        for word in query:
            if word in files[file]:
                tf = files[file].count(word)
                tf_idf = tf * idfs[word]
                score += tf_idf  # Calculation of score.
        file_scores[file] = score
    files_list = list(file_scores.keys())  # List of all files.

    # Sorts files with their tf_idf.
    files_list.sort(key=lambda x: file_scores[x], reverse=True)
    return files_list[:n]  # Returns first n files.


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentences_list = []  # Contains (sentence, idf_score, qtd_score)

    # Following loop calculates idf and qtd scores and populates sentences_list.
    for sentence in sentences:
        score = 0
        qtd = 0
        for word in query:
            if word in sentences[sentence]:
                score += idfs[word]  # Calculation of idf score.
                qtd += 1  # Calculation of idf score.
        sentences_list.append((sentence, score, qtd / len(query)))

    # Sorts sentences_list with their idf scores.
    sentences_list.sort(key=lambda x: x[1], reverse=True)

    # List to contain sentences after sorting according to qtd scores.
    sorted_sentences_list = []

    # Following loop populates sorted_sentences_list.
    for i in range(len(sentences_list)):
        tmp_list = []

        # Following loop checks for sentences with same idf scores.
        while (i != len(sentences_list)-1) and (sentences_list[i][1] == sentences_list[i+1][1]):
            tmp_list.append(sentences_list[i])
            i += 1
        if len(tmp_list) != 0:
            tmp_list.append(sentences_list[i])
            tmp_list.sort(key=lambda x: x[2], reverse=True)  # Sorts according to qtd score.
            for each in tmp_list:
                sorted_sentences_list.append(each[0])
        else:
            sorted_sentences_list.append(sentences_list[i][0])
    return sorted_sentences_list[:n]  # Returns first n sentences.


if __name__ == "__main__":
    main()