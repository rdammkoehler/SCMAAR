from os import getcwd

from behave import given, when, then

from scmaar.scanner import scan

@given(u'a source code repository')
def step_impl(context):
    context.source_directory = getcwd()


@when(u'the repository is scanned')
def step_impl(context):
    context.scanner_report = scan(context.source_directory)


@then('the date and time of the most recent change is reported in "{reporting_format}"')
def step_impl(context, reporting_format):
    assert 'Last Updated:' in context.scanner_report, 'Last Updated date not found'
