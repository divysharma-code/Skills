# Fax Intake Close Reason

_Calibration example for the Feature Documentation template. Source: Confluence
page "Fax Intake Close Reason" (https://coherehealth.atlassian.net/wiki/x/PIAQpQ,
Cohere Hub space, page 2769322044, under "Fax Intake - Misc Features"). Trimmed
to show the section order, voice and table shapes. Names and ticket keys are the
real ones from the page._

# Product Overview

## Feature Details

In an effort to allow payer specific fax close options (as they can have
different requirements for closing a case), we have implemented a new feature
in the Configuration Management which will allow us to have custom list of
close reasons for each payer without requiring a dev effort

- It is a backend feature and should not impact current user experience
- When we onboard new payers or want to change the close reasons for existing
  payers, can be done via Config Management by a PM or Dev leads

## Why We Built It

Previously, we had a single list of Fax close reasons "None of the above" that
was available across payers or we hard-coded custom logic configured for each
payer separately by the Developers

With multiple payers in Cohere environment, each of them have a specific list
of reasons that needs to be included.

## Known Gaps/Out of Scope

- The key identifiers are what get recorded irrespective of the Title/Option
  selected by the user
- If an outcome needs a separate logic/next step to be configured it has to be
  one of the existing ones

# Demo

## Step by Step Walkthrough

| Step | Action | Script |
| --- | --- | --- |
| Member look up screen | Click "Unable to work" | For this scenario we are going to assume that this is an unworkable case by the user but does not require a fax back to the provider. It could happen that the user does not have required skill set to complete the case. I would choose unable to work this case. |
| | Select a reason (+sub-reason if needed) | The expectation is that there are predefined unworkable scenarios for health plan that can be configured to document each of the fax close reasons. |
| | Move to next case | That's it, once I hit finish I can now move on to the next case. The case has been documented appropriately with the select close reason as an outcome. |

(A "NEW Addition!" block follows for a later change: what is changing, impact,
and the config snippet to add.)

## Demo Video

Loom link.

# Reporting and Analytics

- Kibana Dashboard: link to the saved view
- Where the value is recorded: `Outcome.outcome`

# Release Information

- Feature Flag: `useFaxCloseOptionConfiguration`
- Relevant user roles: Available to all QM users doing Fax intake
- Released across Payers, configurations set up done for Humana, GHP and
  Highmark

# Other Resources

## FAQ

1. Which work stream does this impact? (link to the workflow page)
2. What is the existing list of close reasons and their outcomes? (table:
   Payer | Close Reason | Identifier | Case Outcome)

## Documentation / Important Links

- Slack channel(s): N/A
- Initiative documents: N/A
- Designs: N/A
- Technical documentation: Feature Configuration Dictionary (link)
- Jira Epics (engineering projects): INTENG-1475

## Key Stakeholders

- PM Owner of functionality: @name
- Dev Lead: @name
- Informed: @name
