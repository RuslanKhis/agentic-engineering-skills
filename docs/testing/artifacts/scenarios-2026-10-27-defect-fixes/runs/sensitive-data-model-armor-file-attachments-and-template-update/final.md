I wrote the code and tests, but none of the tests have been run. This session has no shell, so the new and existing tests are all unrun. I also couldn't check anything against ADK 2.12 or google-cloud-modelarmor 0.7.1, because neither is installed.

## What changed
- **Attachment screening:** every PDF and Word file is screened against `claims-input` before the model sees it, and any non-`ALLOW` verdict withholds the whole turn.
  - **Screened twice:** once in `chat` before the message is built (`server.py`). Once in `before_model_callback` across the whole request, so files replayed from history are also checked (`agent.py`).
  - **Type check:** a file's type is decided from its leading bytes, not the declared MIME type. A Word file must contain `word/document.xml`, so Excel and PowerPoint zips are refused.
  - **Stricter verdict:** `screen_file` in `claims_agent/screening.py` needs `NO_MATCH_FOUND`, a successful invocation result, and results from all four filters. Anything else withholds the file. Allowed files are cached by hash, and the call has a timeout.
- **Multi-language detection:**
  - `input-template.json` has one line flipped to `true`.
  - `scripts/apply_template.py` now sends an update mask for that single field. Without a mask the update would have overwritten the whole template.
  - The script also sends a deterministic `request_id`, reads the result back, and has a `--dry-run` option.
  - It now parses the JSON with `Template.from_json`, because I believe the old `Template(spec)` would have rejected camelCase keys. That is from memory of proto-plus, not checked.
- **Tests:** `tests/test_attachment_screening.py` and `tests/test_apply_template.py` use doubles and make no network calls. I extended `tests/armor_double.py`. I changed the existing PDF test to use a realistic size, since a 12-byte "PDF" is now rightly refused.

## Behaviour changes you should know about
- **Photos are now refused at upload.** The template has no image modality, so an image can't be screened, and I took "screen every attachment" literally. This breaks the existing photo upload. Allowing photos needs a template change, which you didn't ask for.
- **Documents over 4 MB are refused at upload.** Model Armor file screening takes 69 bytes to 4 MB, so the 10 MB limit no longer applies to PDFs and Word files. I didn't split or extract files, since that would change what gets screened.

## Assumptions (questions nobody was here to answer)
- Is refusing photos acceptable, or should the template get an image modality?
- Should the 4 MB document cap stand, or does the product need 10 MB? That would need a separate extraction route.
- Should a blocked file withhold the customer's text too? I assumed yes.
- Should a template change evict the cache of allowed files? I assumed no; it is process-local.

## Not done
- **Not run:** all tests. Command to run them: `python -m unittest discover -s tests -t .`.
- **No ADK runner test:** `agent.py` and `server.py` wiring has not been run. The screening logic they call is framework-free and covered by the new tests.
- **Live canary (release gate):** `README.md` in `infra/modelarmor/` describes it. It would send a synthetic PDF and DOCX that carry a sensitive-data finding and expect `MATCH_FOUND`. It settles three open points:
  - `MODEL_ARMOR_BYTE_ENCODING`, raw (my default) or base64. A wrong choice reads as a silent allow.
  - Whether file results report all four filter keys.
  - Whether multi-language detection applies to text extracted from files.
- **SDK names unchecked:** `ByteDataItem.ByteItemType` and `InvocationResult` are written from documentation, not from the installed SDK.
- **Template update not applied:** if it's refused, stop and ask Platform Security whether the floor setting conflicts. I touched no floor setting and made no cloud calls.