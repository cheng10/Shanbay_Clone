from __future__ import print_function

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Shanbay_Clone.settings')

import django

django.setup()

from words.models import Word, VocaBook


# populate the database with *nix system word list


def populate():
    # read first N lines from wordlist
    N = 50
    word_file = "wordlist.txt"
    booklist = ["GRE", "CET4", "CET6"]

    with open(word_file) as myfile:
        head = [next(myfile) for _ in range(N)]
    # print (head)

    # remove "\n" in the words
    head = [word.replace("\n", "") for word in head]

    # populate word
    for _ in head:
        add_word(text=_,
                 desc="This is the description for word " + _,
                 sentence="This is the example sentence for word " + _,
                 )

    # populate book
    for book in booklist:
        add_book(book)

    GRE = VocaBook.objects.get(bookname="GRE")
    CET4 = VocaBook.objects.get(bookname="CET4")
    CET6 = VocaBook.objects.get(bookname="CET6")

    for word in head:
        GRE.word.add(Word.objects.get(text=word))

    for idx, word in enumerate(head):
        if idx % 2 == 0:
            CET4.word.add(Word.objects.get(text=word))
        else:
            CET6.word.add(Word.objects.get(text=word))

    for book in VocaBook.objects.all():
        book.save()

    # Print out what we have added to the user.
    for w in Word.objects.all():
        print(w.text)


def add_word(text, desc, sentence):
    w = Word.objects.get_or_create(text=text)[0]
    w.desc = desc
    w.sentence = sentence
    w.save()
    return w


def add_book(bookname):
    b = VocaBook.objects.get_or_create(bookname=bookname)
    return b


# Start execution here!
if __name__ == '__main__':
    print("Starting Shanbay_Clone population script...")
    populate()
