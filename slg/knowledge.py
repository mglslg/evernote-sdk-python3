import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import time
from evernote.api.client import EvernoteClient
import requests
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
auth_token = "S=s25:U=1a56b7f:E=17646405917:C=1762233d170:P=1cd:A=en-devtoken:V=2:H=1cca0c7ee9aac7e1ff59bbab3b80104e"
if auth_token == "your developer token":
    print("Please fill in your developer token")
    print("To get a developer token, visit " \
          "https://sandbox.evernote.com/api/DeveloperToken.action")
    exit(1)
sandbox = False
china = True
client = EvernoteClient(token=auth_token, sandbox=sandbox, china=china)
user_store = client.get_user_store()
version_ok = user_store.checkVersion(
    "Evernote EDAMTest (Python)",
    UserStoreConstants.EDAM_VERSION_MAJOR,
    UserStoreConstants.EDAM_VERSION_MINOR
)
print("Is my Evernote API version up to date? ", str(version_ok))
print("")
if not version_ok:
    exit(1)


def print_notebooks():
    note_store = client.get_note_store()
    notebooks = note_store.listNotebooks()
    print("Found ", len(notebooks), " notebooks:")
    for notebook in notebooks:
        print("  * ", notebook.stack, ":", notebook.name, ":", notebook.guid)


def add_note(url):
    html = requests.post(url).content
    content = str(html, 'utf-8')
    print(content)

    note_store = client.get_note_store()
    note = Types.Note()
    note.title = time.strftime('%Y%m%d', time.localtime()) + "文档测试"
    note.notebookGuid = "9a295350-5659-47c6-a6f8-568eccfdaedc"

    # The content of an Evernote note is represented using Evernote Markup Language
    # (ENML). The full ENML specification can be found in the Evernote API Overview
    # at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
    note.content = '<?xml version="1.0" encoding="UTF-8"?>'
    note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'

    note.content += '<en-note>'
    note.content += 'hello'
    note.content += '</en-note>'

    #created_note = note_store.createNote(note)

    #print("Successfully created a new note with GUID: ", created_note.guid)


if __name__ == '__main__':
    url = "https://blog.csdn.net/IT_DREAM_ER/article/details/105396716"
    # print_notebooks()
    add_note(url)
