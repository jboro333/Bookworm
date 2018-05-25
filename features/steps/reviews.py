from behave import *

use_step_matcher("parse")

@given(u'A review for book "{book}"')
def step_impl(context, book):
    from books.models import Book
    book = Book.objects.filter(name=book)[0]
    context.browser.visit('/bookworm/book/' + str(book.id) + '/review/add/')
    for parameter in context.table.headings:
        context.browser.fill(parameter, context.table[parameter])
    context.browser.find_by_tag('form').find_by_value("Submit").click()
    

@when(u'I create review for book {book}')
def step_impl(context, book):
    from books.models import Book
    book = Book.objects.filter(name=book)[0]
    context.browser.visit('/bookworm/book/' + str(book.id) + '/review/add/')
    for parameter in context.table.headings:
        context.browser.fill(parameter, context.table[parameter])
    context.browser.find_by_tag('form').find_by_value("Submit").click()

@when(u'I delete review')
def step_impl(context):
    table = context.table
    context.browser.visit('/bookworm/home')
    link = context.browser.find_by_xpath('/html/body/main/div[1]/div[2]/a[2]')
    link.click()


@then(u'There are {count:numreviews} reviews in my review list')
def step_impl(context, numreviews):
    context.browser.visit('/bookworm/home/')
    divs = context.browser.find_by_xpath('/html/body/main/div')
    assert len(divs) == numreviews
