CTS-285 • Module 5

## M5.1 — Flask From the Outside In

A learner sees one action: submit an answer and get a response. A developer has to decide which part of the system should own each responsibility.

Developer question

**What should Flask own, what should remain reusable business logic, and what belongs at the data/state boundary?**

### One request, several responsibilities

**Request**
User input arrives

**Flask**
Receives and routes

**Logic**
Applies product rules

**Data/State**
Reads or preserves state

**Response**
User sees what happens next

Flask coordinates the web-facing part of that chain. It does not need to own the two-attempt rule, scoring rule, Memory Bank limit, or every persistence decision simply because those behaviors are triggered by a route.

**Keep this distinction in view:**

- **Framework/interface:** receive input, call the needed behavior, return a response.
- **Business logic:** apply DataMan rules independent of one particular interface.
- **Data/state boundary:** provide and preserve the information those rules need.

### Now test the boundary

The lab gives you a small DataMan request flow. You will decide where responsibilities belong, run the design, inspect the consequence, and revise when your placement makes the system harder to reuse, test, or maintain.

[Open the Flask Responsibility Lab](https://amlw05.github.io/cts-285-course-simulations/m5/flask-responsibility-lab/)

Watch for

A choice can appear to work and still create a weak boundary. Pay attention to what becomes harder to test, reuse, change, or retrieve after each decision.

**Nothing is submitted here.** Complete the lab, return to this Canvas tab, and use **Next**. You will use the lab findings before changing your own M4 prototype.
