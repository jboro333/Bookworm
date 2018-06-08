Feature: Delete Review
  In order to delete a review I made for a specific book, 
  As a user, 
  I want to delete the whole review.


Background: There is a registered user
    Given Exists a user "testuser" with password "testpassword"
    And A book "BookA" by "AuthorA"
    And A review for book "BookA"
      | title   | score | text      |
      | WOW     | 8     | Good book |

Scenario: Delete review
    Given I login as user "testuser" with password "testpassword"
    When I delete review
      | title   | score | text      |
      | WOW     | 8     | Good book |
    Then There are 0 reviews in my review list