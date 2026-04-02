# ECIResponseRecord columns


Describes the fields extracted from the European Citizens' Initiative (ECI) official portal's Commission response pages, explaining why certain fields are always present and why others may be absent depending on whether a dedicated follow-up was published.


## Column definitions


| Field | Type | Required? | Why mandatory / optional (Based on ECI Rules & Portal HTML) |
|---|---|---:|---|
| `registration_number` | `str` | Yes | Copied directly from the initiatives CSV. Every ECI response page is scraped only for initiatives that have already been registered and formally answered — this identifier always exists upstream. |
| `initiative_url` | `str` | Yes | The canonical public URL of the initiative's own portal page (e.g., `https://citizens-initiative.europa.eu/initiatives/details/2020/000001_en`). Copied from the `url` field of the initiatives CSV; it is always present for any registered initiative. |
| `response_url` | `str` | Yes | The URL of the Commission's formal response page scraped for this record. Copied from `response_commission_url` in the initiatives CSV. This field is the very reason the response extractor is invoked — only initiatives that have a published response URL are processed. |
| `title` | `str` | Yes | Human-readable initiative title copied from the initiatives CSV. Organizers must submit a title (max 100 characters) at registration time, so it is always available. |
| `commission_answer_text` | `Optional[List[str]]` | No | Paragraphs of the Commission's main answer extracted from the *"Answer of the European Commission"* HTML section. Each list item represents one paragraph or bullet group. Declared optional to handle the significant variation in page layouts observed across scrape years (2012–2024) and to fail gracefully on unexpected HTML structures, even though a validly scraped response page will always contain this section. |
| `followup_additional_website` | `Optional[str]` | No | URL of a dedicated EU follow-up website for the initiative (matched against the pattern `https://…/eci/eci-{identifier}_en`). Present only when the Commission has set up a standalone tracking site for a specific initiative (e.g., `https://food.ec.europa.eu/animals/animal-welfare/eci/eci-end-cage-age_en`). The vast majority of responses do not include such a site, so this field is `None` for most records. |
| `followup_events` | `Optional[List[str]]` | No | Flat list of follow-up action descriptions (plain text with embedded Markdown links) extracted from the *"Follow-up"* or *"Updates on the Commission's proposals"* HTML section. `None` when no follow-up section is present on the page — common for older or simpler responses that contain only the Commission's answer with no subsequent legislative events. **Serialized as a JSON string in the CSV** (e.g., `["Event A [https://…](https://…)", "Event B"]`) for flat-file compatibility; consumers should recover the list with `json.loads()`. |


## Expected Structure Notes


`ECIResponseRecord` is only created for initiatives that have already reached the final lifecycle stage — a published Commission response. As a result, all four metadata fields (`registration_number`, `initiative_url`, `response_url`, `title`) are guaranteed non-null: they are copied upstream from the initiatives CSV before any HTML parsing begins.

The three HTML-extracted fields (`commission_answer_text`, `followup_additional_website`, `followup_events`) are typed `Optional` because the response page HTML has evolved significantly across scrape years (2012–2024). Legacy pages may omit follow-up sections entirely, while modern ECL-wrapped pages consistently provide them. Fields marked `Optional[List[str]]` will map to `None` in the Pydantic model when the corresponding HTML block is absent for that initiative.