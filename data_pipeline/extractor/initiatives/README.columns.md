# ECIInitiativeDetailsRecord columns

This document describes the fields extracted from the European Citizens' Initiative (ECI) official portal, explaining why certain fields are always present on the HTML page and why others may be missing based on the initiative's lifecycle and legal requirements.

## Column definitions

| Field | Type | Required? | Why mandatory / optional (Based on ECI Rules & Portal HTML) |
|---|---|---:|---|
| `registration_number` | `str` | Yes | Assigned by the EU Commission upon official registration. Every initiative published on the portal legally must have this unique reference (e.g., ECI(2024)000001). |
| `title` | `str` | Yes | Organizers are legally required to provide a title (max 100 characters) when requesting registration. It is permanently displayed on the portal. |
| `objective` | `str` | Yes | Organizers must provide a summary of the subject matter and objectives. The portal always renders this core text on the initiative's page. |
| `annex` | `Optional[str]` | No | Organizers *may* choose to attach an annex providing more detailed background or a draft legal act, but it is not legally required. If they don't submit one, the HTML section is simply absent. |
| `current_status` | `str` | Yes | The portal always displays the current lifecycle phase (e.g., "Collecting", "Closed", "Answered") to inform citizens of its legal standing. |
| `initiative_url` | `str` | Yes | The EU portal generates a dedicated public webpage for every successfully registered initiative. |
| `timeline_registered` | `str` | Yes | This is the official date the Commission registered the initiative. It is the starting point of the legal process and is always published in the portal's timeline. |
| `timeline_collection_start_date` | `Optional[str]` | No | Organizers have up to 6 months after registration to choose their collection start date. A newly registered initiative may not have selected or published this date yet. |
| `timeline_collection_closed` | `Optional[str]` | No | The collection period lasts 12 months. If the initiative is still actively collecting signatures, the official closing date may not be reached or confirmed in the HTML timeline yet. |
| `timeline_verification_start` | `Optional[str]` | No | National authorities only verify signatures *if* the organizers successfully submit them. Most initiatives fail to reach the 1 million target and never trigger this legal phase, meaning it never appears on their page. |
| `timeline_verification_end` | `Optional[str]` | No | Member states have 3 months to complete verification. This date only appears in the HTML after the verification phase concludes. |
| `timeline_response_commission_date` | `Optional[str]` | No | The European Commission only issues a formal response if the initiative successfully passes verification. Very few initiatives reach this final stage. |
| `timeline` | `str` | Yes | The official HTML portal always renders a visual timeline block for every initiative, even if it only contains the "Registered" milestone. |
| `funding_total` | `Optional[str]` | No | Organizers are legally required to declare financial support. However, if they have €0 in external funding, or are newly registered and haven't updated their financial disclosures, the portal may omit this data. |
| `funding_by` | `Optional[str]` | No | Follows the same rules as `funding_total`. If no sponsors gave over the reporting threshold (typically €500), no specific donors will be listed in the HTML. |
| `signatures_collected` | `Optional[str]` | No | The portal displays this based on the Central Online Collection System. Newly registered initiatives will have no data. Older initiatives might lack this if they used private collection systems or if final verified numbers haven't been published yet. |
| `signatures_collected_by_country` | `Optional[str]` | No | The HTML map/table showing the breakdown by member state is only populated when active collection data is available or after final verification is published. |
| `signatures_countries_threshold_met_count` | `Optional[str]` | No | An initiative must reach a minimum threshold of signatures in at least 7 member states. The portal only confirms this status after national authorities complete the official verification phase. |
| `response_url` | `Optional[str]` | No | This link is only added to the HTML if the initiative succeeds and the Commission publishes its official legal communication in response. |

## Expected Structure Notes

Because ECI portal pages evolve as an initiative moves through its lifecycle, the scraper handles optional fields gracefully. Fields marked `Optional[str]` will map to `None` in the Pydantic model if the corresponding HTML block or data point does not yet exist for that specific initiative.
