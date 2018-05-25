from behave import *

use_step_matcher("parse")

@when(u'I create genre')
def step_impl(context):
    context.browser.visit('/bookworm/genre/add/')
    context.browser.fill(context.table.headings[0], context.table[context.table.headings[0]])
    context.browser.find_by_tag('form').find_by_value("Submit").click()


@then(u'There are {count:numgenres} genres in my genre list')
def step_impl(context, numgenres):
    context.browser.visit('/bookworm/home/')
    divs = context.browser.find_by_xpath('/html/body/main/div')
    assert len(divs) == numgenres
