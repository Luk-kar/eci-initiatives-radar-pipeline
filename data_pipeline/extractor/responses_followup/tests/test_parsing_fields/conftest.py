"""
HTML fixtures covering the full lifespan of ECI response pages on the EU
Commission website.  The schema has changed substantially over the years —
from bare HTML fragments to ECL-wrapped, component-driven layouts — and
individual pages may reflect different snapshots of the site at the time
they were scraped, so no single structural assumption holds universally.
Parsers must treat every field as optional and handle legacy patterns
alongside current ones without breaking.
"""

import pytest

from bs4 import BeautifulSoup

# Two layout variants are represented: a modern ECL container layout where each section
# lives in its own div.ecl-u-mb-2xl (exercises _walk_wrapper_children), and a flat legacy
# layout where the h2 and its content are direct siblings (exercises _walk_next_siblings).
# In both variants the "Follow-up on the Commission's actions:" h3 acts as a boundary —
# commission_answer.py stops there, while followup_details.py continues past it.

_ECI_HTML = [
    (
        "2012_000001",  # Fake one, used as fallback example
        """
<div class="ecl-col-l-9">

  <h2 id="about-this-initiative">About this initiative</h2>
  <p>The Right2Water ECI called on the European institutions to implement the human right
  to water and sanitation as recognised by the United Nations, and to promote the provision
  of water and sanitation as essential public services for all.</p>

  <h2 id="response-of-the-commission">Response of the Commission</h2>
  <p>On 19 March 2014, the Commission adopted a
  <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52014DC0177">Communication</a>
  responding positively to the ECI and committing to strengthen EU water policy.</p>

  <h2 id="next-steps">Next steps</h2>
  <p>The Commission will continue monitoring the implementation of the revised
  <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32020L2184">
  Drinking Water Directive</a>, adopted on 16 December 2020.</p>

  <h2 id="related-links">Related links</h2>
  <ul>
    <li><a href="https://environment.ec.europa.eu/topics/water_en">EU water policy</a></li>
    <li><a href="https://citizens-initiative.europa.eu/initiatives/details/2012/000001_en">
    Initiative details page</a></li>
  </ul>

</div>
""",
    ),
    (
        "2018_000004",
        """
<div class="ecl-col-l-9" data-inpage-navigation-source-area="h2, div.ecl-featured-item__heading">

  <div class="ecl-u-mb-2xl">
    <a id="paragraph_433"></a>
    <div>
      <div class="ecl">
        <h2 class="ecl-u-type-heading-2" id="about-this-initiative">About this initiative</h2>
      </div>
      <div class="ecl">
        <p>The ECI 'End the Cage Age' calls on the Commission to propose legislation to
        prohibit the use of cages for EU farmed animals.</p>
        <ul>
          <li>laying hens, rabbits, pullets and broiler breeders;</li>
          <li>farrowing crates for sows;</li>
          <li>individual calf pens, where not already prohibited.</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="ecl-u-mb-2xl">
    <a id="paragraph_434"></a>
    <div>
      <div class="ecl">
        <h2 class="ecl-u-type-heading-2" id="response-of-the-commission">
          Response of the Commission
        </h2>
      </div>
      <!-- Main response text — collected by commission_answer.py -->
      <div class="ecl">
        <p>
          On 30 June 2021, the Commission decided to positively respond to the ECI.
          <a href="https://ec.europa.eu/transparency/documents-register/detail?ref=C(2021)4747&amp;lang=en">In its communication</a>
          the Commission sets out plans for a legislative proposal to prohibit cages
          for the species and categories of animals covered by the ECI.
        </p>
        <p>
          Scientific opinions were commissioned from
          <a class="ecl-link ecl-link--icon" href="https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2022.7421">
            <span class="ecl-link__label">EFSA</span>
          </a>
          on the welfare of pigs, broilers, laying hens, ducks, geese, quail and calves.
        </p>
      </div>
      <!-- Follow-up block — h3 stops commission_answer.py; consumed by followup_details.py -->
      <div class="ecl">
        <h3>Follow-up on the Commission's actions:</h3>
        <ul>
          <li>In 2022 the Commission launched stakeholder consultations on poultry, ruminants and pigs.</li>
          <li>EFSA adopted scientific opinions on pigs (2022), laying hens (2022) and calves (2023).</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="ecl-u-mb-2xl">
    <a id="paragraph_435"></a>
    <div>
      <div class="ecl">
        <h2 class="ecl-u-type-heading-2" id="next-steps">Next steps</h2>
      </div>
      <div class="ecl">
        <p>
          The Commission will present proposals on the revision of EU animal welfare
          legislation, including its commitment to phase out cages, based on the
          <a href="https://agriculture.ec.europa.eu/vision-agriculture-food_en">Vision for Agriculture and Food</a>
          adopted on 19 February 2025.
        </p>
      </div>
    </div>
  </div>

  <div class="ecl-u-mb-2xl">
    <a id="paragraph_436"></a>
    <div>
      <div class="ecl">
        <h2 class="ecl-u-type-heading-2" id="supporting-measures">Supporting measures</h2>
      </div>
      <div class="ecl">
        <p>
          Materials from the pilot project "Best Practice Hens" (2021–2023) are published on a
          <a class="ecl-link ecl-link--icon" href="https://bestpracticehens.eu/materials/">
            <span class="ecl-link__label">dedicated website</span>
          </a>.
        </p>
      </div>
    </div>
  </div>

  <div class="ecl-u-mb-2xl">
    <a id="paragraph_2217"></a>
    <div>
      <div class="ecl">
        <h2 class="ecl-u-type-heading-2" id="press-release">Press release</h2>
      </div>
      <div class="ecl">
        <p>
          Please see the
          <a href="https://ec.europa.eu/commission/presscorner/detail/en/ip_21_3297">press release</a>
          from 30 June 2021.
        </p>
      </div>
    </div>
  </div>

  <div>
    <a id="paragraph_438"></a>
    <div>
      <div class="ecl">
        <h2 class="ecl-u-type-heading-2" id="video">Video</h2>
      </div>
      <div class="ecl">
        <p>
          On the occasion of the adoption of its communication, the Commission has
          <a class="ecl-link ecl-link--icon" href="https://vimeo.com/567105378/79af612ef3">
            <span class="ecl-link__label">released a video</span>
          </a>.
        </p>
      </div>
    </div>
  </div>

  <div class="ecl-u-mb-2xl">
    <a id="paragraph_439"></a>
    <div>
      <div class="ecl">
        <h2 class="ecl-u-type-heading-2" id="related-links">Related links</h2>
      </div>
      <div class="ecl">
        <ul>
          <li>
            <a class="ecl-link ecl-link--icon" href="https://food.ec.europa.eu/animals/animal-welfare_en">
              <span class="ecl-link__label">EU animal welfare policy</span>
            </a>
          </li>
          <li>
            <a class="ecl-link ecl-link--icon" href="https://citizens.ec.europa.eu/initiatives/details/2018/000004_en">
              <span class="ecl-link__label">Initiative details page</span>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>

</div>
""",
    ),
    (
        "2022_000002",
        """
<div class="ecl-col-l-9" data-inpage-navigation-source-area="h2, div.ecl-featured-item__heading">

  <div class="ecl-u-mb-2xl">
    <a id="paragraph_1887"></a>
    <div>
      <div class="ecl">
        <h2 class="ecl-u-type-heading-2" id="about-this-initiative">About this initiative</h2>
      </div>
      <div class="ecl">
        <p>In March 2022, the European Commission registered the European Citizens Initiative
        entitled Fur Free Europe. The organisers invited the Commission to prohibit by law,
        throughout the Union, the keeping and killing of animals for the sole or main purpose
        of fur production.</p>
      </div>
    </div>
  </div>

  <div class="ecl-u-mb-2xl">
    <a id="paragraph_1919"></a>
    <div>
      <div class="ecl">
        <h2 class="ecl-u-type-heading-2" id="response-of-the-commission">Response of the Commission</h2>
      </div>
      <div class="ecl">
        <p>The Commission published the response to this initiative on 7 December 2023 in the
        form of a
        <a href="https://citizens-initiative.europa.eu/initiatives/details/2022/000002/en">Communication</a>,
        setting out the Commission's legal and political conclusions on the initiative and the
        actions it intended to take as a response.</p>
      </div>
    </div>
  </div>

  <div class="ecl-u-mb-2xl">
    <a id="paragraph_1920"></a>
    <div>
      <div class="ecl">
        <h2 class="ecl-u-type-heading-2" id="follow-up-on-the-commissions-actions">
          Follow-up on the Commission's actions
        </h2>
      </div>
      <div class="ecl">
        <ul>
          <li>The Commission conducted, in 2024, three on-site visits to Member States with
          mink/fur farms, exploring the controls and the One Health mechanisms in place.</li>
          <li>A survey on fur animals directed at Member States authorities was carried out
          end of 2024 to collect factual information and data for a Commission impact
          assessment.</li>
          <li>Through an
          <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32025R1422">
          Implementing Regulation adopted on 17 July 2025</a>, American mink
          <em>Neovison vison</em> is now listed under the Invasive Alien Species Regulation,
          entering into force in August 2027.</li>
          <li>On 4 July 2025, the Commission launched a
          <a href="https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14669-The-Fur-Free-Europe-initiative-assessment_en">
          Call for evidence</a> requesting input from stakeholders and citizens on the
          follow-up to the ECI Fur Free Europe.</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="ecl-u-mb-2xl">
    <a id="paragraph_1922"></a>
    <div>
      <div class="ecl">
        <h2 class="ecl-u-type-heading-2" id="related-links">Related links</h2>
      </div>
      <div class="ecl">
        <ul>
          <li>
            <a href="https://citizens-initiative.europa.eu/fur-free-europe_en">
              European Citizens initiative portal
            </a>
          </li>
          <li>
            <a href="https://ec.europa.eu/commission/presscorner/detail/en/ip_22_1753">
              Fur Free Europe Citizens Initiative on banning fur
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>

</div>
""",
    ),
]


ECI_FIXTURES = [
    (reg_num, BeautifulSoup(html, "html.parser")) for reg_num, html in _ECI_HTML
]


@pytest.fixture
def eci_fixture_soup():
    index = {reg_num: soup for reg_num, soup in ECI_FIXTURES}

    def _get(registration_number: str) -> BeautifulSoup:
        if registration_number not in index:
            raise KeyError(f"No fixture for {registration_number!r}")
        return index[registration_number]

    return _get
