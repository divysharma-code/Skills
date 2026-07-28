# mom-tracker reference

## 1. MOM template variants

All variants share this shell — no YAML frontmatter, ever:

```
# <Meeting Title> — Notes (<YYYY-MM-DD>, <start time>, <duration/scheduled vs actual if it ran over>)

<1-2 sentence intro: what kind of meeting, who, what it covered>

## 1. <First section>
...
## N. <Last section — always ends with>
## Reference
- Meeting: Fellow note_id <id> / meeting_id `<id>`
- Recording: recording_id <id>          (omit if no recording)
- People to follow up with: <names + why>   (omit if none)
```

Filename: `<local_mom_dir>/<YYYY-MM-DD>-<slug>.md`.

### 1:1 / knowledge-share
Use when one person is walking the user through a domain/process (onboarding
1:1s, SME knowledge-shares).

Sections: `Framework`/`Process` table (Stage | What they do | What it
filters out, or similar) → `Domain Concepts` (subheadings per topic, mix of
prose + tables/diagrams) → `Insights & Inferences` (bulleted — things to
treat as open questions or verify before repeating) → `Reference`.

### Weekly rollup
Use when covering multiple meetings from a week rather than one call.

Sections: `Progress` (bulleted, grouped by theme/workstream) → `Plans`
(table: Item | Owner | From) → `Problems / Open Items` (bulleted, flag
anything unverified) → `Reference` (table: Date | Meeting | Fellow note_id).

### Discussion / brainstorm 1:1
Use for two-way working sessions, demos, or debates between peers.

Sections: `<Person>'s Beliefs & Rationale` (table: Belief | Why) → `What Was
Demoed`/`What Was Discussed` (bulleted, grouped by person/topic) →
`Decisions Made` (bulleted) → `Open / Unresolved` (bulleted — name the
disagreement explicitly, don't smooth it over) → `Action Items` (table:
Action | Owner | Notes) → `Questions Raised` (table: Question | Asked by |
To | Why it mattered) → `Reference`.

### Strategy / belief-mapping (decode)
Use when one senior/dominant voice (a manager, mentor, or stakeholder) is
laying out a worldview, strategic bet, or philosophy the user needs to
absorb and act on — even if the user talks plenty, the meeting's center of
gravity is decoding *why* that person believes what they believe.

Sections: `Context & Core Belief` (the blunt opening premise, 1 short
paragraph) → a variable number of numbered narrative sections that walk the
logic thread-by-thread as it actually unfolded (name each by its content,
e.g. "Market structure: who currently owns the customer?" — not "Section 2";
use bullets/sub-bullets for reasoning, tables only where there's a real
comparison, like a market-share breakdown) → `Questions Asked in the
Meeting` (see §2 below — usually the thematic-cluster format, since these
conversations tend to be exploratory) → `How <Person>'s Thinking Is Decoded`
(numbered list; each entry = a short bold one-line frame + 1-3 sentences
unpacking the incentive/mental-model behind it — this is specifically about
reverse-engineering *their* reasoning, not the user's own insights) →
`What You Should Take Away` (2-4 blunt, pragmatic bullets — no inflated or
"motivational poster" language) → `Reference`.

### Choosing a variant
- Covering several meetings from one week → **Weekly rollup**.
- One SME teaching the user a domain/process, the user mostly the learner →
  **1:1 / knowledge-share**.
- Two peers exchanging/demoing on roughly equal footing → **Discussion /
  brainstorm**.
- One person (usually senior) laying out a strategic worldview the user
  needs to decode and act on → **Strategy / belief-mapping**.
- Doesn't cleanly fit one variant → mix sections. The shell (H1 + intro +
  numbered H2s + closing Reference) matters more than which exact sections
  appear.

## 2. Questions section format

Two valid formats — pick based on the meeting's shape, don't default to one:

- **Attribution table** (`Question | Asked by | To | Why it mattered`) —
  use when there are few participants, turn-taking is clear, and *who*
  asked matters for understanding the exchange (e.g. two peers debating).
- **Thematic clusters** — use when questions are numerous, often rhetorical,
  or mostly probing from one dominant voice exploring a problem space (e.g.
  a strategy session). Group under short category headings (e.g. "Market +
  strategy questions", "Trust / credibility questions") as a bulleted list
  under each; only tag `[asked by X]` inline where the asker isn't the
  meeting's default questioner or otherwise not obvious.

Don't force attribution onto a thematic conversation, and don't flatten a
tight back-and-forth into anonymous theme buckets — match the format to how
the conversation actually happened.

## 3. Tracker sheet column schema

Sheet: `MOM Tracker` (spreadsheet_id in `SKILL.md` frontmatter), tab `Log`.

| Col | Header | Contents |
|---|---|---|
| A | Date | `YYYY-MM-DD` of the meeting |
| B | Meeting Type | One value from §4 below |
| C | Attendees | Comma-separated names |
| D | MOM Doc | `=HYPERLINK(url_or_path, label)` — local file path or Google Doc URL |
| E | Topic | Short free-text tag, e.g. "Sprint Planning", "Design Research", "PPP Updates" |
| F | Fellow Note ID | The `note_id` from Fellow, for traceability back to the recording |

Row-finding: `read_sheet_values` on `Log!A:A`, first fully-empty row past
the header is the write target. Never use `append_table_rows` — this sheet
has no Sheets "Table" object defined.

## 4. Meeting Type taxonomy

Guess from attendees' roles/teams (via `get_meeting_participants`) + the
meeting title/summary — always show the guess at the confirm gate, never
commit it silently.

- `Meeting with Engineering`
- `Meeting with Design`
- `Meeting with Product`
- `Meeting with Data`
- `Meeting with Business`
- `1:1`
- `Standup`
- `Grooming`
- `Onboarding`

If none fit well, ask for the right label rather than forcing one of the
above.
