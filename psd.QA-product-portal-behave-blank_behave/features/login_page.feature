Feature: Login on PP

@login
Scenario Outline: Validate Successful Login
    Given I am at a Login page
    When I fill in the Email with <credential>
    And I click on Next button
    And I fill in the field password with <credential>
    And I click on Sign In button
    Then The current page is Home page

    Examples:
    |credential         |
    |valid credential   |

Scenario Outline: Validate Failed Login
    Given I am at a Login page
    When I try to Login
    Then An error message appears

    Examples:
    |credential         |
    |no username        |
    |no password        |
