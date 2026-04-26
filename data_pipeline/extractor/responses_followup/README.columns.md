# ECIResponseFollowupRecord columns


Describes the fields extracted from the dedicated EU follow-up websites set up for individual European Citizens' Initiatives — standalone tracking sites the Commission publishes for high-profile cases (e.g., *End the Cage Age*, *Fur Free Europe*) when the initiative warrants ongoing public communication beyond the original response page.


## Column definitions


| Field | Type | Required? | Why mandatory / optional (Logical Intent) |
|---|---|---:|---|
| `registration_number` | `str` | Yes | The unique identifier of the underlying initiative. The follow-up record only exists because that initiative exists, so this value is always carried forward and is the join key linking the follow-up site back to its registered initiative and Commission response. |
| `initiative_url` | `str` | Yes | The canonical public URL of the initiative's own portal page. Required because every follow-up record must remain traceable back to the registered initiative — without this link the follow-up content is orphaned from its origin. |
| `response_url` | `str` | Yes | The URL of the Commission's formal response page for this initiative. Required because a dedicated follow-up website is only ever set up *after* the Commission has issued a response, so the response itself is a precondition for the follow-up record's existence. |
| `followup_url` | `str` | Yes | The URL of the dedicated EU follow-up website that this record summarises. This is the very page the extractor is invoked against — without it there would be nothing to extract — so it is mandatory by definition. |
| `title` | `str` | Yes | Human-readable initiative title carried over from registration. Always present because every registered initiative is required to have a title and the follow-up site exists to track that named initiative. |
| `commission_answer_text` | `Optional[List[str]]` | No | Paragraphs of the Commission's main answer as restated on the follow-up website (typically a brief recap rather than the full response). Optional because some follow-up sites could omit the recap entirely and link straight to the original response, while others include a tailored summary; the field reflects whatever is actually present on the page. |
| `followup_events` | `Optional[List[str]]` | No | Flat list of follow-up action descriptions published on the dedicated site — concrete steps the Commission has taken since responding (consultations, mandates issued to agencies, on-site visits, scientific opinions, draft proposals, etc.). Optional because a freshly-launched follow-up site may not yet list any events, even though the page itself exists; an empty or missing list distinguishes "site published, no actions yet" from "actions actively being added." |


## Expected Structure Notes


`ECIResponseFollowupRecord` is only created for initiatives that have reached a stage beyond a published Commission response — specifically, those where the Commission has set up a dedicated follow-up website to track ongoing actions. This is a small subset of all responded-to initiatives: most ECIs are concluded by the response itself and never receive a standalone tracking site. As a result, the five metadata fields (`registration_number`, `initiative_url`, `response_url`, `followup_url`, `title`) are guaranteed non-null — they are the entry conditions for the record's existence and are carried forward from upstream stages before any HTML parsing of the follow-up site begins.

The two content-extracted fields (`commission_answer_text`, `followup_events`) are typed `Optional` because the layouts of dedicated follow-up websites vary considerably from initiative to initiative — they are bespoke pages curated per topic, not a single templated format. Some sites lead with a Commission recap and follow with a detailed timeline of events; others present only events. The `Optional` typing lets each record reflect possible structure of its source page that serves as starting point.

Both list-typed fields are serialised as Python-list-literal strings in the CSV (e.g., `"['Event A', 'Event B']"`) for flat-file compatibility.