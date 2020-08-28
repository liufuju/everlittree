# -*- coding: utf-8 -*-
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
import os, re, time


def template_read(tempFilePath):
    with open(tempFilePath, 'r', encoding='UTF-8') as file_object:
        data = file_object.readlines()
    template = ''
    for line in data:
        template += line

    return template


def xml_check(content):
    marks = ['&', '\'', '"', '>', '<']
    mark_entity = ['&amp;', '&apos;', '&quot;', '&gt;', '&lt;']
    for i in range(len(marks)):
        content = content.replace(marks[i], mark_entity[i])
    return content


def single_lit_note(lit, template, note_store):
    note = Types.Note()

    authors = lit.author_abbr.split(';')
    first_author = re.search('\w+', authors[0].split(',')[0]).group(0)
    note.title = '{} | {} | {} | {}'.format(lit.type.split(';')[0], lit.year, first_author, lit.title_APA)

    old_content = ['{{ author full name }}', '{{ author string }}', '{{ year string }}', '{{ title string }}',
                   '{{ journal title }}', '{{ journal volume }}', '{{ journal issue }}', '{{ journal page }}',
                   '{{ abstract }}']
    new_content = [lit.author_full, lit.citation_strs[0], lit.citation_strs[1], lit.citation_strs[2],
                   lit.citation_strs[3], lit.citation_strs[5], lit.citation_strs[6], lit.citation_strs[7], lit.abstract]

    for i in range(len(new_content)):
        new_content[i] = xml_check(new_content[i])

    # replace the content
    for i in range(len(old_content)):
        template = template.replace(old_content[i], new_content[i])
    note.content = template
    created_note = note_store.createNote(note)

    return created_note


def create_catalog(notes, client, catalogTempPath, singleCataTempPath):
    catalog_template = template_read(catalogTempPath)
    single_cata_template = template_read(singleCataTempPath)

    user_store = client.get_user_store()
    note_store = client.get_note_store()
    user = user_store.getUser()
    userId = user.id
    shardId = user.shardId
    link_temp = 'evernote:///view/{}/{}/'.format(userId, shardId) + '{{ GUID }}/{{ GUID }}'

    catalog_content = ''
    for note in notes:
        guid = note.guid
        link = link_temp.replace('{{ GUID }}', guid)
        new_content = single_cata_template.replace('{{ note link }}', link)
        new_content = new_content.replace('{{ note title }}', note.title)
        catalog_content += new_content
    final_catalog = catalog_template.replace('{{ content }}', catalog_content)

    catalog_note = Types.Note()
    localtime = time.asctime(time.localtime(time.time()))
    catalog_note.title = 'Catalog | {}'.format(localtime)
    catalog_note.content = final_catalog
    created_catalog = note_store.createNote(catalog_note)

    return created_catalog


def create_notes_online(client, lits, template):
    # user_store = client.get_user_store()
    note_store = client.get_note_store()

    new_notes = []
    for lit in lits:
        created_note = single_lit_note(lit, template, note_store)
        new_notes.append(created_note)

    return new_notes


def create_catalog_online(new_notes, client, catalog_template, single_cata_template):
    user_store = client.get_user_store()
    note_store = client.get_note_store()
    user = user_store.getUser()
    userId = user.id
    shardId = user.shardId
    link_temp = 'evernote:///view/{}/{}/'.format(userId, shardId) + '{{ GUID }}/{{ GUID }}'

    catalog_content = ''
    for note in new_notes:
        guid = note.guid
        link = link_temp.replace('{{ GUID }}', guid)
        new_content = single_cata_template.replace('{{ note link }}', link)
        new_content = new_content.replace('{{ note title }}', note.title)
        catalog_content += new_content
    final_catalog = catalog_template.replace('{{ content }}', catalog_content)

    catalog_note = Types.Note()
    localtime = time.asctime(time.localtime(time.time()))
    catalog_note.title = 'Catalog | {}'.format(localtime)
    catalog_note.content = final_catalog
    created_catalog = note_store.createNote(catalog_note)

    return created_catalog
