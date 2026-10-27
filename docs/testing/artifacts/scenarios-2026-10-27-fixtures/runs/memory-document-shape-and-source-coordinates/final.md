Yes, you're both cutting up and losing parts of the documents, and almost all of it happens in `review_app/grouping.py`. The extract itself looks intact: 52 records, matching its manifest. I couldn't check the extract against the PDFs, which aren't available.

Bash was disabled in this session, so I couldn't execute anything. I traced the saved envelopes by hand against the grouper code. The audit script I wrote (`analysis/audit_run.py`) hasn't been run, and neither have the unit tests.

**What goes wrong in the grouper**
- **Clause collisions:** units are keyed by label only, so 4.2(a) and 4.3(a) merge into one `DMP:(a)`, and likewise for (b). That is the reviewer's "two provisions" complaint.
- **Misplaced continuation:** a continuation is attached to whichever unit came just before it in the pack, not to the record it continues. The Conservation Area tail of 4.2(b), 2.5 m, landed on `DMP:(a)`, so `DMP:(b)` ends at "except where".
- **Table cells dropped:** cells are de-duplicated by their text alone, which removed 7 of 26 cells, including the 30 m2 footprint for the 500–800 row. Row and column positions are never rendered.
- **Fixed-width splitting:** units are cut every 160 characters, mid-word and mid-number (`eave|s`, `35|0`). Every part carries the whole unit's record IDs and pages, so no part traces back to its record.
- **Silent skips:** footnote 7 is dropped without a trace, and so is the unreviewed page-18 map image.

**Retrieval**
- The pack held 35 IDs although top_k is 40. It never included r007, r010, r011 or any of page 17, which holds the table continuation and its notes.
- The 800–1200 m² row, which applies to the 900 m² plot, therefore never reached the writer.

**Effect on this run's answer**
From the extract records, and unconfirmed against the PDF, the writer's two substantive findings look wrong.
- **Eaves:** the site is in a Conservation Area, where the limit is 2.5 m, and the proposal is 2.9 m. The writer said it was within 3 m.
- **Outbuilding:** the 900 m² plot's limit is 40 m², so 36 m² probably complies. The writer used 30 m². Whether note a applies can't be answered from the question.

The reviewer was right to reject the draft, and I didn't treat these corrections as a pass.

**Rules held**
- No model calls, network access, installs or app-code changes.
- The page-18 Inset 3 map stays unresolved, not assumed.
- Where I assumed something, it is written down in `analysis/FINDINGS.md`.

**Questions I couldn't ask, and the assumptions I used**
- Is `MAX_UNIT_CHARS = 160` a real writer budget? I assumed it's unknown. Storage has no size limit, so storage isn't a reason to split.
- Is 35 results with top_k=40 deliberate? I assumed it's unexplained.

**Left undone**
- No fixes. The remedies are in `analysis/FINDINGS.md`: key units by clause path, resolve continuations by record ID, remove the cell de-dup, split at record boundaries, surface skipped footnotes and images, and add a coverage check. A test is listed for each.
- No tests run, and no verification against the PDFs.
- Retrieval needs a separate look, covering why 35 came back and expanding hits to a table's continuation and footnotes.