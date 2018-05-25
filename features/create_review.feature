Feature: Create Review
    In order to give my personal opinion on a book I read, 
    As a user, 
    I want to explain what impression the book gave me.


  
Background: There is a registered user
    Given Exists a user "testuser" with password "testpassword"
    And A book "BookA" by author "AuthA"

Scenario: Create review
    Given I login as user "testuser" with password "testpassword"
    When I create review for book "BookA"
      | title   | score | text      |
      | WOW     | 8     | Good book |
    Then There are 1 reviews in my review list