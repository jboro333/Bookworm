Feature: Devote Genre
    In order to keep updated how I qualified the book, 
    As a user, 
    I want to invalid the vote and change it.

Background: There is a registered user
    Given Exists a user "testuser" with password "testpassword"
    And A book "BookA" by author "AuthA"
    And A genre named "Genre1"
    And A vote by "testuser" of "Genre1" on "BookA"

Scenario: Create vote
    Given I login as user "testuser" with password "testpassword"
    When I vote or devote genre "Genre1" in book "BookA"
    Then "Genre1" has 0 votes in "BookA"
