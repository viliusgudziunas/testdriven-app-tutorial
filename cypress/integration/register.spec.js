import { generate } from "randomstring";

const username = generate();
const email = `${username}@test.com`;

describe("Register", () => {
  it("should display the registration form", () => {
    cy.visit("/register")
      .get("h1")
      .contains("Register")
      .get("form")
      .get("input[disabled]")
      .get(".validation-list")
      .get(".validation-list > .error")
      .first()
      .contains("Username must be greater than 5 characters");
  });

  it("should allow a user to register", () => {
    cy.visit("/register")
      .get("input[name='username']")
      .type(username)
      .get("input[name='email']")
      .type(email)
      .get("input[name='password']")
      .type("test")
      .get("input[type='submit']")
      .click();

    cy.contains("All Users");
    cy.contains(username);
    cy.get(".navbar-burger").click();
    cy.get(".navbar-menu").within(() => {
      cy.get(".navbar-item")
        .contains("User Status")
        .get(".navbar-item")
        .contains("Log Out")
        .get(".navbar-item")
        .contains("Log In")
        .should("not.be.visible")
        .get(".navbar-item")
        .contains("Register")
        .should("not.be.visible");
    });
  });
});
