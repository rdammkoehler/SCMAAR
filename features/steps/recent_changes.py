# pylint: disable=E0611
from os import getcwd

from behave import given, when, then

from scmaar.scanner import scan


@given('a source code repository')
def given_current_source_directory_is_cwd(context):
    context.source_directory = getcwd()


@when('the repository is scanned')
def when_scanned(context):
    context.scanner_report = scan(context.source_directory)


@then('the date and time of the most recent change is reported in "{reporting_format}"')
def then_report_contains_last_updated_with_format(context, reporting_format):
    assert 'Last Updated:' in context.scanner_report, f'Last Updated date not found using {reporting_format}'
