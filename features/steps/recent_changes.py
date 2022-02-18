# pylint: disable=E0611
from os import getcwd
from re import search
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
    updated_pattern = r'Last Updated: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\+|-)\d{2}:\d{2}'
    authored_pattern = r'Last Authored: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\+|-)\d{2}:\d{2}'
    assert search(updated_pattern, context.scanner_report), f'Last Updated date not found in {context.scanner_report} using {reporting_format}'
    assert search(authored_pattern, context.scanner_report), f'Last Authored date not found in {context.scanner_report} using {reporting_format}'
