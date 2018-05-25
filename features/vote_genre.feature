Feature: Vote Genre
    In order to punctuate how suitable the genre is for a concrete book, 
    As a user, 
    I want to give my vote to it.


Background: There is a registered user, a book and a genre
    Given Exists a user "testuser" with password "testpassword"
    And A book "BookA" by author "AuthA"
    And A genre named "Genre1"

Scenario: Create vote
    Given I login as user "testuser" with password "testpassword"
    When I vote or devote genre "Genre1" in book "BookA"
    Then "Genre1" has 1 votes in "BookA"
