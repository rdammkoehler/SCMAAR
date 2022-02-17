# Created by rpd at 2/17/22
Feature: Most Recent Change
  # Enter feature description here

  Scenario: Most Recent Change Reported In Plain Text
    Given a source code repository
    When the repository is scanned
    Then the date and time of the most recent change is reported in "plain text"

