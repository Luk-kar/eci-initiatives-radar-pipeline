"""
HTML fixtures covering the full lifespan of ECI response pages on the EU
Commission website. The schema has changed substantially over the years —
from bare HTML fragments to ECL-wrapped, component-driven layouts — and
individual pages may reflect different snapshots of the site at the time
they were scraped, so no single structural assumption holds universally.
Parsers must treat every field as optional and handle legacy patterns
alongside current ones without breaking.
"""

import pytest

from bs4 import BeautifulSoup


_ECI_HTML = [
    (
        "2018_000004",
        """
<div class="ecl-col-l-9" data-inpage-navigation-source-area="h2, div.ecl-featured-item__heading">
             <div class="ecl-u-mb-2xl">
              <a id="paragraph_433">
              </a>
              <div>
               <div class="ecl">
                <h2 class="ecl-u-type-heading-2" id="about-this-initiative">
                 About this initiative
                </h2>
               </div>
               <div class="ecl">
                <p>
                 The European Citizens' Initiative (ECI) 'End the Cage Age' calls on the Commission to propose legislation to prohibit the use of cages for EU farmed animals for:
                </p>
                <ul type="disc">
                 <li>
                  laying hens, rabbits, pullets, broiler breeders, layer breeders, quail, ducks and geese;
                 </li>
                 <li>
                  farrowing crates for sows;
                 </li>
                 <li>
                  sow stalls, where not already prohibited;
                 </li>
                 <li>
                  individual calf pens, where not already prohibited.
                 </li>
                </ul>
                <p>
                 Within one year, the organisers of the ECI, with the support of more than 170 non-governmental organisations across Europe, collected 1.4 million signatures from supporters throughout the EU.
                </p>
                <p>
                 Detailed information on this ECI is available on the
                 <a class="ecl-link ecl-link--icon" href="https://www.endthecageage.eu/">
                  <span class="ecl-link__label">
                   website of the organisers
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 and on the dedicated
                 <a href="https://europa.eu/citizens-initiative/initiatives/details/2018/000004_en">
                  Commission's 'End the Cage Age' webpage
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 .
                </p>
               </div>
              </div>
             </div>
             <div class="ecl-u-mb-2xl">
              <a id="paragraph_434">
              </a>
              <div>
               <div class="ecl">
                <h2 class="ecl-u-type-heading-2" id="response-of-the-commission">
                 Response of the Commission
                </h2>
               </div>
               <div class="ecl">
                <p>
                 On 30 June 2021, the Commission decided to positively respond to the ECI.
                 <a href="https://ec.europa.eu/transparency/documents-register/detail?ref=C(2021)4747&amp;lang=en">
                  In its communication
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 the Commission sets out plans for a legislative proposal to prohibit cages for the species and categories of animals covered by the ECI and to consider options for introducing rules or standards for imported products that are equivalent to the EU’s and/or a labelling requirement, in compliance with WTO rules. The Commission will also pursue or implement specific supporting measures in key related policy areas.
                </p>
                <p>
                 The Commission has asked the European Food Safety Authority (EFSA) to complement the existing scientific evidence to determine the conditions needed for the prohibition of the use of cages. Scientific opinions were adopted by EFSA on the welfare on farm
                 <a class="ecl-link ecl-link--icon" href="https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2022.7421">
                  <span class="ecl-link__label">
                   of pigs
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 (2022),
                 <a class="ecl-link ecl-link--icon" href="https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7788">
                  <span class="ecl-link__label">
                   broilers,
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 addressing also broiler breeders (2022),
                 <a class="ecl-link ecl-link--icon" href="https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7789">
                  <span class="ecl-link__label">
                   laying hens
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 , addressing also layer breeders and pullets (2022),
                 <a class="ecl-link ecl-link--icon" href="https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7992">
                  <span class="ecl-link__label">
                   ducks, geese and quail
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 (2023) and of
                 <a class="ecl-link ecl-link--icon" href="https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7896">
                  <span class="ecl-link__label">
                   calves
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 (2023). The Commission also has started a series of stakeholder consultations in 2022, including in the context of subgroups of the EU Animal Welfare Platform (on poultry, on ruminants and on pigs).
                </p>
                <p>
                 To facilitate a balanced and economically viable transition to cage-free farming, in which the competitiveness of the sectors concerned is further improved, the Commission is pursuing supporting measures in key related policy areas, such as research and innovation. Several research projects such as the
                 <a class="ecl-link ecl-link--icon" href="https://www.eupahw.eu/pdf/projects/priority-%20area-3-green/JIPs_SOA17.pdf">
                  <span class="ecl-link__label">
                   “Sustainability aspects of AW-promoting livestock systems”
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 under
                 <a class="ecl-link ecl-link--icon" href="https://www.eupahw.eu/">
                  <span class="ecl-link__label">
                   the European Partnership on Animal Health and Welfare
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 , may be relevant in this context.
                </p>
                <p>
                 The Common Agricultural Policy (CAP) provides financial support and incentives – such as the new eco-schemes instrument – to help farmers upgrade to more animal-friendly facilities. In its recommendations for the National Strategic Plans under the CAP, the Commission has regularly recommended the Member States to make efforts to promote e.g. the production of eggs under non-cage systems for laying hens.
                </p>
               </div>
              </div>
             </div>
             <div class="ecl-u-mb-2xl">
              <a id="paragraph_435">
              </a>
              <div>
               <div class="ecl">
                <h2 class="ecl-u-type-heading-2" id="next-steps">
                 Next steps
                </h2>
               </div>
               <div class="ecl">
                <p>
                 As established by the
                 <a href="https://agriculture.ec.europa.eu/vision-agriculture-food_en">
                  Vision for Agriculture and Food
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 adopted on 19 February 2025, building on the recommendations of the
                 <a href="https://agriculture.ec.europa.eu/common-agricultural-policy/cap-overview/main-initiatives-strategic-dialogue-future-eu-agriculture_en">
                  Strategic Dialogue on the Future of EU Agriculture
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 , the Commission will closely exchange with farmers, the food chain and civil society. On that basis, the Commission will present proposals on the revision of the existing EU animal welfare legislation, including its commitment to phase out cages. The Commission will also pursue, in line with international rules, a stronger alignment of animal welfare standards applied to imported animals and food.
                </p>
                <p>
                 This revision will be based on the latest scientific evidence and take into account the socio-economic impact on farmers and the agri-food chain, providing support and appropriate, species-specific transition periods and pathways.
                </p>
                <p>
                 Further to the
                 <a href="https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14671-On-farm-animal-welfare-for-certain-animals-modernisation-of-EU-legislation_en">
                  call for evidence
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 launched on 18 June 2025 (and closed on 16 July 2025), the Commission published on 19 September 2025 a
                 <a href="https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14671-On-farm-animal-welfare-for-certain-animals-modernisation-of-EU-legislation/public-consultation_en">
                  public consultation
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 which will run until 12 December 2025. The objective of both initiatives is to seek the views of stakeholders, NGOs and citizens on certain potential policy measures, including on the phasing out of cages, in view of the upcoming
                 <a href="/animals/animal-welfare/evaluations-and-impact-assessment/revision-eu-animal-welfare-legislation_en">
                  revision of the EU legislation for on-farm animal welfare
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 <a href="https://food.ec.europa.eu/animals/animal-welfare/evaluations-and-impact-assessment/revision-eu-animal-welfare-legislation_en">
                  .
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                </p>
                <p>
                 The Commission will continue to develop supporting measures, such as best practices, guidelines, recommendations and studies, for the promotion of and the transition to non-cage farming. In addition, the Commission will further consider which role animal welfare labelling and public procurement might play in this context.
                </p>
               </div>
              </div>
             </div>
             <div class="ecl-u-mb-2xl">
              <a id="paragraph_436">
              </a>
              <div>
               <div class="ecl">
                <h2 class="ecl-u-type-heading-2" id="supporting-measures">
                 Supporting measures
                </h2>
               </div>
               <div class="ecl">
                <p>
                 A pilot project “Best Practice Hens” implemented from 2021 to 2023, aimed to help egg producers meet market demand by providing practical guidance on how to transition to alternative, higher-welfare cage-free systems. Materials developed under this project are published on a
                 <a class="ecl-link ecl-link--icon" href="https://bestpracticehens.eu/materials/">
                  <span class="ecl-link__label">
                   dedicated website
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 .
                </p>
               </div>
              </div>
             </div>
             <div class="ecl-u-mb-2xl">
              <a id="paragraph_2217">
              </a>
              <div>
               <div class="ecl">
                <h2 class="ecl-u-type-heading-2" id="press-release">
                 Press release
                </h2>
               </div>
               <div class="ecl">
                <p>
                 Please see the
                 <a href="https://ec.europa.eu/commission/presscorner/detail/en/ip_21_3297">
                  press release
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 from 30 June 2021.
                </p>
               </div>
              </div>
             </div>
             <div>
              <a id="paragraph_438">
              </a>
              <div>
               <div class="ecl">
                <h2 class="ecl-u-type-heading-2" id="video">
                 Video
                </h2>
               </div>
               <div class="ecl">
                <p>
                 On the occasion of the adoption of its communication on ‘End the Cage Age’, the Commission has
                 <a class="ecl-link ecl-link--icon" href="https://vimeo.com/567105378/79af612ef3">
                  <span class="ecl-link__label">
                   released a video
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 .
                </p>
               </div>
              </div>
             </div>
            </div>
""",
    ),
    (
        "2022_000002",
        """
<div class="ecl-row inpage-navigation-container">
            <div class="ecl-col-l-3">
             <nav aria-labelledby="ecl-inpage-navigation-357178478" class="ecl-inpage-navigation oe-theme-ecl-inpage-navigation ecl-u-z-dropdown" data-ecl-auto-init="InpageNavigation" data-ecl-auto-initialized="true" data-ecl-inpage-navigation="true">
              <div class="ecl-inpage-navigation__title" id="ecl-inpage-navigation-357178478">
               Page contents
              </div>
              <div class="ecl-inpage-navigation__body">
               <div class="ecl-inpage-navigation__trigger-wrapper">
                <button aria-controls="ecl-inpage-navigation-list" aria-expanded="false" class="ecl-inpage-navigation__trigger" data-ecl-inpage-navigation-trigger="true" id="ecl-inpage-navigation-357178478-trigger" type="button">
                 <span class="ecl-inpage-navigation__trigger-current" data-ecl-inpage-navigation-trigger-current="true">
                  Page contents
                 </span>
                 <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-icon--rotate-180 ecl-inpage-navigation__trigger-icon ecl-icon--corner-arrow" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                  <path d="m45 30.12-2.73 2.82-18.24-18.36L5.73 33 3 30.18 24.03 9z">
                  </path>
                 </svg>
                </button>
               </div>
               <ul class="ecl-inpage-navigation__list" data-ecl-inpage-navigation-list="true" id="ecl-inpage-navigation-357178478-list" style="max-height: 443px;">
                <li class="ecl-inpage-navigation__item">
                 <a class="ecl-link ecl-link--standalone ecl-inpage-navigation__link" data-ecl-inpage-navigation-link="" href="#about-this-initiative">
                  About this initiative
                 </a>
                </li>
                <li class="ecl-inpage-navigation__item">
                 <a class="ecl-link ecl-link--standalone ecl-inpage-navigation__link" data-ecl-inpage-navigation-link="" href="#response-of-the-commission">
                  Response of the Commission
                 </a>
                </li>
                <li class="ecl-inpage-navigation__item">
                 <a class="ecl-link ecl-link--standalone ecl-inpage-navigation__link" data-ecl-inpage-navigation-link="" href="#next-steps">
                  Next steps
                 </a>
                </li>
                <li class="ecl-inpage-navigation__item">
                 <a class="ecl-link ecl-link--standalone ecl-inpage-navigation__link" data-ecl-inpage-navigation-link="" href="#supporting-measures">
                  Supporting measures
                 </a>
                </li>
                <li class="ecl-inpage-navigation__item">
                 <a class="ecl-link ecl-link--standalone ecl-inpage-navigation__link" data-ecl-inpage-navigation-link="" href="#press-release">
                  Press release
                 </a>
                </li>
                <li class="ecl-inpage-navigation__item">
                 <a class="ecl-link ecl-link--standalone ecl-inpage-navigation__link" data-ecl-inpage-navigation-link="" href="#video">
                  Video
                 </a>
                </li>
               </ul>
              </div>
             </nav>
            </div>
            <div class="ecl-col-l-9" data-inpage-navigation-source-area="h2, div.ecl-featured-item__heading">
             <div class="ecl-u-mb-2xl">
              <a id="paragraph_433">
              </a>
              <div>
               <div class="ecl">
                <h2 class="ecl-u-type-heading-2" id="about-this-initiative">
                 About this initiative
                </h2>
               </div>
               <div class="ecl">
                <p>
                 The European Citizens' Initiative (ECI) 'End the Cage Age' calls on the Commission to propose legislation to prohibit the use of cages for EU farmed animals for:
                </p>
                <ul type="disc">
                 <li>
                  laying hens, rabbits, pullets, broiler breeders, layer breeders, quail, ducks and geese;
                 </li>
                 <li>
                  farrowing crates for sows;
                 </li>
                 <li>
                  sow stalls, where not already prohibited;
                 </li>
                 <li>
                  individual calf pens, where not already prohibited.
                 </li>
                </ul>
                <p>
                 Within one year, the organisers of the ECI, with the support of more than 170 non-governmental organisations across Europe, collected 1.4 million signatures from supporters throughout the EU.
                </p>
                <p>
                 Detailed information on this ECI is available on the
                 <a class="ecl-link ecl-link--icon" href="https://www.endthecageage.eu/">
                  <span class="ecl-link__label">
                   website of the organisers
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 and on the dedicated
                 <a href="https://europa.eu/citizens-initiative/initiatives/details/2018/000004_en">
                  Commission's 'End the Cage Age' webpage
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 .
                </p>
               </div>
              </div>
             </div>
             <div class="ecl-u-mb-2xl">
              <a id="paragraph_434">
              </a>
              <div>
               <div class="ecl">
                <h2 class="ecl-u-type-heading-2" id="response-of-the-commission">
                 Response of the Commission
                </h2>
               </div>
               <div class="ecl">
                <p>
                 On 30 June 2021, the Commission decided to positively respond to the ECI.
                 <a href="https://ec.europa.eu/transparency/documents-register/detail?ref=C(2021)4747&amp;lang=en">
                  In its communication
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 the Commission sets out plans for a legislative proposal to prohibit cages for the species and categories of animals covered by the ECI and to consider options for introducing rules or standards for imported products that are equivalent to the EU’s and/or a labelling requirement, in compliance with WTO rules. The Commission will also pursue or implement specific supporting measures in key related policy areas.
                </p>
                <p>
                 The Commission has asked the European Food Safety Authority (EFSA) to complement the existing scientific evidence to determine the conditions needed for the prohibition of the use of cages. Scientific opinions were adopted by EFSA on the welfare on farm
                 <a class="ecl-link ecl-link--icon" href="https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2022.7421">
                  <span class="ecl-link__label">
                   of pigs
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 (2022),
                 <a class="ecl-link ecl-link--icon" href="https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7788">
                  <span class="ecl-link__label">
                   broilers,
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 addressing also broiler breeders (2022),
                 <a class="ecl-link ecl-link--icon" href="https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7789">
                  <span class="ecl-link__label">
                   laying hens
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 , addressing also layer breeders and pullets (2022),
                 <a class="ecl-link ecl-link--icon" href="https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7992">
                  <span class="ecl-link__label">
                   ducks, geese and quail
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 (2023) and of
                 <a class="ecl-link ecl-link--icon" href="https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7896">
                  <span class="ecl-link__label">
                   calves
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 (2023). The Commission also has started a series of stakeholder consultations in 2022, including in the context of subgroups of the EU Animal Welfare Platform (on poultry, on ruminants and on pigs).
                </p>
                <p>
                 To facilitate a balanced and economically viable transition to cage-free farming, in which the competitiveness of the sectors concerned is further improved, the Commission is pursuing supporting measures in key related policy areas, such as research and innovation. Several research projects such as the
                 <a class="ecl-link ecl-link--icon" href="https://www.eupahw.eu/pdf/projects/priority-%20area-3-green/JIPs_SOA17.pdf">
                  <span class="ecl-link__label">
                   “Sustainability aspects of AW-promoting livestock systems”
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 under
                 <a class="ecl-link ecl-link--icon" href="https://www.eupahw.eu/">
                  <span class="ecl-link__label">
                   the European Partnership on Animal Health and Welfare
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 , may be relevant in this context.
                </p>
                <p>
                 The Common Agricultural Policy (CAP) provides financial support and incentives – such as the new eco-schemes instrument – to help farmers upgrade to more animal-friendly facilities. In its recommendations for the National Strategic Plans under the CAP, the Commission has regularly recommended the Member States to make efforts to promote e.g. the production of eggs under non-cage systems for laying hens.
                </p>
               </div>
              </div>
             </div>
             <div class="ecl-u-mb-2xl">
              <a id="paragraph_435">
              </a>
              <div>
               <div class="ecl">
                <h2 class="ecl-u-type-heading-2" id="next-steps">
                 Next steps
                </h2>
               </div>
               <div class="ecl">
                <p>
                 As established by the
                 <a href="https://agriculture.ec.europa.eu/vision-agriculture-food_en">
                  Vision for Agriculture and Food
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 adopted on 19 February 2025, building on the recommendations of the
                 <a href="https://agriculture.ec.europa.eu/common-agricultural-policy/cap-overview/main-initiatives-strategic-dialogue-future-eu-agriculture_en">
                  Strategic Dialogue on the Future of EU Agriculture
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 , the Commission will closely exchange with farmers, the food chain and civil society. On that basis, the Commission will present proposals on the revision of the existing EU animal welfare legislation, including its commitment to phase out cages. The Commission will also pursue, in line with international rules, a stronger alignment of animal welfare standards applied to imported animals and food.
                </p>
                <p>
                 This revision will be based on the latest scientific evidence and take into account the socio-economic impact on farmers and the agri-food chain, providing support and appropriate, species-specific transition periods and pathways.
                </p>
                <p>
                 Further to the
                 <a href="https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14671-On-farm-animal-welfare-for-certain-animals-modernisation-of-EU-legislation_en">
                  call for evidence
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 launched on 18 June 2025 (and closed on 16 July 2025), the Commission published on 19 September 2025 a
                 <a href="https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14671-On-farm-animal-welfare-for-certain-animals-modernisation-of-EU-legislation/public-consultation_en">
                  public consultation
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 which will run until 12 December 2025. The objective of both initiatives is to seek the views of stakeholders, NGOs and citizens on certain potential policy measures, including on the phasing out of cages, in view of the upcoming
                 <a href="/animals/animal-welfare/evaluations-and-impact-assessment/revision-eu-animal-welfare-legislation_en">
                  revision of the EU legislation for on-farm animal welfare
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 <a href="https://food.ec.europa.eu/animals/animal-welfare/evaluations-and-impact-assessment/revision-eu-animal-welfare-legislation_en">
                  .
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                </p>
                <p>
                 The Commission will continue to develop supporting measures, such as best practices, guidelines, recommendations and studies, for the promotion of and the transition to non-cage farming. In addition, the Commission will further consider which role animal welfare labelling and public procurement might play in this context.
                </p>
               </div>
              </div>
             </div>
             <div class="ecl-u-mb-2xl">
              <a id="paragraph_436">
              </a>
              <div>
               <div class="ecl">
                <h2 class="ecl-u-type-heading-2" id="supporting-measures">
                 Supporting measures
                </h2>
               </div>
               <div class="ecl">
                <p>
                 A pilot project “Best Practice Hens” implemented from 2021 to 2023, aimed to help egg producers meet market demand by providing practical guidance on how to transition to alternative, higher-welfare cage-free systems. Materials developed under this project are published on a
                 <a class="ecl-link ecl-link--icon" href="https://bestpracticehens.eu/materials/">
                  <span class="ecl-link__label">
                   dedicated website
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 .
                </p>
               </div>
              </div>
             </div>
             <div class="ecl-u-mb-2xl">
              <a id="paragraph_2217">
              </a>
              <div>
               <div class="ecl">
                <h2 class="ecl-u-type-heading-2" id="press-release">
                 Press release
                </h2>
               </div>
               <div class="ecl">
                <p>
                 Please see the
                 <a href="https://ec.europa.eu/commission/presscorner/detail/en/ip_21_3297">
                  press release
                 </a>
                 <button aria-controls="laco-modal" class="wt-unselected wt-laco wt-laco--button wt-offprint" title="Search for available translations" type="button">
                  <svg aria-hidden="true" focusable="false" height="20" viewBox="0 0 82.205 82.205" width="20" xmlns="http://www.w3.org/2000/svg">
                   <g fill="none" stroke="#040404" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="3">
                    <circle cx="40.98" cy="41.103" fill="#fff" r="22.347">
                    </circle>
                    <path d="M40.98,76.103c19.33,0,35-15.67,35-35">
                    </path>
                    <path d="M40.98,6.103c-19.33,0-35,15.67-35,35">
                    </path>
                    <ellipse cx="40.98" cy="41.103" rx="12.551" ry="22.347">
                    </ellipse>
                    <line x1="40.98" x2="40.98" y1="18.755" y2="63.449">
                    </line>
                    <line x1="18.633" x2="63.326" y1="41.103" y2="41.103">
                    </line>
                    <polyline points="12.182,31.81 5.981,41.101 2.005,30.661">
                    </polyline>
                    <polyline points="80.2,51.375 75.816,41.084 69.965,50.592">
                    </polyline>
                   </g>
                  </svg>
                 </button>
                 from 30 June 2021.
                </p>
               </div>
              </div>
             </div>
             <div>
              <a id="paragraph_438">
              </a>
              <div>
               <div class="ecl">
                <h2 class="ecl-u-type-heading-2" id="video">
                 Video
                </h2>
               </div>
               <div class="ecl">
                <p>
                 On the occasion of the adoption of its communication on ‘End the Cage Age’, the Commission has
                 <a class="ecl-link ecl-link--icon" href="https://vimeo.com/567105378/79af612ef3">
                  <span class="ecl-link__label">
                   released a video
                  </span>
                  <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external" fill="currentColor" focusable="false" height="48" viewBox="0 0 48 48" width="48" xmlns="xmlns=&quot;http://www.w3.org/2000/svg">
                   <path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z" fill-rule="evenodd">
                   </path>
                   <path d="M39 42V24h3v18c0 1.65-1.35 3-3 3H6c-1.65 0-3-1.35-3-3V9c0-1.65 1.35-3 3-3h18v3H6v33z" fill-rule="evenodd">
                   </path>
                  </svg>
                 </a>
                 .
                </p>
               </div>
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
