# Project Instructions

This project is an agent harness for building a Rasa-powered airline customer service assistant.

The assistant should eventually help with airline customer service tasks such as:

- checking flight upgrade eligibility
- explaining baggage policies
- helping users change or cancel flights
- answering flight status questions
- escalating to a human agent when needed

## Working Rules

Whenever you implement a new feature or make changes, always:

1. train the model
2. have a few conversations with the trained agent to confirm the changes behave as intended
3. report back the transcripts to stdout as simple markdown

## Development Style

Work slowly and safely.

Before making changes:
- inspect the existing project structure
- explain what files need to change
- make the smallest useful change first

After making changes:
- run validation where possible
- train the model
- test with example conversations
- summarize what worked and what failed

## First Milestone

Create a basic airline customer service assistant that can:

1. greet the user
2. understand that the user wants a flight upgrade
3. ask for booking reference if missing
4. ask for destination or flight details if needed
5. provide a simple placeholder response explaining that upgrade eligibility will be checked
6. gracefully handle unclear requests