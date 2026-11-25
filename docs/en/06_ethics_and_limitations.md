# 06. Ethics, data protection and limitations

This document states how personal data are handled, where the scope of the system ends,
and which limitations should be read alongside the results in Section 5.

## Personal data

The usage evidence in `data/` was produced for administrative analysis of a tool in
operation. It was minimised before publication. Aggregation happened at the extraction
boundary, so identifiers never left the production environment, and the tables in this
repository contain no user identifier, e-mail address, session identifier, message text
or network metadata.

Group labels were replaced by codes assigned in random order before publication, so
neither the codes nor the row order carry information about group size, scope or
chronology. Active accounts are reported in bands, and rates per account are withheld
for groups with fewer than six accounts, so that no published cell describes one or two
identifiable accounts. The material is compatible with the Brazilian General Data
Protection Law because it contains no personal data as defined in Article 5, I. Users are
identified in the internal reports for administrative purposes only, and those reports
are not part of this repository.

## Scope boundaries

The system answers epidemiological questions about populations. Individual clinical advice
is outside its scope, and when a request crosses that boundary the appropriate response is
to say so rather than to answer. The usage record shows that this boundary is tested in
practice, which is why it is stated as a design rule and not only as a disclaimer.

Documents uploaded by a user are treated as data, not as instructions. This is the
practical defence against content that tries to redirect the system through its own
payload.

## Verification of claims

Numbers that appear in a report come from an operation result or from the script that
assembled the table, never from model memory. Bibliographic references are resolved
against bibliographic APIs before being cited, and a reference that does not resolve is
dropped rather than kept with a plausible-looking identifier. When a source lacks data for
a period, the system reports the absence instead of interpolating silently.

## Limitations

- **Coverage.** The substrate is Brazil-centred. Questions about other countries are
  answerable only where an international source covers them.
- **Latency and revision.** Recent periods are provisional, and results computed at
  different dates can differ for legitimate reasons.
- **Non-determinism.** The same request can take different paths and produce differently
  worded answers. The numbers remain traceable, the narrative does not repeat verbatim.
- **Cost.** Complex plans consume time and tokens. The design accepts this in exchange for
  the ability to answer unanticipated questions.
- **Evaluation.** This repository reports use, not accuracy. A formal evaluation against
  benchmark epidemiological questions, with reference answers established by specialists,
  is the natural next step and is not reported here.
- **Outcome evidence.** The usage record shows that sessions happened and what was asked.
  It does not show that each session ended in a completed analysis. Statements about
  usefulness in the manuscript are therefore about process, not about outcome.
