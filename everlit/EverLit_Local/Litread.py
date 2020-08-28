# -*- coding: utf-8 -*-
import re


class Literature:
    def __init__(self):
        self.author_abbr = None
        self.author_full = None
        self.author_APA = None
        self.title = None
        self.title_APA = None
        self.type = None
        self.publication = None
        self.abstract = None
        self.year = None
        self.bp = None
        self.ep = None
        self.ar = None
        self.doi = None
        self.citation_wos = None
        self.citation_all = None
        self.citation_strs = None


    def APA_citation_formation(self):
        """
        for APA style citation
        :return:
        """
        author_str = ''
        k = 1
        for author in self.author_APA:
            if k == len(self.author_APA):
                sub = ' '
                if len(self.author_APA) > 1:
                    pre = '& '
                else:
                    pre = ''
            else:
                sub = ', '
                pre = ''
            author_str += pre + author + sub
            k += 1
        year_str = '({}). '.format(self.year)

        title_str = self.title + '. '

        journal_title = self.publication.title_APA
        journal_comma = ', '
        journal_volume = self.publication.volume
        journal_issue = '({}), '.format(self.publication.issue) if len(self.publication.issue) > 0 else ''
        if self.bp != '':
            journal_page = '{}–{}.'.format(self.bp, self.ep)
        elif self.ar != '':
            journal_page = self.ar + '.'
        else:
            journal_page = '[ERROR]'
        final = [author_str, year_str, title_str, journal_title, journal_comma, journal_volume, journal_issue, journal_page]
        self.citation_strs = final


class Publication():
    def __init__(self):
        self.title = None
        self.year = None
        self.volume = None
        self.issue = None
        self.title_APA = None


def tab_win_utf_read(filepath):
    """
    reading data from WoS citation file.
    :param filepath: the path of your WoS literature data.
    :return: data in the form of dict
    """
    with open(filepath, 'r', encoding='utf-8') as file_object:
        first_line = file_object.readline()
        raw_data = file_object.readlines()

    lits = []
    for line in raw_data:
        if len(line) > 1:
            lit = single_lit_read(line)
            lits.append(lit)

    return lits


def single_lit_read(data_raw):
    """
    read single row of literature data
    :param data_raw: a list of literature record
    :return: a literature object.
    """
    strings = data_raw.split('\t')

    journal = Publication()
    journal.title = strings[9]
    journal.year = strings[44]
    journal.volume = strings[45]
    journal.issue = strings[46]
    journal.title_APA = journal_trans_APA(journal.title)

    lit = Literature()
    lit.author_abbr = strings[1]
    lit.author_full = strings[5]
    lit.author_APA = author_trans_APA(lit.author_abbr)
    lit.title = title_trans_APA(strings[8])
    lit.title_APA = title_trans_APA(lit.title)
    lit.type = strings[13]
    lit.abstract = strings[21]
    lit.citation_wos = strings[31]
    lit.citation_all = strings[32]
    lit.year = strings[44]
    lit.bp = strings[51]
    lit.ep = strings[52]
    lit.ar = strings[53]
    lit.doi = strings[54]
    lit.publication = journal
    lit.APA_citation_formation()

    return lit


def title_trans_APA(title):
    """
    transfer article title into APA style.
    :param title:
    :return:
    """
    data = title.split(':')
    trans = ''
    k = 1
    for d in data:
        if k != len(data):
            sub = ': '
        else:
            sub = ''
        trans += d.strip().lower().capitalize() + sub
        k += 1
    return trans


def journal_trans_APA(journal):
    """
    transfer journal title into APA style
    :param journal:
    :return:
    """
    trivial = ['OF', 'IN', 'AND', 'of']
    while True:
        word = re.search('[A-Z]{2,}', journal)
        if word is None:
            break
        else:
            word = word.group(0)

        journal = journal.replace(word, '{}')
        if word not in trivial:
            word = word.strip().lower().capitalize()
        else:
            word = word.strip().lower()
        journal = journal.format(word)

    return journal.strip()


def author_trans_APA(author_abbr):
    """
    transform wos author name abbreviation into format required by APA-6
    :param author_abbr: origininal abbreviation data from wos
    :return: author name abbreviation in APA-6 format
    """
    names = author_abbr.split(';')
    trans_data = []
    for name in names:
        last, remaining = name.split(',')
        last = last.strip().lower().capitalize()
        remaining = remaining.strip()
        trans_remain = []
        for char in remaining:
            trans_remain.append(char + '.')
        trans_data.append([last] + [trans_remain])

    trans_names = []
    for name in trans_data:
        final_name = ''
        final_name += name[0] + ', '
        for abbr in name[1]:
            final_name += abbr + ' '
        trans_names.append(final_name.strip())

    return trans_names


