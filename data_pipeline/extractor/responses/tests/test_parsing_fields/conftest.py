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

# HTML SCHEMA EVOLUTION
# ──────────────────────────────────────────────────────────────────────────
# 2012  Bare HTML fragments — no ECL wrapper, plain <h2> headings (no id,
#       no <strong>). Section names vary ("More information" vs "Other
#       information"). A footer banner is always present, either as a bare
#       <figure> or inside a <div data-inpage-navigation-source-area>.
#       No "Submission and examination" section yet.
#
# 2017  Two scraped versions exist per initiative (old and new page).
#       v1: still no ECL wrapper, banner still present. Sub-headings appear
#           (<h6> in 000002, <h4> in 000004). 000004 introduces <h2 id=…>
#           with a combined "Answer … and follow-up" title and SVG link icons.
#           Note the persistent typo: id="Answer-of-the-European-Commision".
#       v2: <div class="ecl"> wrapper added, banner gone. 000004 gains a
#           "Submission and examination" section and starts nesting <p> tags
#           inside <h2>.
#
# 2018–2020  ECL wrapper is now universal. Headings standardise to
#       <h2><strong>…</strong></h2> (id still absent on most). "Submission
#       and examination" becomes a standard section. From 2019/000016 onward,
#       an ecl-file download component appears after the Answer heading.
#       2020/000001 is an outlier: an extra outer <div> wraps the ECL div,
#       and some bullet lists use a "●" Unicode character in <p> tags instead
#       of <ul><li>. Empty <p></p> whitespace artefacts appear throughout.
#
# 2021–2022  id attributes return consistently on <h2><strong> headings,
#       starting with "Submission and examination". The ecl-file component
#       moves from the Answer section into the Submission section.
#
# 2024  ecl-file gains publication metadata (<ul class="ecl-file__detail-meta">)
#       and a file-format label (<div class="ecl-file__meta">, e.g. "(HTML)").
#       All <h2> headings now carry both id and <strong>.
# ──────────────────────────────────────────────────────────────────────────

# fmt: off
_ECI_HTML = [
    ("2012/000003", """
<h2>Answer of the European Commission</h2>
<p>The Commission committed, in particular, to taking the following actions:</p>
<ul>
  <li>reinforcing implementation of EU water quality legislation, building on the commitments presented in the 7th Environment Action Programme (EAP) and the Water Blueprint;</li>
  <li>launching an EU-wide public consultation on the Drinking Water Directive;</li>
  <li>improving transparency for urban wastewater and drinking water data management;</li>
  <li>advocating universal access to safe drinking water as a priority for Sustainable Development Goals.</li>
</ul>
<p>Official documents related to the decision:</p>
<ul>
  <li><a href="https://ec.europa.eu/transparency/documents-register/detail?ref=COM(2014)177&amp;lang=en">Communication</a></li>
  <li><a href="https://ec.europa.eu/transparency/documents-register/detail?ref=COM(2014)177&amp;lang=en">Annex</a></li>
</ul>
<h2>Follow-up</h2>
<p>This section provides regularly updated information on follow-up actions taken by the Commission.</p>
<ul>
  <li>An <strong>amendment to the</strong> <a href="http://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv:OJ.L_.2015.260.01.0006.01.ENG">Drinking Water Directive</a> came into force on 28 October 2015 (see <a href="http://europa.eu/rapid/press-release_IP-15-5940_en.htm">press release</a>).</li>
  <li><a href="http://ec.europa.eu/environment/water/water-drink/pdf/revised_drinking_water_directive.pdf"><strong>A proposal for the revision of the Directive on drinking water</strong></a> was adopted on 01 February 2018.</li>
</ul>
<h2>More information</h2>
<ul>
  <li>The <strong>European Parliament</strong> adopted an <a href="http://www.europarl.europa.eu/sides/getDoc.do?pubRef=-//EP//NONSGML+TA+P8-TA-2015-0294+0+DOC+PDF+V0//EN">own-initiative report</a> on 08/09/2015.</li>
</ul>
<div data-inpage-navigation-source-area="h2">
  <section class="ecl-banner ecl-banner--m">
    <figure class="ecl-banner__picture-container">
      <picture class="ecl-picture ecl-banner__picture">
        <img alt="Footer banner" src="/hero-banner-bg.png">
      </picture>
    </figure>
  </section>
</div>
"""),
    ("2012/000005", """
<h2>Answer of the European Commission</h2>
<p>Decision date: 28/05/2014<br>Official documents related to the decision:</p>
<h2>Follow-up</h2>
<p>In the Communication adopted on 28/05/2014, the Commission explains that it has decided not to submit
a legislative proposal, given that Member States and the European Parliament had only recently discussed
and decided EU policy in this regard. See <a href="http://europa.eu/rapid/press-release_IP-14-608_en.htm">press release</a>.</p>
<figure class="ecl-banner__picture-container">
  <picture class="ecl-picture ecl-banner__picture">
    <img alt="Footer banner" src="/hero-banner-bg.png">
  </picture>
</figure>
"""),
    ("2012/000007", """
<h2>Answer of the European Commission</h2>
<p>Decision date: 03/06/2015</p>
<p><br>Official documents related to the decision:</p>
<ul>
  <li><a href="https://ec.europa.eu/transparency/documents-register/detail?ref=C(2015)3773&amp;lang=en">Communication</a></li>
  <li><a href="https://ec.europa.eu/transparency/documents-register/detail?ref=C(2015)3773&amp;lang=en">Annex</a></li>
</ul>
<p>While the Commission does share the conviction that animal testing should be phased out in Europe,
its approach for achieving that objective differs from the one proposed in this Citizens' Initiative.</p>
<p>The Commission commits to active monitoring of compliance and enforcement of the legislation, and will
continue supporting the development and validation of alternative approaches to the use of animals in
research and testing.</p>
<h2>Follow-up</h2>
<p>The Commission adopted a Communication on 03 June 2015 in response to the initiative
<a href="http://ec.citizens-initiative.europa.eu/public/initiatives/successful/details/2012/000007">Stop Vivisection</a>.
See <a href="http://europa.eu/rapid/press-release_IP-15-5094_en.htm">press release</a>.</p>
<h2>Other information</h2>
<p>On 18 April 2017, the European Ombudsman issued a
<a href="https://www.ombudsman.europa.eu/en/cases/decision.faces/en/78182/html.bookmark">decision</a>
concerning the initiative 'Stop Vivisection'. The Ombudsman concluded that there was no maladministration.</p>
<figure class="ecl-banner__picture-container">
  <picture class="ecl-picture ecl-banner__picture">
    <img alt="Footer banner" src="/hero-banner-bg.png">
  </picture>
</figure>
"""),
    ("2017/000002", """
<h2>Answer of the European Commission</h2>
<p>Official documents:</p>
<p>Main conclusions of the Communication:</p>
<ul>
  <li>On the first aim, to 'ban glyphosate-based herbicides', the Commission concluded that there are
  neither scientific nor legal grounds to justify a ban of glyphosate, and will not make a legislative
  proposal to that effect.</li>
</ul>
<h2>Follow-up</h2>
<p>This section provides information on the follow-up actions taken by the Commission.</p>
<h6><strong>Legislative action on aim 2 ('to ensure that the scientific evaluation of pesticides for
EU regulatory approval is based only on published studies [...]'):</strong></h6>
<p>The <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32019R1381">Regulation
of the European Parliament and the Council</a> was published on 6 September 2019 and became applicable
on 27 March 2021.</p>
<figure class="ecl-banner__picture-container">
  <picture class="ecl-picture ecl-banner__picture">
    <img alt="Footer banner" src="/hero-banner-bg.png">
  </picture>
</figure>
"""),
    ("2017/000004", """
<h2 id="Answer-of-the-European-Commision">
  Answer of the European Commission and follow-up
</h2>
<h4>Official document:</h4>
<ul>
  <li><a href="https://ec.europa.eu/transparency/documents-register/detail?ref=C(2021)171&amp;lang=en">Communication</a></li>
</ul>
<p>Main conclusions of the Communication:</p>
<p>Inclusion and respect for the rich cultural diversity of Europe is one of the priorities of the
European Commission. While no further legal acts are proposed, the full implementation of legislation
and policies already in place provides a powerful set of measures to support the initiative's goals.</p>
<h4>Follow-up</h4>
<ul>
  <li>The Commission implements funding programmes in the areas of culture and education (notably
  Erasmus+) which are fully accessible for small regional or minority language communities.</li>
  <li>Regarding the promotion of linguistic diversity, the Commission is further developing its
  cooperation with the Council of Europe's
  <a class="ecl-link ecl-link--icon" href="https://www.ecml.at/ECML-Programme/ECML-ECCooperation/Colloquium2023/tabid/5664/language/en-GB/Default.aspx">
    <span class="ecl-link__label">colloquium on Strengthening support to regional and minority languages</span>
    <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external"><path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z"/></svg>
  </a>
  co-organised with the ECML in November 2023.</li>
</ul>
<p><strong>Other information</strong></p>
<p>In a <a href="https://curia.europa.eu/jcms/upload/docs/application/pdf/2022-11/cp220179en.pdf">judgement</a>
of 9 November 2022, the General Court dismissed the request to annul the Commission Communication
C(2021) 171.</p>
<div data-inpage-navigation-source-area="h2">
  <section class="ecl-banner ecl-banner--m">
    <figure class="ecl-banner__picture-container">
      <picture class="ecl-picture ecl-banner__picture">
        <img alt="Footer banner" src="/hero-banner-bg.png">
      </picture>
    </figure>
  </section>
</div>
"""),    
("2017/000002", """
<div class="ecl">
<h2>Answer of the European Commission</h2>
<p>Official documents:</p>
<ul>
  <li><a href="https://ec.europa.eu/transparency/documents-register/detail?ref=C(2017)8414">Communication</a></li>
</ul>
<ul>
  <li><a href="https://ec.europa.eu/transparency/documents-register/api/files/C(2017)8414_1/de00000000208522?rendition=false">Annex</a></li>
</ul>
<p>Main conclusions of the Communication:</p>
<ul>
  <li>On the first aim, to 'ban glyphosate-based herbicides', the Commission concluded that there are
  neither scientific nor legal grounds to justify a ban of glyphosate, and will not make a legislative
  proposal to that effect.</li>
</ul>
<ul>
  <li>On the third aim, to 'set EU-wide mandatory reduction targets for pesticide use', the Commission
  intends to focus on the implementation of the
  <a href="https://ec.europa.eu/food/plant/pesticides/sustainable_use_pesticides_en">Sustainable Use Directive</a>.</li>
</ul>
<h2>Follow-up</h2>
<h6><strong>Legislative action on aim 2 ('to ensure that the scientific evaluation of pesticides for
EU regulatory approval is based only on published studies [...]'):</strong></h6>
<p>The <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32019R1381">Regulation
of the European Parliament and the Council</a> was published on 6 September 2019 and became applicable
on 27 March 2021.</p>
</div>
<div data-inpage-navigation-source-area="h2">
  <section class="ecl-banner ecl-banner--m">
    <figure class="ecl-banner__picture-container">
      <picture class="ecl-picture ecl-banner__picture">
        <img alt="Footer banner" src="/hero-banner-bg.png">
      </picture>
    </figure>
  </section>
</div>
"""),
    ("2017/000004", """
<div class="ecl">
<h2 id="Submission-and-examination">Submission and examination
  <p><a href="https://citizens-initiative.europa.eu/initiatives/details/2017/000004_en">Minority
  SafePack – one million signatures for diversity in Europe</a> was submitted on 10 January 2020,
  having gathered 1,123,422 statements of support.</p>
  <p>The Commission adopted a Communication on 14 January 2021. See
  <a href="https://ec.europa.eu/commission/presscorner/detail/en/ip_21_81">press release</a>.</p>
</h2>
<h2 id="Answer-of-the-European-Commision">
  Answer of the European Commission and follow-up
</h2>
<h4>Official document:</h4>
<ul>
  <li><a href="https://ec.europa.eu/transparency/documents-register/detail?ref=C(2021)171&amp;lang=en">Communication</a></li>
</ul>
<p>Main conclusions of the Communication:</p>
<p>While no further legal acts are proposed, the full implementation of legislation and policies
already in place provides a powerful set of measures to support the initiative's goals.</p>
<h4>Follow-up</h4>
<ul>
  <li>The Commission implements funding programmes in culture and education (notably Erasmus+)
  accessible for small regional or minority language communities, as detailed in the
  <a href="https://op.europa.eu/en/publication-detail/-/publication/d325c589-011a-11ef-a251-01aa75ed71a1/language-en">2024
  publication 'Linguistic diversity in the European Union'</a>.</li>
  <li>The Commission is developing cooperation with the ECML, notably a
  <a class="ecl-link ecl-link--icon" href="https://www.ecml.at/ECML-Programme/ECML-ECCooperation/Colloquium2023/tabid/5664/language/en-GB/Default.aspx">
    <span class="ecl-link__label">colloquium on Strengthening support to regional and minority languages</span>
    <svg aria-hidden="true" class="ecl-icon ecl-icon--xs ecl-link__icon ecl-icon--external"><path d="M30 6V3h15v15h-3V8.13L29.13 21 27 18.87 39.87 6z"/></svg>
  </a>
  co-organised in November 2023.</li>
</ul>
<p><strong>Other information</strong></p>
<p>In a <a href="https://curia.europa.eu/jcms/upload/docs/application/pdf/2022-11/cp220179en.pdf">judgement</a>
of 9 November 2022, the General Court dismissed the request to annul C(2021) 171. The appeal was
dismissed by the <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62023CJ0026">Court
judgment</a> of 5 June 2025.</p>
</div>
<div data-inpage-navigation-source-area="h2">
  <section class="ecl-banner ecl-banner--m">
    <figure class="ecl-banner__picture-container">
      <picture class="ecl-picture ecl-banner__picture">
        <img alt="Footer banner" src="/hero-banner-bg.png">
      </picture>
    </figure>
  </section>
</div>
"""),
    ("2018/000004", """
<div class="ecl">
<h2><strong>Submission and examination</strong>
  <p><a href="https://citizens-initiative.europa.eu/initiatives/details/2018/000004_en">'End the
  Cage Age'</a> was submitted on 2 October 2020, having gathered 1,397,113 statements of support.</p>
  <p>The Commission adopted a Communication on 30 June 2021. See
  <a href="https://ec.europa.eu/commission/presscorner/detail/en/ip_21_3297">press release</a>.</p>
</h2>
<h2><strong>Answer of the European Commission</strong></h2>
<p>Main conclusions of the <a href="https://ec.europa.eu/transparency/documents-register/detail?ref=C(2021)4747&amp;lang=en">Communication</a>:</p>
<p>The Commission communicated its intention to table a legislative proposal, by the end of 2023, to
phase out, and finally prohibit, the use of cages for all animals mentioned in the ECI.</p>
<p>The new Common Agricultural Policy will provide financial support and incentives to help farmers
upgrade to more animal-friendly facilities in line with the new standards.</p>
<h2><strong>Follow-up</strong></h2>
<p>As established by the <a href="https://agriculture.ec.europa.eu/vision-agriculture-food_en">Vision
for Agriculture and Food</a> adopted on 19 February 2025, the Commission will present proposals on
the revision of the existing EU animal welfare legislation, including its commitment to phase out
cages.</p>
<p>On 19 September 2025, the Commission launched a
<a href="https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14671-On-farm-animal-welfare-for-certain-animals-modernisation-of-EU-legislation/public-consultation_en">public
consultation</a> open until 12 December 2025. For further updates, check the
<a href="https://food.ec.europa.eu/animals/animal-welfare/eci/eci-end-cage-age_en">dedicated web
page</a>.</p>
</div>
<div data-inpage-navigation-source-area="h2">
  <section class="ecl-banner ecl-banner--m">
    <figure class="ecl-banner__picture-container">
      <picture class="ecl-picture ecl-banner__picture">
        <img alt="Footer banner" src="/hero-banner-bg.png">
      </picture>
    </figure>
  </section>
</div>
"""),
("2019/000007", """
<div class="ecl">
<h2 id="Answer-of-the-European-Commission"><strong>Answer of the European Commission</strong></h2>
<p>Main conclusions of the <a href="https://citizens-initiative.europa.eu/sites/default/files/2025-09/C20256015EN.pdf"><u>Communication</u></a>:</p>
<p>The Commission carefully analysed the citizens' proposals and concluded that while some proposals
fall outside of EU competence, others are already covered under the current Cohesion policy thanks to
its robust safeguards promoting inclusion and equal treatment of minorities.</p>
<p>Consequently, no new legislation will be proposed in response to this ECI. However, the Commission
will continue to ensure non-discriminatory access to Union funding and to monitor Member States'
actions to guarantee equal treatment in the implementation of Cohesion policy.</p>
</div>
<div data-inpage-navigation-source-area="h2">
  <section class="ecl-banner ecl-banner--m">
    <figure class="ecl-banner__picture-container">
      <picture class="ecl-picture ecl-banner__picture">
        <img alt="Footer banner" src="/hero-banner-bg.png">
      </picture>
    </figure>
  </section>
</div>
"""),
("2019/000016", """
<div class="ecl">
 <p></p>
 <h2><strong>Submission and examination</strong></h2>
 <p>The <a href="https://citizens-initiative.europa.eu/initiatives/details/2019/000016_en">'Save
 bees and farmers!'</a> initiative was submitted on 7 October 2022. See
 <a href="https://ec.europa.eu/commission/presscorner/detail/en/mex_22_6074">press announcement</a>.</p>
 <p>The Commission adopted a Communication on 5 April 2023. See
 <a href="https://ec.europa.eu/commission/presscorner/detail/en/ip_23_2084"><u>press release</u></a>.</p>
 <p></p>
 <h2><strong>Answer of the European Commission</strong></h2>
 <div class="ecl-file ecl-file--thumbnail" data-ecl-file="" id="ecl-file-2120600983">
  <div class="ecl-file__container">
   <div class="ecl-file__info">
    <div class="ecl-file__title" id="ecl-file-2120600983-title">
     Factsheet &#8211; Successful Initiatives &#8211; Save bees and farmers
    </div>
   </div>
  </div>
  <div class="ecl-file__footer">
   <a class="ecl-link ecl-link--standalone ecl-link--icon ecl-file__download"
      href="/document/download/4f0c11b9-e808-41d7-8d82-b94b898fb0f5_en?filename=7%20Factsheet%20Save%20Bees%20and%20Farmers%20ECI_EN.pdf"
      id="ecl-file-2120600983-link">
    <span class="ecl-link__label" id="ecl-file-2120600983-link-label">Download</span>
   </a>
  </div>
 </div>
 <p>Rather than proposing new legislative acts, the priority is to ensure that
 <strong>the proposals currently being negotiated are timely adopted and implemented</strong>,
 together with an <strong>effective implementation of the CAP</strong>.</p>
 <ul>
  <li>the <a href="https://ec.europa.eu/commission/presscorner/detail/en/ip_22_3746">Nature
  Restoration Law</a></li>
  <li><a href="https://ec.europa.eu/commission/presscorner/detail/en/ip_22_3746">Sustainable
  Use of Plant Protection Products Regulation</a></li>
  <li><a href="https://ec.europa.eu/commission/presscorner/detail/en/ip_23_281">revised EU
  Pollinators&#8217; Initiative</a></li>
 </ul>
 <p></p>
 <p>On 25 April 2023, Commissioner Sinkevičius met with the organisers.</p>
 <h2>Updates on the Commission's proposals</h2>
 <p>The Nature Restoration Law entered into force on 18 August 2024. See the
 <a href="https://environment.ec.europa.eu/topics/nature-and-biodiversity/nature-restoration-law_en">
 <u>dedicated Commission website</u></a>.</p>
 <p>The Commission <a href="https://eur-lex.europa.eu/eli/C/2024/3117/oj">withdrew</a> its
 proposal on Sustainable Use of Plant Protection Products on 27 March 2024.</p>
 <p></p>
</div>
<div data-inpage-navigation-source-area="h2">
  <section class="ecl-banner ecl-banner--m">
    <figure class="ecl-banner__picture-container">
      <picture class="ecl-picture ecl-banner__picture">
        <img alt="Footer banner" src="/hero-banner-bg.png">
      </picture>
    </figure>
  </section>
</div>
"""),
("2020/000001", """
<div>
 <div class="ecl">
  <p></p>
  <h2><strong>Submission and examination</strong></h2>
  <p>The '<a href="https://citizens-initiative.europa.eu/initiatives/details/2020/000001_en">Stop
  Finning &#8211; Stop the trade</a>' initiative was submitted on 11 January 2023, having gathered
  1,119,996 verified statements of support. See
  <a href="https://ec.europa.eu/commission/presscorner/detail/en/mex_23_143">press announcement</a>.</p>
  <p>A&nbsp;public hearing&nbsp;took place at the European Parliament on 27 March 2023. See
  <a href="https://multimedia.europarl.europa.eu/en/webstreaming/envi-pech-peti-committee-meeting_20230327-1500-COMMITTEE-PECH-ENVI-PETI">recording</a>.</p>
  <p>The Commission adopted a Communication on 5 July 2023. See
  <a href="https://ec.europa.eu/commission/presscorner/detail/en/IP_23_3676">press release</a>.</p>
  <h2><strong>Answer of the European Commission</strong></h2>
  <div class="ecl-file ecl-file--thumbnail" data-ecl-file="" id="ecl-file-1216333423">
   <div class="ecl-file__container">
    <div class="ecl-file__info">
     <div class="ecl-file__title" id="ecl-file-1216333423-title">
      Factsheet - Successful Initiatives - Stop Finning-Stop the trade
     </div>
    </div>
   </div>
   <div class="ecl-file__footer">
    <a class="ecl-link ecl-link--standalone ecl-link--icon ecl-file__download"
       href="/document/download/0d2f6f03-b148-4055-b057-16d92f5246f6_en?filename=dg_mare-eci_fs_stop_finning_trade_20230705v01.pdf"
       id="ecl-file-1216333423-link">
     <span class="ecl-link__label" id="ecl-file-1216333423-link-label">Download</span>
    </a>
   </div>
  </div>
  <p></p>
  <p>Main conclusions of the
  <a href="https://citizens-initiative.europa.eu/sites/default/files/2023-07/C_2023_4489_1_EN.pdf">Communication</a>:</p>
  <p>The Commission commits to:</p>
  <p>&#9679; Start without delay preparatory work with a view to launch, by the end of 2023, an impact
  assessment on the environmental, social and economic consequences of applying the &#8220;fins
  naturally attached&#8221; policy.</p>
  <p>&#9679; By end 2024, provide more detailed EU import and export information to improve statistics
  on trade in shark products.</p>
  <p>&#9679; Step up the EU&#8217;s international action: advocate for a worldwide ban of shark
  finning and strengthen conservation and management measures for sharks&#8217; species.</p>
  <p></p>
  <p>On 13 July 2023, Commissioner Sinkevičius met with the organisers of 'Stop Finning - Stop the
  trade' to discuss the Commission's reply.</p>
  <h2>Follow-up</h2>
  <p>In the second half of 2023 the European Commission started&nbsp;working on an impact assessment
  on the consequences of applying the &#8220;fins naturally attached&#8221; policy.</p>
  <p>In 2024, the Commission organised a
  <a href="https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14158-Better-protecting-sharks-through-sustainable-fishing-and-trade_en">call for evidence</a>
  seeking views on a potential ban on EU sales and trade of loose shark fins. Its results can be found
  on the <a href="https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14158-Better-protecting-sharks-through-sustainable-fishing-and-trade/public-consultation_en">dedicated page.</a></p>
  <p>The Commission created 13 new
  <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32024R2522"><u>tariff codes
  for sharks and their fins</u></a>. These codes enter in application in January 2025.</p>
  <p>More information on the
  <a href="https://oceans-and-fisheries.ec.europa.eu/ocean/marine-biodiversity/sharks_en"><u>EU sharks'
  protection and management</u></a> page.</p>
  <p></p>
 </div>
</div>
<div data-inpage-navigation-source-area="h2">
  <section class="ecl-banner ecl-banner--m">
    <figure class="ecl-banner__picture-container">
      <picture class="ecl-picture ecl-banner__picture">
        <img alt="Footer banner" src="/hero-banner-bg.png">
      </picture>
    </figure>
  </section>
</div>
"""),
("2021/000006", """
<div class="ecl">
 <h2 id="Submission-and-examination"><strong>Submission and examination</strong></h2>
 <p>The '<a href="https://citizens-initiative.europa.eu/initiatives/details/2021/000006_en">Save
 Cruelty Free Cosmetics - Commit to a Europe Without Animal Testing</a>' initiative was submitted
 on 25 January 2023, having gathered 1,217,916<strong></strong> verified statements of support.
 See <a href="https://ec.europa.eu/commission/presscorner/detail/en/mex_23_382">press
 announcement</a>.</p>
 <p>The initiative was debated at the European Parliament&#8217;s plenary on 10 July 2023. See
 <a href="https://multimedia.europarl.europa.eu/en/webstreaming/plenary-session_20230710-0900-PLENARY"><u>recording</u></a>.</p>
 <p>The Commission adopted a Communication on 25 July 2023. See
 <a href="https://ec.europa.eu/commission/presscorner/detail/en/IP_23_3993">press release.</a></p>
 <p></p>
 <h2><strong>Answer of the European Commission</strong></h2>
 <div class="ecl-file ecl-file--thumbnail" data-ecl-file="" id="ecl-file-2121608236">
  <div class="ecl-file__container">
   <div class="ecl-file__info">
    <div class="ecl-file__title" id="ecl-file-2121608236-title">
     Factsheet &#8211; Successful Initiatives &#8211; Save cruelty free cosmetics
    </div>
   </div>
  </div>
  <div class="ecl-file__footer">
   <a class="ecl-link ecl-link--standalone ecl-link--icon ecl-file__download"
      href="/document/download/56b85308-4559-439e-8ed6-e4029aa144f7_en?filename=09_Save%20Cruelty%20Free%20Cosmetics_2023_EN.pdf"
      id="ecl-file-2121608236-link">
    <span class="ecl-link__label" id="ecl-file-2121608236-link-label">Download</span>
   </a>
  </div>
 </div>
 <ul>
  <li><strong>Protect the cosmetics animal testing ban:</strong> The Commission will defend the
  ban before the Court of Justice of the EU and consider<strong></strong> outcomes for future
  legislative changes.</li>
  <li><strong>Transform EU chemicals legislation:</strong> The Commission will work on a roadmap
  towards chemical safety assessments free from animal testing.</li>
 </ul>
 <h2>Follow-up</h2>
 <p><strong>Follow-up meeting</strong></p>
 <p>On 8 November 2023, Commissioner Sinkevi&#269;ius met with the organisers.</p>
 <p lang="EN-US">See the information on the roadmap on the
 <a href="https://single-market-economy.ec.europa.eu/sectors/chemicals/reach/roadmap-towards-phasing-out-animal-testing_en">dedicated website</a>.</p>
 <p>The<strong></strong>
 <a href="https://single-market-economy.ec.europa.eu/sectors/chemicals/european-partnership-alternative-approaches-animal-testing_en"><u>European Partnership for Alternative Approaches to Animal Testing (EPAA)</u></a>
 is a&nbsp;partnership between the Commission and industry.</p>
 <p><strong>Judgments of the General Court</strong>
 (<a href="https://curia.europa.eu/juris/document/document.jsf?docid=279983">T-655/20</a>
 and
 <a href="https://curia.europa.eu/juris/document/document.jsf?docid=279984">T-656/20</a>)</p>
 <p>The General Court issued its judgments on 22 November 2023. The Commission will consider
 them in view of<strong></strong> any potential future measures.</p>
</div>
<div data-inpage-navigation-source-area="h2">
  <section class="ecl-banner ecl-banner--m">
    <figure class="ecl-banner__picture-container">
      <picture class="ecl-picture ecl-banner__picture">
        <img alt="Footer banner" src="/hero-banner-bg.png">
      </picture>
    </figure>
  </section>
</div>
"""),
("2022/000002", """
<div class="ecl">
 <h2 id="Submission-and-examination"><strong>Submission and examination</strong></h2>
 <p>The '<a href="https://citizens-initiative.europa.eu/initiatives/details/2022/000002_en">Fur
 Free Europe</a>' initiative was submitted on 14 June 2023, having gathered&nbsp;1,502,319&nbsp;
 verified statements of support. See
 <a href="https://ec.europa.eu/commission/presscorner/detail/en/mex_23_3282">press
 announcement</a>.</p>
 <p>The initiative was debated at the European Parliament's plenary on 19 October 2023.
 See&nbsp;recording&nbsp;(
 <a href="https://multimedia.europarl.europa.eu/en/video/european-citizens-initiative-fur-free-europe-opening-statement-by-michal-wiezik-renew-sk-author-and-iliana-ivanova-european-commissioner-for-innovation-research-culture-education-and-youth_I247290">part 1</a>
 and
 <a href="https://multimedia.europarl.europa.eu/en/video/european-citizens-initiative-fur-free-europe-meps-debate_I247291">part 2</a>).</p>
 <p>The Commission adopted a Communication on 7 December 2023. See
 <a href="https://ec.europa.eu/commission/presscorner/detail/en/ip_23_6251">press release</a>
 and
 <a href="https://ec.europa.eu/commission/presscorner/detail/en/QANDA_23_6254">questions and
 answers</a><em>.</em></p>
 <div class="ecl-file ecl-file--thumbnail" data-ecl-file="" id="ecl-file-530511715">
  <div class="ecl-file__container">
   <div class="ecl-file__info">
    <div class="ecl-file__title" id="ecl-file-530511715-title">
     Factsheet - Successful Initiatives - Fur Free Europe
    </div>
   </div>
  </div>
  <div class="ecl-file__footer">
   <a class="ecl-link ecl-link--standalone ecl-link--icon ecl-file__download"
      href="/document/download/e3395521-65c6-41f0-a576-5eff0382665f_en?filename=Factsheet%20-%20Successful%20Initiatives%20-%20Fur%20Free%20Europe.pdf"
      id="ecl-file-530511715-link">
    <span class="ecl-link__label" id="ecl-file-530511715-link-label">Download</span>
   </a>
  </div>
 </div>
 <p></p>
 <h2><strong>Answer of the European Commission</strong></h2>
 <p>Main conclusions of the
 <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52023XC01559">Communication</a>:</p>
 <p>The Commission&nbsp;has tasked the European Food Safety Authority (EFSA) to provide a
 scientific opinion on the welfare of animals farmed for fur.</p>
 <p>Building on this scientific input and an assessment of economic and social impacts, the
 Commission will communicate by March 2026 on the most appropriate action.</p>
 <h2>Follow-up</h2>
 <p>On 9 February 2024, Commissioner Stella Kyriakides met with the organisers of 'Fur Free
 Europe' to discuss the Commission's reply.</p>
 <p>The Commission's work on the accompanying actions has been progressing. See the
 <a href="https://food.ec.europa.eu/animals/animal-welfare/eci/eci-fur-free-europe_en">dedicated
 website</a> for details.</p>
 <p></p>
</div>
<div data-inpage-navigation-source-area="h2">
  <section class="ecl-banner ecl-banner--m">
    <figure class="ecl-banner__picture-container">
      <picture class="ecl-picture ecl-banner__picture">
        <img alt="Footer banner" src="/hero-banner-bg.png">
      </picture>
    </figure>
  </section>
</div>
"""),
("2024/000004", """
<div class="ecl">
 <h2 id="Submission-and-examination"><strong>Submission and examination</strong></h2>
 <p>The <a href="https://citizens-initiative.europa.eu/initiatives/details/2024/000004_en">'My
 Voice, My Choice: For Safe And Accessible Abortion'</a> initiative was submitted on 1 September
 2025, having gathered&nbsp;1,124,513 verified statements of support. See
 <a href="https://ec.europa.eu/commission/presscorner/detail/en/mex_25_2004">European Commission
 news</a>.</p>
 <p>The initiative was debated at the European Parliament&#8217;s plenary on 16 December 2025. In
 the <a href="https://www.europarl.europa.eu/doceo/document/TA-10-2025-0338_EN.html">resolution</a>
 adopted on 17 December 2025, the Parliament expressed support. See
 <a href="https://www.europarl.europa.eu/news/en/press-room/20251211IPR32167/my-voice-my-choice-meps-support-citizens-initiative-on-accessible-abortion">press
 release</a>.</p>
 <p>The Commission adopted a Communication on 26 February 2026. See the Commission's
 <a href="https://ec.europa.eu/commission/presscorner/detail/en/ip_26_472">press release</a> and
 <a href="https://ec.europa.eu/commission/presscorner/detail/en/speech_26_492">Remarks by
 Executive Vice-President M&#238;nzatu and Commissioner Lahbib</a>.</p>
 <p></p>
 <div class="ecl-file ecl-file--thumbnail" data-ecl-file="" id="ecl-file-2117586954">
  <div class="ecl-file__container">
   <div class="ecl-file__info">
    <ul class="ecl-file__detail-meta">
     <li class="ecl-file__detail-meta-item">General publications</li>
     <li class="ecl-file__detail-meta-item">18 March 2026</li>
    </ul>
    <div class="ecl-file__title" id="ecl-file-2117586954-title">
     Factsheet - Successful Initiatives - My Voice, My Choice: For Safe And Accessible Abortion
    </div>
   </div>
  </div>
  <div class="ecl-file__footer">
   <div class="ecl-file__meta">(HTML)</div>
   <a class="ecl-link ecl-link--standalone ecl-link--icon ecl-file__download"
      href="/document/download/e7ba3ca9-10fd-4111-bbd9-eda1ff08fa13_en"
      id="ecl-file-2117586954-link">
    <span class="ecl-link__label" id="ecl-file-2117586954-link-label">Download</span>
   </a>
  </div>
 </div>
 <p></p>
 <h2><strong>Answer of the European Commission</strong></h2>
 <p>Main conclusions of the
 <a href="https://ec.europa.eu/transparency/documents-register/detail?ref=C(2026)3225&amp;lang=en">Communication</a>.</p>
 <p>Having carefully analysed the initiative and with regard to the EU Treaties&#8217; limitations
 to EU competence in the area of public health, the Commission underlines that Member States can
 rely on existing EU instruments to improve equal access to legally available and affordable
 healthcare services, including safe abortion services.</p>
 <p>This EU support can be provided through the
 <a href="https://european-social-fund-plus.ec.europa.eu/en">European Social Fund Plus</a> (ESF+)
 programme, in case Member States wish, voluntarily and in accordance with their national laws, to
 provide such support.</p>
 <p>As EU support can already be provided under existing instruments, it is not necessary to
 propose a new legal instrument.</p>
</div>
<div data-inpage-navigation-source-area="h2">
  <section class="ecl-banner ecl-banner--m">
    <figure class="ecl-banner__picture-container">
      <picture class="ecl-picture ecl-banner__picture">
        <img alt="Footer banner" src="/hero-banner-bg.png">
      </picture>
    </figure>
  </section>
</div>
"""),
]
# fmt: on

ECI_FIXTURES = [
    (reg_num, BeautifulSoup(html, "html.parser")) for reg_num, html in _ECI_HTML
]
