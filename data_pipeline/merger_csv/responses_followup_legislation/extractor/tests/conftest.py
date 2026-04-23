import pytest


@pytest.fixture
def commission_answers_rejection_legislation() -> list[tuple[bool, str, list[str]]]:
    """
    A pytest fixture providing mock test data for European Citizens' Initiatives (ECI)
    where the European Commission rejected demands to introduce new legislation.

    Returns:
        list[tuple[bool, str, list[str]]]: A list of tuples containing:

            - bool: A flag indicating whether the initiative was considered fully REJECTED
                    concerning new legislative proposals (True) or if it contained full/partial
                    commitments to other legislation (False).

            - str: The ECI registration number (e.g., '2012/000003').

            - list[str]: The expected extracted outcome strings highlighting the exact wording
                         used by the Commission to state no new legislation will be proposed.
                         If the test case is meant to fail or return nothing, this is None.

            - an example of rejection phrases as reference for developer
    """

    return [
        (
            False,
            "2012/000003",
            [
                "The Commission committed, in particular, to taking the following actions:",
                "reinforcing implementation of EU water quality legislation, building on the commitments presented in the 7th Environment Action Programme (EAP) and the Water Blueprint; launching an EU-wide public consultation on the Drinking Water Directive, notably in view of improving access to quality water in the EU; improving transparency for urban wastewater and drinking water data management and explore the idea of benchmarking water quality; bringing about a more structured dialogue between stakeholders on transparency in the water sector; cooperating with existing initiatives to provide a wider set of benchmarks for water services; stimulating innovative approaches for development assistance (e.g. support to partnerships between water operators and to public-public partnerships); promoting sharing of best practices between Member States (e.g. on solidarity instruments) and identifying new opportunities for cooperation; advocating universal access to safe drinking water and sanitation as a priority area for Sustainable Development Goals.",
                "Official documents related to the decision:",
            ],
            None,
        ),
        (
            True,
            "2012/000005",
            [
                "Decision date: 28/05/2014 Official documents related to the decision:",
                "In the Communication adopted on 28/05/2014, the Commission explains that it has decided not to submit a legislative proposal, given that Member States and the European Parliament had only recently discussed and decided EU policy in this regard. The Commission has concluded that the existing funding framework, which had been recently debated and agreed by EU Member States and the European Parliament, is the appropriate one. See [press release](http://europa.eu/rapid/press-release_IP-14-608_en.htm) .",
            ],
            ["not to submit a legislative proposal"],
        ),
        (
            False,
            "2017/000002",
            [
                "Official documents:",
                "Main conclusions of the Communication:",
                "On the first aim, to 'ban glyphosate-based herbicides', the Commission concluded that there are neither scientific nor legal grounds to justify a ban of glyphosate, and will not make a legislative proposal to that effect.",
                "On the second aim, to “ensure that the scientific evaluation of pesticides for EU regulatory approval is based only on published studies, which are commissioned by competent public authorities instead of the pesticide industry”, the Commission committed to come forward with a legislative proposal by May 2018, amongst others, to strengthen the transparency of the EU risk assessment in the food chain and enhance – through a series of measures – the governance for the conduct of industry studies submitted to the European Food Safety Authority (EFSA) for risk assessment. See details below under ‘Follow-up’.",
                "On the third aim, to 'set EU-wide mandatory reduction targets for pesticide use, with a view to achieving a pesticide-free future', the Commission concluded that it intends to focus on the implementation of the [Sustainable Use Directive](https://ec.europa.eu/food/plant/pesticides/sustainable_use_pesticides_en) , and will re-evaluate the situation, initially in a report to Council and the Parliament on the implementation of the Directive to be produced in 2019. The Commission committed also to establishing harmonised risk indicators to enable the monitoring of trends at EU level and to use the resulting data as a basis for determining future policy options.",
            ],
            [
                "will not make a legislative proposal to that effect"
            ],  # It is canceled by proposition of other later point legislation
            # e. g. "the Commission committed to come forward with a legislative proposal"
        ),
        (
            True,
            "2012/000007",
            [
                "Decision date: 03/06/2015",
                "Official documents related to the decision:",
                "Main conclusions of the Communication:",
                "While the Commission does share the conviction that animal testing should be phased out in Europe, its approach for achieving that objective differs from the one proposed in this Citizens' Initiative.",
                "The Commission considers that the Directive on the protection of animals used for scientific purposes (Directive 2010/63/EU), which the Initiative seeks to repeal, is the right legislation to achieve the underlying objectives of the Initiative. It sets full replacement of animals as its ultimate goal as soon as it is scientifically possibly, and provides a legally binding stepwise approach as non-animal alternatives become available. Therefore, no repeal of that legislation was proposed.",
                "Moreover, the Communication sets out four further Commission’s actions to be taken towards the goal of phasing out animal testing. These actions included a scientific conference engaging the scientific community and relevant stakeholders in a debate on how to exploit the advances in science for the development of scientifically valid non-animal approaches.",
                "The Commission commits to active monitoring of compliance and enforcement of the legislation, and will continue supporting the development and validation of alternative approaches to the use of animals in research and testing. Dialogue with all stakeholders will continue, especially with the scientific community, to advance towards the goal of phasing out animal testing through knowledge sharing, dissemination, and education and training activities on non-animal alternatives and the Three Rs (Replacement, Reduction and Refinement of animal use in testing).",
            ],
            [
                "no repeal of that legislation was proposed"
            ],  # One part of the request rejected but still open for a new legislation
        ),
        (
            True,
            "2017/000004",
            [
                "Official document:",
                "Main conclusions of the Communication:",
                "Inclusion and respect for the rich cultural diversity of Europe is one of the priorities and objectives of the European Commission. A wide range of measures addressing several aspects of the proposals of the initiative have been taken over the last years since the initiative was originally presented in 2013. The Communication assesses each of the nine individual proposals on its own merits, taking into account the principles of subsidiarity and proportionality. While no further legal acts are proposed, the full implementation of legislation and policies already in place provides a powerful set of measures to support the initiative’s goals.",
            ],
            ["no further legal acts are proposed"],
        ),
        (
            False,
            "2018/000004",
            [
                "Main conclusions of the [Communication](https://ec.europa.eu/transparency/documents-register/detail?ref=C(2021)4747&lang=en) :",
                "In its response to the ECI, the Commission communicated its intention to table a legislative proposal, by the end of 2023, to phase out, and finally prohibit, the use of cages for all animals mentioned in the ECI, under conditions to be determined on the basis of opinions from the European Food Safety Authority (EFSA) and the results of an impact assessment and a public consultation.",
                "In parallel to the legislation and to facilitate a balanced and economically viable transition to cage-free farming, the Commission will seek specific supporting measures in key related policy areas, such as trade and research and innovation. In particular, the new Common Agricultural Policy will provide financial support and incentives – such as the new eco-schemes instrument – to help farmers upgrade to more animal-friendly facilities in line with the new standards.",
                "On 30 June 2021, the Commission decided to positively respond to the ECI. [In its communication](https://ec.europa.eu/transparency/documents-register/detail?ref=C(2021)4747&lang=en) the Commission sets out plans for a legislative proposal to prohibit cages for the species and categories of animals covered by the ECI and to consider options for introducing rules or standards for imported products that are equivalent to the EU’s and/or a labelling requirement, in compliance with WTO rules. The Commission will also pursue or implement specific supporting measures in key related policy areas.",
                "The Commission has asked the European Food Safety Authority (EFSA) to complement the existing scientific evidence to determine the conditions needed for the prohibition of the use of cages. Scientific opinions were adopted by EFSA on the welfare on farm [of pigs](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2022.7421) of pigs (2022), [broilers,](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7788) broilers, addressing also broiler breeders (2022), [laying hens](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7789) laying hens , addressing also layer breeders and pullets (2022), [ducks, geese and quail](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7992) ducks, geese and quail (2023) and of [calves](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7896) calves (2023). The Commission also has started a series of stakeholder consultations in 2022, including in the context of subgroups of the EU Animal Welfare Platform (on poultry, on ruminants and on pigs).",
                "To facilitate a balanced and economically viable transition to cage-free farming, in which the competitiveness of the sectors concerned is further improved, the Commission is pursuing supporting measures in key related policy areas, such as research and innovation. Several research projects such as the [“Sustainability aspects of AW-promoting livestock systems”](https://www.eupahw.eu/pdf/projects/priority-%20area-3-green/JIPs_SOA17.pdf) “Sustainability aspects of AW-promoting livestock systems” under [the European Partnership on Animal Health and Welfare](https://www.eupahw.eu/) the European Partnership on Animal Health and Welfare , may be relevant in this context.",
                "The Common Agricultural Policy (CAP) provides financial support and incentives – such as the new eco-schemes instrument – to help farmers upgrade to more animal-friendly facilities. In its recommendations for the National Strategic Plans under the CAP, the Commission has regularly recommended the Member States to make efforts to promote e.g. the production of eggs under non-cage systems for laying hens.",
            ],
            None,
        ),
        (
            True,
            "2019/000007",
            [
                "Main conclusions of the [Communication](https://eur-lex.europa.eu/eli/C/2025/4991/oj/eng) Communication",
                "The Commission carefully analysed the citizens' proposals and concluded that while some proposals fall outside of EU competence, as they would interfere with the existing constitutional setup of the concerned Member States, others are already covered under the current Cohesion policy thanks to its robust safeguards promoting inclusion and equal treatment of minorities, as well as the respect for cultural and linguistic diversity.",
                "Consequently, no new legislation will be proposed in response to this ECI. However, the Commission will continue to ensure non-discriminatory access to Union funding and to monitor as well as support Member States' actions to guarantee equal treatment in the implementation of Cohesion policy.",
                "For the next Multiannual Financial Framework, the Commission has proposed a strengthened and modernised cohesion and growth policy that ensures adequate mechanisms are in place in Member States to ensure compliance with the relevant provisions of the Charter of Fundamental Rights throughout the implementation of the national and regional partnership plans, as well as respect for the principles of the rule of law. Where a Member State fails to fulfil these conditions, the Commission will withhold the corresponding payments.",
            ],
            ["no new legislation will be proposed "],
        ),
        (
            False,
            "2019/000016",
            [
                "In its [response to the ECI](https://ec.europa.eu/transparency/documents-register/detail?ref=C(2023)2320&lang=en) response to the ECI , the Commission welcomes the initiative and acknowledges its importance, in particular as the interlinked crises of climate change, pollution and biodiversity loss constitute growing challenges for Europe’s agriculture and food security.",
                "Since 2019 when the initiative started its collection of support, the Commission has been engaged in intensive work under the [European Green Deal](https://ec.europa.eu/info/strategy/priorities-2019-2024/european-green-deal_en) to ensure the sustainability of food systems, including on",
                "the [EU Farm to fork and the Biodiversity strategies](https://ec.europa.eu/commission/presscorner/detail/en/ip_20_884) the [Nature Restoration Law](https://ec.europa.eu/commission/presscorner/detail/en/ip_22_3746) [Sustainable Use of Plant Protection Products Regulation](https://ec.europa.eu/commission/presscorner/detail/en/ip_22_3746) [revised EU Pollinators’ Initiative](https://ec.europa.eu/commission/presscorner/detail/en/ip_23_281) the revised [EU common agricultural policy](https://agriculture.ec.europa.eu/common-agricultural-policy_en) 2023-2027",
                "The [proposal for a regulation on the sustainable use of plant protection products](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52022PC0305&qid=1678816018855) tabled in June 2022 sets out an ambitious path to reduce the risk and use of chemical pesticides in EU agriculture by 50% by 2030.",
                "The [proposal for a Nature Restoration Law](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=COM:2022:304:FIN) tabled in June 2022 combines an overarching restoration objective for the long-term recovery of nature in the EU’s land and sea areas with binding restoration targets for specific habitats and species.",
                "In its reply, the Commission underlined that rather than proposing new legislative acts, the priority is to ensure that the proposals currently being negotiated by the co-legislators are timely adopted and then implemented, together with an effective implementation of the CAP. Over one million statements in support of this citizens’ initiative are a clear signal and encouragement that the high level of ambition of the Commission proposals should be maintained.",
                "On 25 April 2023, Commissioner Virginijus Sinkevičius met with the organisers of 'Save bees and farmers!' to discuss the Commission’s reply to the initiative.",
                "Updates on the Commission's proposals",
                "Proposal for the Nature Restoration Law: following the agreement of the European Parliament on the text (on 27 February 2024), the Council of the EU adopted the regulation on 17 June 2024. It entered into force on 18 August 2024 (20 days after its publication in the Official Journal of the EU) and became applicable immediately.",
                "For up-to-date information on the Nature Restoration Law, see the [dedicated Commission website](https://environment.ec.europa.eu/topics/nature-and-biodiversity/nature-restoration-law_en) dedicated Commission website .",
                "Proposal for Regulation on the Sustainable Use of Plant Protection Products: In view of the rejection by the European Parliament of the proposal in November 2023, and a lack of progress of the discussions in the Council, the Commission decided on 27 March 2024 to [withdraw](https://eur-lex.europa.eu/eli/C/2024/3117/oj) its proposal.",
                "For up-to-date information on the developments in the field of sustainable use of pesticides, see the [dedicated Commission website](https://food.ec.europa.eu/plants/pesticides/sustainable-use-pesticides_en) .",
                "For up-to-date information on the EU Pollinators Initiative, see the [dedicated Commission website](https://environment.ec.europa.eu/topics/nature-and-biodiversity/pollinators_en) .",
            ],
            None,
        ),
        (
            False,
            "2020/000001",
            [
                "Main conclusions of the [Communication](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52023XC0804%2801%29&qid=1774949272886) :",
                "The Commission commits to:",
                "● Start without delay preparatory work with a view to launch, by the end of 2023, an impact assessment on the environmental, social and economic consequences of applying the “fins naturally attached” policy to the placing on the EU market of sharks, whether within the EU or for international trade (imports and exports).",
                "● By end 2024, provide more detailed EU’s import and export information to improve statistics on trade in shark products.",
                "● Better enforce the EU’s already strong traceability measures by strengthening the enforcement of EU law that applies to the entire value chain - control of fishing at sea, full traceability of shark products from landing to consumer, consumer information, and prevention and redress of illegal trade - and ensuring the collection and reporting of complete and reliable information by fishermen and Member States’ authorities on all these aspects.",
                "● Step up the EU’s international action: advocate for a worldwide ban of shark finning and strengthen the effective implementation of conservation and management measures for sharks’ species; encourage the reduction of demand for shark fins; and fight against shark fins trafficking.",
                "On 13 July 2023, Commissioner Virginijus Sinkevičius met with the organisers of ‘Stop Finning - Stop the trade' to discuss the Commission’s reply to the initiative.",
            ],
            None,
        ),
        (
            False,
            "2021/000006",
            [
                "Main conclusions of the [Communication](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52023XC0818%2801%29&qid=1773663489800) Communication :",
                "The Commission outlines the following actions to further reduce animal testing in response to specific objectives of the European citizens' initiative:",
                "Protect and strengthen the cosmetics animal testing ban: The EU Cosmetics Regulation already prohibits the placing on the market of cosmetic products that have been tested on animals, but this ban does not extend to safety tests required to assess risks from chemicals to workers and the environment under the EU Regulation on the Registration, Evaluation, Authorisation, and Restriction of Chemicals (REACH). The interface between the two pieces of legislation is currently being assessed in two cases before the Court of Justice of the European Union. The Commission will consider the outcome of the court cases in view of any future potential legislative changes. Transform EU chemicals legislation: The Commission will work together with all relevant parties on a roadmap towards chemical safety assessments that are free from animal testing. The roadmap will serve as a guiding framework for future actions and initiatives aimed at reducing and ultimately eliminating animal testing in the context of chemicals legislation within the European Union. Modernise science in the EU: The Commission will continue to strongly support\xa0 the development of alternative approaches with appropriate funding. It will also initiate a series of actions to accelerate the reduction of animal testing in research, education and training.",
            ],
            None,
        ),
        (
            False,
            "2022/000002",
            [
                "Main conclusions of the [Communication](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52023XC01559) :",
                "The Commission\xa0has tasked the European Food Safety Authority (EFSA) to provide a scientific opinion on the welfare of animals farmed for fur.",
                "Building further on this scientific input, and on an assessment of economic and social impacts, the Commission will then communicate, by March 2026, on the most appropriate action. The Commission will also continue its preparatory work on other animal welfare proposals, as announced in the Farm to Fork Strategy.",
                "The Commission has also proposed accompanying actions in the field of 'One Health' preventive mechanisms, invasive alien species and labelling of fur in apparel and clothing accessories.",
                "The Commission published the response to this initiative on 7 December 2023 in the form of [a Communication](https://citizens-initiative.europa.eu/initiatives/details/2022/000002_en) , setting out the Commission's legal and political conclusions on the initiative and the actions it intended to take as a response.",
                "The Commission's actions will concern:",
                "The welfare of animals kept for fur production; The [One health dimension;](https://health.ec.europa.eu/one-health_en) the environmental aspects linked to Invasive alien species; and labelling aspects related to the animals kept for fur production.",
                "The European Commission also mandated the European Food Safety Authority (EFSA) to give an independent view on the protection of animals kept for fur production. [The mandate](https://open.efsa.europa.eu/questions/EFSA-Q-2023-00869) requested EFSA to deliver, one technical report, in accordance with Article 31 of [Regulation (EC) No 178/2002](https://eur-lex.europa.eu/eli/reg/2002/178/oj) and a scientific opinion in accordance with Article 29 of Regulation (EC) No 178/2002 for mink, foxes, raccoon dogs and chinchillas.\xa0EFSA published the [scientific opinion on the welfare of animals kept for fur production](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2025.9519) scientific opinion on the welfare of animals kept for fur production on 30 July 2025.",
            ],
            None,
        ),
        (
            True,
            "2024/000004",
            [
                "Main conclusions of the [Communication](https://ec.europa.eu/transparency/documents-register/detail?ref=C(2026)3225&lang=en) .",
                "Having carefully analysed the initiative and with regard to the EU Treaties' limitations to EU competence in the area of public health, the Commission underlines that Member States can rely on existing EU instruments to improve equal access to legally available and affordable healthcare services, including safe abortion services.",
                "This EU support can be provided through the [European Social Fund Plus](https://european-social-fund-plus.ec.europa.eu/en) (ESF+) programme, in case Member States wish, voluntarily and in accordance with their national laws, to provide such support, notably by using or reallocating available resources under their ESF+ programmes. The ESF+ could be used to enhance access to legally available, affordable and safe abortion services for pregnant women. The ESF+ can support the efforts of these Member States, while granting them autonomy to determine how and under what conditions access to safe and legal abortion will be provided.",
                "As EU support can already be provided relatively quickly by Member States willing to do so under existing instruments, it is not necessary to propose a new legal instrument.",
            ],
            ["not necessary to propose a new legal instrument"],
        ),
    ]


@pytest.fixture
def followup_events_law_passed() -> list[tuple[bool, str, list[str]]]:
    """
    A pytest fixture providing mock test data for evaluating the extraction of
    passed, adopted, or active legislation from the follow-up events of European
    Citizens' Initiatives (ECIs).

    Returns:
        list[tuple[str, list[str] | None, list[str] | None]]: A list of test cases containing:

            - str: The ECI registration number (e.g., '2012/000003').

            - list[str] | None: The expected output list of specific sentences indicating that a
                                law, directive, or regulation was passed, adopted, or entered into force.
                                Returns None if no such events occurred.

            - list[str] | None: The raw input list of follow-up event strings detailing the Commission's
                                implementation steps. Returns None if there is no follow-up data.
    """
    return [
        (
            "2012/000003",
            [
                # "As a first step following the European Citizens' Initiative Right2Water, an amendment to the Drinking Water Directive aimed at improving the monitoring of drinking water across Europe came into force on 28 October 2015 (see press release).",
                "As a first step following the European Citizens' Initiative Right2Water, an amendment to the [Drinking Water Directive](http://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv:OJ.L_.2015.260.01.0006.01.ENG) aimed at improving the monitoring of drinking water across Europe came into force on 28 October 2015 (see [press release](http://europa.eu/rapid/press-release_IP-15-5940_en.htm) ).",
                # "On 16 December 2020, the European Parliament formally adopted the revised Drinking Water Directive",
                "[On 16 December 2020](https://ec.europa.eu/commission/presscorner/detail/en/ip_20_2417) , the European Parliament formally adopted [the revised Drinking Water Directive](http://data.europa.eu/eli/dir/2020/2184/oj)",
                "The Regulation based on this proposal entered into force in June 2020",
                # "In January 2024, the Commission adopted new minimum hygiene standards",  # Non direct law mention exception
                "In January 2024, the Commission adopted [new minimum hygiene standards](https://environment.ec.europa.eu/publications/delegated-acts-drinking-water-directive_en)",
            ],
            [
                "As a first step following the European Citizens' Initiative Right2Water, an amendment to the [Drinking Water Directive](http://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv:OJ.L_.2015.260.01.0006.01.ENG) aimed at improving the monitoring of drinking water across Europe came into force on 28 October 2015 (see [press release](http://europa.eu/rapid/press-release_IP-15-5940_en.htm) ).",
                "[A proposal for the revision of the Directive on drinking water](http://ec.europa.eu/environment/water/water-drink/pdf/revised_drinking_water_directive.pdf) A proposal for the revision of the Directive on drinking water was adopted by the Commission on 01 February 2018. This proposal, in reaction to the initiative, foresees inter alia an obligation for Member States to improve access to water and ensure access for vulnerable and marginalised groups (see [press release](http://europa.eu/rapid/press-release_IP-18-429_en.htm) ).The proposal builds upon the [evaluation of the Drinking Water Directive](http://ec.europa.eu/environment/water/water-drink/review_en.html) carried out in 2016 and the [public consultation](https://ec.europa.eu/environment/consultations/water_drink_en.htm) on the Quality of Drinking Water in the EU carried out in 2014. [On 16 December 2020](https://ec.europa.eu/commission/presscorner/detail/en/ip_20_2417) , the European Parliament formally adopted [the revised Drinking Water Directive](http://data.europa.eu/eli/dir/2020/2184/oj) . The Directive entered into force on 12 January 2021. Member States had until 12 January 2023 to transpose it into national legislation.",
                "A [proposal for a regulation on minimum requirements for water reuse](https://ec.europa.eu/environment/water/pdf/water_reuse_regulation.pdf) was adopted by the Commission in May 2018. The proposed rules aim at stimulating and facilitating water reuse in the EU for agricultural irrigation. The Regulation based on this proposal entered into force in June 2020. The new rules apply from 26 June 2023. Further information on this initiative can be found on the [dedicated Commission website](http://ec.europa.eu/environment/water/reuse.htm) .",
                "In January 2024, the Commission adopted [new minimum hygiene standards](https://environment.ec.europa.eu/publications/delegated-acts-drinking-water-directive_en) new minimum hygiene standards for materials and products that come into contact with drinking water . They will apply as of 31 December 2026 to materials and products used in new installations, or when older installations are renovated or repaired. These hygiene standards are an important milestone in the implementation of the recast Drinking Water Directive Therefore, their implementation also responds to the 'Right2Water' initiative.",
                "Further information on rules on drinking water can be found on the [dedicated Commission website.](http://ec.europa.eu/environment/water/water-drink/index_en.html)",
                "Subsequent implementation reports on the Water Framework Directive and Floods Directive were published in 2015, 2019 and 2021. For further information, see the [dedicated website](https://ec.europa.eu/environment/water/water-framework/impl_reports.htm) .",
                "The Commission prepares a [review of the Water Framework Directive](https://ec.europa.eu/environment/water/fitness_check_of_the_eu_water_legislation/index_en.htm) review of the Water Framework Directive in line with the requirements of Article 19(2) of the Directive.",
                '[The European Pillar of Social Rights](https://ec.europa.eu/commission/priorities/deeper-and-fairer-economic-and-monetary-union/european-pillar-social-rights/european-pillar-social-rights-20-principles_en) The European Pillar of Social Rights proclaimed by the European Parliament, the Council and the Commission on 17/11/2017 foresees an explicit reference to the right of citizens to water and sanitation under principle 20 – "Access to essential services" .',
                "Stakeholder meetings on benchmarking of water quality and services took place on 09/09/2014 and 12/10/2015 in Brussels. This stakeholder dialogue is one of the actions announced in the [Communication](http://ec.citizens-initiative.europa.eu/public/initiatives/finalised/answered) and aims to increase transparency on performance of water and sanitation services. All related documents can be found in the [repository](https://circabc.europa.eu/ui/group/65764c73-4a57-45dc-8199-473014cf65bf/library/dde40439-9af7-47b8-9751-006b136e681b) .",
                'The Commission identified \'water and sanitation \' as a key priority area for the post-2015 development framework in its Communication ["A Decent life for all : from vision to collective action"](http://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:52014DC0335) (COM(2014) 335) adopted on 02/06/2014. The EU efforts have substantially contributed to maintaining the universal access to water and sanitation in the list of [Sustainable Development Goals](https://sustainabledevelopment.un.org/post2015/transformingourworld) Sustainable Development Goals in the "2030 Agenda for Sustainable Development" (Goal 6: Ensure availability and sustainable management of water and sanitation for all), adopted by the UN General Assembly on 25/09/2015.',
                'The European Commission is also working with different partners to stimulate innovative approaches for development assistance(e.g. support to partnerships between water operators and to public-public partnerships), promote sharing of best practices between Member States (e.g. on solidarity instruments) and identify new opportunities for cooperation. This dialogue is taking place in dedicated workshops and international fora. Euro paid has organised a workshop on "Innovative partnerships and financing mechanisms" as ways to promote access to drinking water and sanitation in developing countries. This event also aimed to explore the potential role of EU actors and institutions in encouraging water cooperation and the sharing of best practices. Commissioner Mimica also highlighted the EU commitment on this issue during the Thematic session on "Innovative financing for small and decentralized water and sanitation operators and actors" at the 7th World Water Forum in South Korea.',
                "The European Parliament adopted an [own-initiative report](http://www.europarl.europa.eu/sides/getDoc.do?pubRef=-//EP//NONSGML+TA+P8-TA-2015-0294+0+DOC+PDF+V0//EN) on the follow up to the European citizens' initiative Right2Water on 08/09/2015.",
                "At its plenary session meeting on 15/10/2014, the European Economic and Social Committee adopted its [opinion](https://webapi2016.EESC.europa.eu/v1/documents/eesc-2014-02361-00-01-ac-tra-en.doc/content) on the Commission's Communication in reply to the Right2Water initiative.",
            ],
        ),
        (
            "2012/000005",
            None,
            [
                "In the Communication adopted on 28/05/2014, the Commission explains that it has decided not to submit a legislative proposal, given that Member States and the European Parliament had only recently discussed and decided EU policy in this regard. The Commission has concluded that the existing funding framework, which had been recently debated and agreed by EU Member States and the European Parliament, is the appropriate one. See [press release](http://europa.eu/rapid/press-release_IP-14-608_en.htm) ."
            ],
        ),
        (
            "2017/000002",
            [
                # "A proposal for a Regulation of the European Parliament and the Council on the transparency and sustainability of the EU risk assessment in the food chain was adopted by the Commission on 11 April 2018 in response to the second aim of the initiative (see above).",
                "[A proposal for a Regulation of the European Parliament and the Council on the transparency and sustainability of the EU risk assessment in the food chain](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52018PC0179&qid=1616683628859) was adopted by the Commission on 11 April 2018 in response to the second aim of the initiative (see above).",
                "Following the agreement of the European Parliament and the Council, the [Regulation of the European Parliament and the Council](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32019R1381) of the European Parliament and the Council was published in the Official Journal of the EU on 6 September 2019.",
                # False-positive:
                #
                # "The new Regulation sets out objectives and general principles of risk communication.
                # In the coming years, the Commission, in close cooperation with the Member States and with the European Food Safety Authority,
                # will adopt a general plan for risk communication to ensure a coherent risk communication strategy throughout the risk analysis process,
                #  combined with open dialogue amongst all interested parties."
                #
                # "Developing comprehensive risk communication :
                # The new Regulation sets out objectives and general principles of risk communication.
                # In the coming years, the Commission, in close cooperation with the Member States and with the European Food Safety Authority,
                # will adopt a general plan for risk communication to ensure a coherent risk communication strategy throughout
                # the risk analysis process, combined with open dialogue amongst all interested parties."
            ],
            [
                "[A proposal for a Regulation of the European Parliament and the Council on the transparency and sustainability of the EU risk assessment in the food chain](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52018PC0179&qid=1616683628859) was adopted by the Commission on 11 April 2018 in response to the second aim of the initiative (see above).",
                "To address citizens' concerns and drawing also on the Commission's [Fitness Check of the General Food Law](https://ec.europa.eu/food/safety/general_food_law/fitness_check_en) , the proposal was a targeted amendment of the [General Food Law Regulation](http://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32002R0178) and – as far as transparency and confidentiality aspects were concerned – of eight other sectoral legislative acts.",
                "While the citizens’ initiative was focusing only on the area of plant protection products, the Regulation, based on the Commission’s proposal, covered the entire food chain and all regulated products in the food chain.",
                "Following the agreement of the European Parliament and the Council, the [Regulation of the European Parliament and the Council](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32019R1381) of the European Parliament and the Council was published in the Official Journal of the EU on 6 September 2019. Following its entry into force 20 days after publication, it became applicable 18 months later, i.e. on 27 March 2021 .",
                "Ensuring more transparency: Citizens will have automatic access to all studies and information submitted by industry in the risk assessment process. Stakeholders and the general public will also be consulted on submitted studies. At the same time, the Regulation will guarantee confidentiality, in duly justified circumstances, by setting out the type of information that may be considered significantly harmful for commercial interests and therefore cannot be disclosed.",
                "Increasing the independence of studies : The [European Food Safety Authority](http://www.efsa.europa.eu/) will be notified of all commissioned studies to guarantee that companies applying for authorisations submit all relevant information and do not hold back unfavourable studies. The Authority will also provide general advice to applicants, in particular SMEs, prior to the submission of the dossier. The Commission may ask the Authority to commission additional studies for verification purposes and will perform fact-finding missions to verify the compliance of laboratories/studies with applicable standards between March 2021 and March 2025.",
                "Strengthening the governance and the scientific cooperation: Member States, civil society and the European Parliament will be involved in the governance of the European Food Safety Authority by being duly represented in its Management Board. Member States will foster the Authority's scientific capacity and engage the best independent experts into its work.",
                "Developing comprehensive risk communication : The new Regulation sets out objectives and general principles of risk communication. In the coming years, the Commission, in close cooperation with the Member States and with the [European Food Safety Authority](http://www.efsa.europa.eu/) , will adopt a general plan for risk communication to ensure a coherent risk communication strategy throughout the risk analysis process, combined with open dialogue amongst all interested parties.",
                "The Commission and EFSA are working closely to ensure the proper implementation of the new Regulation.",
                "Further information can be found [on the dedicated Commission website](https://ec.europa.eu/food/safety/general_food_law/transparency-and-sustainability-eu-risk-assessment-food-chain_en) .",
                "Pesticides reduction: a key priority for the Farm to Fork Strategy",
                "The [Farm to Fork Strategy](https://food.ec.europa.eu/horizontal-topics/farm-fork-strategy_en) , published in May 2020, sets ambitious targets for pesticides, notably a reduction by 50% of the use and risk of chemical and most hazardous pesticides .",
                "For up-to-date information on the developments in the field of sustainable use of pesticides and harmonised risk indicators, see the [dedicated Commission website](https://food.ec.europa.eu/plants/pesticides/sustainable-use-pesticides_en) .",
            ],
        ),
        (
            "2012/000007",
            None,
            [
                "The Commission adopted a Communication on 03 June 2015 setting out the actions it intended to take in response to the initiative [Stop Vivisection](http://ec.citizens-initiative.europa.eu/public/initiatives/successful/details/2012/000007) . See [press release](http://europa.eu/rapid/press-release_IP-15-5094_en.htm) .",
                "The European Commission organised a scientific conference in Brussels on 6-7 December 2016 to engage the scientific community and relevant stakeholders in a debate on how to exploit cutting edge advances in biomedical and other research in the development of scientifically valid non-animal approaches (alternatives to animal testing).",
                "On the occasion of the conference, the Commission reported on the progress made in implementing the follow-up actions to the initiative Stop Vivisection. See the [conference report](http://ec.europa.eu/environment/chemicals/lab_animals/3r/pdf/scientific_conference/non_animal_approaches_conference_report.pdf) (point 5, pp. 16-20).",
                "[The Commission published a]() [review report](https://eur-lex.europa.eu/legal-content/EN/TXT/?qid=1510219889073&uri=COM:2017:631:FIN) of the Directive 2010/63/EU in 2017. In addition, it published a [report on implementation](https://eur-lex.europa.eu/legal-content/EN/TXT/?qid=1581689520921&uri=CELEX:52020DC0015) of this Directive in February 2020. These reports provided the first assessments of the extent to which the Directive is reaching its objectives and is implemented by the Member States.",
                "Further information can be found on the [dedicated Commission website](http://ec.europa.eu/environment/chemicals/lab_animals/index_en.htm) .",
                "On 18 April 2017, the European Ombudsman issued a [decision](https://www.ombudsman.europa.eu/en/cases/decision.faces/en/78182/html.bookmark) concerning the initiative 'Stop Vivisection'. The Ombudsman concluded that there was no maladministration by the Commission.",
            ],
        ),
        (
            "2017/000004",
            None,
            [
                "The Commission implements funding programmes in the areas of culture and education (notably Erasmus+) which are fully accessible for small regional or minority language communities. Several examples of projects promoting regional and minorities languages funded by the Erasmus+ and Creative Europe programmes can be found in the [2024 publication ‘Linguistic diversity in the European Union’](https://op.europa.eu/en/publication-detail/-/publication/d325c589-011a-11ef-a251-01aa75ed71a1/language-en) .",
                "As regards rules on EU funding more generally, the Commission has reinforced compliance with the fundamental rights in the EU funds. The Common Provisions Regulation (CPR) setting out rules for the 2021-2027 budget contains an ‘enabling condition’ requiring Member States to ensure compliance with the Charter of Fundamental Rights and the non-discrimination principle when disbursing EU funds covered by the CPR. These will continue to support socio-economic integration including that of marginalised communities, vulnerable groups including ethnic minorities, in line with priorities and needs identified by the Commission and the Member States.",
                "Concerning research opportunities, ‘Horizon Europe’, the current Framework Programme for Research and Innovation (2021-2027), and its implementation programmes offer, in particular under Cluster 2 ‘Culture, creative and inclusive society’, research opportunities in relation to cultural and linguistic diversity in Europe. Research on national minorities or cultural and linguistic diversity may be carried out from different perspectives and using methodologies from different social sciences and humanities. Opportunities for research on linguistic diversity will be continued throughout the entire lifetime of the Horizon Europe programme, i.e. in the work programmes 2025-27.",
                "As regards the initiative’s proposals related to the audiovisual media services, namely to ensure freedom to provide services and the reception of audiovisual content in regions where national minorities reside, the Commission monitors the application of the Audiovisual Media Services Directive (Directive 2010/13/EU, AVMSD) and also the particular application of the rules on the promotion of European works. The [report on the application of the AVMSD Directive](https://digital-strategy.ec.europa.eu/en/library/commission-report-application-audiovisual-media-services-directive) , covering the period 2019-2022, was published in January 2024. It confirms that the AVMSD remains an essential instrument to govern the Union-wide coordination of national legislation for all audiovisual media and that the ‘country-of-origin’ principle has facilitated the cross-border transmission of television channels and video-on-demand (VOD) services. [The report on the application of the rules on the promotion of European works,](https://digital-strategy.ec.europa.eu/en/library/commission-reports-promotion-european-works-audiovisual-media-services-0) covering the period 2020-2021, was published in June 2024. The new rules requiring on-demand services to secure at least 30% share of European works in each of their catalogues have been gradually introduced by Member States, contributing actively to the objective of promoting cultural diversity within the Union.",
                "As regards the initiative's proposals related to geo-blocking, in follow up to the first short-term review of the Geo-blocking Regulation, the Commission organised, in 2021 and 2022, a dialogue with the audiovisual sector to agree on concrete steps to improve the availability of and access to audiovisual content across the EU. The final meeting of the dialogue took place on 6 December 2022. More information can be found in the [event report](https://digital-strategy.ec.europa.eu/en/library/final-meeting-dialogue-access-and-availability-audiovisual-content-across-eu?pk_source=ec_newsroom&pk_medium=email&pk_campaign=dae%20Newsroom) . The Commission presented the outcome of the dialogue in the [2024 stock-taking exercise on the implementation of the Geo-blocking Regulation](https://digital-strategy.ec.europa.eu/en/policies/geoblocking) .",
                "Regarding the promotion of linguistic diversity in the field of regional and minority languages, the Commission is further developing its cooperation on this subject with the Council of Europe’s European Centre for Modern Languages (ECML). Notably, a [colloquium on Strengthening support to regional and minority languages within a plurilingual context](https://www.ecml.at/ECML-Programme/ECML-ECCooperation/Colloquium2023/tabid/5664/language/en-GB/Default.aspx) colloquium on Strengthening support to regional and minority languages within a plurilingual context was co-organised with the ECML in November 2023. Detailed case-studies are being produced, with the aim of building a repository of best practices.",
                "Finally, linguistic diversity in Europe, including regional and minority languages, is promoted in relation to the European Day of Languages or the [European School Education Platform](https://school-education.ec.europa.eu/en) . The 2024 European Day of languages presented and discussed the results of the most recent [Eurobarometer on “Europeans and their languages”](https://europa.eu/eurobarometer/surveys/detail/2979) . One of the results was that 85% of European citizens considered that regional and minority languages should be protected.",
                "Other information",
                "In a [judgement](https://curia.europa.eu/jcms/upload/docs/application/pdf/2022-11/cp220179en.pdf) of 9 November 2022 (case T-158/21), the General Court of the Court of Justice of the European Union dismissed the request of the organisers' group of 'Minority SafePack' to annul the Commission Communication C(2021) 171. The court held that the Commission has not erred in law nor infringed its obligations to state sufficient reasons in its communication, in which the Commission stated that no further legislation was necessary at this stage to achieve the objectives sought by the ECI.",
                "The organisers filed an appeal against this judgment with the Court of Justice on 21 January 2023. The appeal was dismissed by the [Court judgment](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62023CJ0026) of 5 June 2025.",
            ],
        ),
        (
            "2018/000004",
            None,
            [
                "In 2022 and 2023 EFSA published scientific opinions concerning the welfare risks associated with cages for all animal species and categories covered by the ECI (pigs, laying hens, broiler breeders, layer breeders, calves, rabbits, ducks, geese and quail). A public consultation was carried out from 15 October 2021 to 21 January 2022. An impact assessment was initiated, with an inception impact assessment published in July 2021, followed by a series of consultation activities, including in the context of the EU animal welfare platform, and its relevant subgroups.",
                "As part of its 2020 Farm to Fork Strategy, the Commission had already expressed its intention to propose a revision of the animal welfare legislation, including on transport and rearing. This legislation was submitted to a fitness check, concluded in September 2022. Its results were presented in a [Commission Staff Working Document](https://food.ec.europa.eu/document/download/b9cc1000-c978-4895-8e9b-c2e1296adbfe_en?filename=aw_eval_revision_swd_2022-328_en.pdf) Commission Staff Working Document , See [more information on the revision](https://food.ec.europa.eu/animals/animal-welfare/evaluations-and-impact-assessment/revision-animal-welfare-legislation_en) more information on the revision and related developments.",
                "The Commission is carefully assessing important aspects to ensure that the transition to cage-free farming is sustainable for the agricultural sector and for our food systems, including food security. The transition to cage-free systems demands the adaptation of several farming parameters, such as enriching the environment of the animals, and providing them with more space, to secure improved welfare conditions for the animals. Further consultations are needed concerning the costs, the appropriate length of the transitional period and the relevant measures at import. To ensure a proper balance between animal welfare and socio-economic impacts, the phasing out of cages has to come with other animal welfare measures at farm level.",
                "As established by the [Vision for Agriculture and Food](https://agriculture.ec.europa.eu/vision-agriculture-food_en) adopted on 19 February 2025, building on the recommendations of the [Strategic Dialogue on the Future of EU Agriculture](https://agriculture.ec.europa.eu/common-agricultural-policy/cap-overview/main-initiatives-strategic-dialogue-future-eu-agriculture_en) , the Commission is closely exchanging with farmers, the food chain and civil society. On that basis, the Commission will present proposals on the revision of the existing EU animal welfare legislation, including its commitment to phase out cages. The Commission will also pursue, in line with international rules, a stronger alignment of animal welfare standards applied to imported animals and food.",
                "Following the announcement made in the 2025 Vision for Agriculture and Food, the Commission launched an impact assessment for a revision of the EU’s on-farm welfare legislation. Further to the [call for evidence](https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14671-On-farm-animal-welfare-for-certain-animals-modernisation-of-EU-legislation_en) call for evidence launched on 18 June 2025 (and closed on 16 July 2025), on 19 September 2025, the Commission launched a [public consultation](https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14671-On-farm-animal-welfare-for-certain-animals-modernisation-of-EU-legislation/public-consultation_en) public consultation open until 12 December 2025. See the [Commission news](https://ec.europa.eu/commission/presscorner/detail/en/mex_25_2142#:~:text=Commission%20seeks%20input%20for%20revising%20EU%20legislation%20on%20animal%20farm%20welfare) Commission news of 19 September 2025.",
                "For further updates, check the [dedicated web page](https://food.ec.europa.eu/animals/animal-welfare/eci/eci-end-cage-age_en) .",
                "As established by the [Vision for Agriculture and Food](https://agriculture.ec.europa.eu/vision-agriculture-food_en) adopted on 19 February 2025, building on the recommendations of the [Strategic Dialogue on the Future of EU Agriculture](https://agriculture.ec.europa.eu/common-agricultural-policy/cap-overview/main-initiatives-strategic-dialogue-future-eu-agriculture_en) , the Commission will closely exchange with farmers, the food chain and civil society. On that basis, the Commission will present proposals on the revision of the existing EU animal welfare legislation, including its commitment to phase out cages. The Commission will also pursue, in line with international rules, a stronger alignment of animal welfare standards applied to imported animals and food.",
                "This revision will be based on the latest scientific evidence and take into account the socio-economic impact on farmers and the agri-food chain, providing support and appropriate, species-specific transition periods and pathways.",
                "Further to the [call for evidence](https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14671-On-farm-animal-welfare-for-certain-animals-modernisation-of-EU-legislation_en) launched on 18 June 2025 (and closed on 16 July 2025), the Commission published on 19 September 2025 a [public consultation](https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14671-On-farm-animal-welfare-for-certain-animals-modernisation-of-EU-legislation/public-consultation_en) which will run until 12 December 2025. The objective of both initiatives is to seek the views of stakeholders, NGOs and citizens on certain potential policy measures, including on the phasing out of cages, in view of the upcoming [revision of the EU legislation for on-farm animal welfare](/animals/animal-welfare/evaluations-and-impact-assessment/revision-eu-animal-welfare-legislation_en) [.](https://food.ec.europa.eu/animals/animal-welfare/evaluations-and-impact-assessment/revision-eu-animal-welfare-legislation_en)",
                "The Commission will continue to develop supporting measures, such as best practices, guidelines, recommendations and studies, for the promotion of and the transition to non-cage farming. In addition, the Commission will further consider which role animal welfare labelling and public procurement might play in this context.",
                "A pilot project “Best Practice Hens” implemented from 2021 to 2023, aimed to help egg producers meet market demand by providing practical guidance on how to transition to alternative, higher-welfare cage-free systems. Materials developed under this project are published on a [dedicated website](https://bestpracticehens.eu/materials/) dedicated website .",
            ],
        ),
        (
            "2019/000016",
            [
                "Proposal for the Nature Restoration Law: following the agreement of the European Parliament on the text (on 27 February 2024), the Council of the EU adopted the regulation on 17 June 2024. It entered into force on 18 August 2024 (20 days after its publication in the Official Journal of the EU) and became applicable immediately."
            ],
            [
                "On 25 April 2023, Commissioner Virginijus Sinkevičius met with the organisers of 'Save bees and farmers!' to discuss the Commission’s reply to the initiative.",
                "Updates on the Commission's proposals",
                "Proposal for the Nature Restoration Law: following the agreement of the European Parliament on the text (on 27 February 2024), the Council of the EU adopted the regulation on 17 June 2024. It entered into force on 18 August 2024 (20 days after its publication in the Official Journal of the EU) and became applicable immediately.",
                "For up-to-date information on the Nature Restoration Law, see the [dedicated Commission website](https://environment.ec.europa.eu/topics/nature-and-biodiversity/nature-restoration-law_en) dedicated Commission website .",
                "Proposal for Regulation on the Sustainable Use of Plant Protection Products: In view of the rejection by the European Parliament of the proposal in November 2023, and a lack of progress of the discussions in the Council, the Commission decided on 27 March 2024 to [withdraw](https://eur-lex.europa.eu/eli/C/2024/3117/oj) its proposal.",
                "For up-to-date information on the developments in the field of sustainable use of pesticides, see the [dedicated Commission website](https://food.ec.europa.eu/plants/pesticides/sustainable-use-pesticides_en) .",
                "For up-to-date information on the EU Pollinators Initiative, see the [dedicated Commission website](https://environment.ec.europa.eu/topics/nature-and-biodiversity/pollinators_en) .",
            ],
        ),
        (
            "2020/000001",
            [
                "The codes enter in application in January 2025.",
                "This concerns, among others, implementation of the revised EU fisheries control Regulation and the Regulation on illegal, unreported and unregulated fishing (IUU) that entered into force in January 2024 and the implementation of CITES shark listings.",
            ],
            [
                "In the second half of 2023 the European Commission started working on an impact assessment on the environmental, social and economic consequences of applying the “fins naturally attached” policy to the placing on the EU market of sharks, whether within the EU or for international trade (imports and exports).",
                "In 2024, the Commission organised a [call for evidence](https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14158-Better-protecting-sharks-through-sustainable-fishing-and-trade_en) seeking views and expertise on the environmental, social and economic consequences of a potential ban on EU sales and international trade of loose shark fins, as well as other policy options to better protect sharks and related marine ecosystems. The call for evidence was complemented by a public consultation. Its results can be found on the [dedicated page.](https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14158-Better-protecting-sharks-through-sustainable-fishing-and-trade/public-consultation_en) The targeted consultations included also a [public event](https://oceans-and-fisheries.ec.europa.eu/events/better-protecting-sharks-through-sustainable-fishing-and-trade-2024-07-09_en) in Vigo (Spain) on 9 July 2024. The consultations will guide further impact assessment work, including an external study to be carried out over 2025.",
                "Following up on its commitment to develop more detailed EU import and export data to improve statistics on trade in shark products, the Commission created 13 new [tariff codes for sharks and their fins](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32024R2522) tariff codes for sharks and their fins . These codes will enable the tracking of the most traded shark species, including the blue shark and shortfin mako. The codes enter in application in January 2025.",
                "Moreover, the Commission is working towards better enforcement of the existing rules. This concerns, among others, implementation of the revised EU fisheries control Regulation and the Regulation on illegal, unreported and unregulated fishing (IUU) that entered into force in January 2024 and the implementation of CITES shark listings.",
                "More information can be found on the [EU sharks’ protection and management](https://oceans-and-fisheries.ec.europa.eu/ocean/marine-biodiversity/sharks_en) EU sharks’ protection and management page.",
                "At the international level, the Commission is reaching out to international partners with a view to achieve, among others, a worldwide finning ban and a reduction of global shark consumption. Since autumn 2023, the question of finning and shark conservation efforts has been raised with a number of partners, including at the High-Level Dialogue with China, the United States, Japan and Canada, as well as in the context of the Food and Agriculture Organisation (FAO). Moreover, in the context of regional fisheries management organisations (RFMOs), the EU worked closely with the US and other partners at the annual meeting of the International Commission for the Conservation of Atlantic Tunas (ICCAT) in November 2024, to gather a record number of co-sponsors (42 ICCAT contracting parties) for a proposal to adopt a fins-naturally-attached policy. While at this occasion the proposal did not achieve the necessary consensus, the EU will continue to promote the fins-naturally-attached policy in ICCAT and other RFMOs, where the EU fleet reports shark catches, in order to eventually implement a finning ban at regional level.",
            ],
        ),
        (
            "2021/000006",
            None,
            [
                "Follow-up meeting",
                "On 8 November 2023, Commissioner Virginijus Sinkevičius met with the organisers of ‘Save Cruelty Free Cosmetics - Commit to a Europe without Animal Testing' to discuss the Commission’s reply to the initiative.",
                "Launch of work on the roadmap",
                "In the second half of 2023, the Commission started work on a roadmap to phase out animal testing for chemical safety assessments that was announced in its reply to the ECI. Finalisation of the work on the roadmap is planned by early 2026.",
                "See the information on the preparation of the roadmap towards phasing out animal testing on the [dedicated website](https://single-market-economy.ec.europa.eu/sectors/chemicals/reach/roadmap-towards-phasing-out-animal-testing_en) .",
                "See also the information on related [workshops and conferences](https://single-market-economy.ec.europa.eu/sectors/chemicals/reach/roadmap-towards-phasing-out-animal-testing/events-and-outreach-activities_en) , organised since 2023.",
                "The [European Partnership for Alternative Approaches to Animal Testing (EPAA)](https://single-market-economy.ec.europa.eu/sectors/chemicals/european-partnership-alternative-approaches-animal-testing_en) European Partnership for Alternative Approaches to Animal Testing (EPAA) is a partnership between the European Commission and industry that aims to replace animal testing by innovative, non-animal testing methods/New Approach Methodologies (NAMs), to reduce the number of animals used and to refine procedures where no alternatives exist, or are not sufficient to ensure the safety of substances (the '3R principle'). EPAA organised several [conferences and activities](https://single-market-economy.ec.europa.eu/sectors/chemicals/european-partnership-alternative-approaches-animal-testing/activities-and-events_en) , including the EPAA Annual Conferences on 15 November 2023 and 13 November 2024. On 5-6 November 2025, EPAA organised an annual conference to mark the 20th anniversary of its activity.",
                "Alternatives to animal testing in research",
                "The Commission has proposed a European Research Area (ERA) policy action on non-animal approaches for biomedical research and testing of pharmaceuticals. This action was presented during a dedicated workshop within a [conference of the European Research Area](https://european-research-area.ec.europa.eu/european-research-area-stakeholder-conference-2024) on 18-19 September 2024.",
                "The Commission included “alternatives to animal testing” in the [2025-2027 strategic plan of Horizon Europe](https://op.europa.eu/en/web/eu-law-and-publications/publication-detail/-/publication/6abcc8e7-e685-11ee-8b2b-01aa75ed71a1) 2025-2027 strategic plan of Horizon Europe (EU’s research and innovation fund).",
                "A workshop on future priority research areas for new approach methodologies (NAMs) was held at the European Commission (DG Research and Innovation) on 10–11 April 2025. A report from the workshop is expected to be published at later stage.",
                "Judgments of the General Court on the relationship between REACH and the Cosmetic Products Regulation ( [T-655/20](https://curia.europa.eu/juris/document/document.jsf?text=&docid=279983&pageIndex=0&doclang=en&mode=req&dir=&occ=first&part=1&cid=1997743) and [T-656/20](https://curia.europa.eu/juris/document/document.jsf?text=&docid=279984&pageIndex=0&doclang=EN&mode=lst&dir=&occ=first&part=1&cid=4301162) )",
                "As stated in the response to the first objective of the initiative – ‘protect and strengthen the cosmetics animal testing ban’ - the interface between the REACH Regulation and the Cosmetic Products Regulation was at the time being assessed by the Court of Justice of the European Union. The General Court issued its judgments on 22 November 2023 and clarified that the REACH Regulation requires companies that manufacture or import chemical substances that are only used in cosmetic products to provide information (if necessary, generated through animal testing) on hazardous properties for the safety assessment of workers manufacturing or processing these substances.",
                "The Commission will carefully consider the Court’s judgments in view of any potential future measures.",
            ],
        ),
        (
            "2022/000002",
            [
                # "Through an Implementing Regulation adopted on 17 July 2025, American mink (Neovison vison) is now listed under the Invasive Alien Species Regulation. The listing of this species will enter into force in August 2027.",
                "Through an [Implementing Regulation adopted on 17 July 2025](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32025R1422&qid=1753087782491) , American mink (Neovison vison) is now listed under the Invasive Alien Species Regulation."
            ],
            [
                "On 9 February 2024, Commissioner Stella Kyriakides met with the organisers of ‘Fur Free Europe’ to discuss the Commission’s reply to the initiative.",
                "The Commission’s work on the accompanying actions, as announced in the Communication, has been progressing. See the [dedicated website](https://food.ec.europa.eu/animals/animal-welfare/eci/eci-fur-free-europe_en) for details.",
                "The Commission conducted, in 2024, three on-site visits to Member States with mink/fur farms, exploring the controls and the One Health mechanisms in place.",
                "A survey on fur animals, directed at Member States authorities was carried out end of 2024 to help collect factual information and data that would feed into a Commission assessment of economic, social and environmental impacts of the actions mentioned in the Communication. The contributions of 18 Member States authorities were received by the end of February 2025 and will be used in the context of the study supporting the follow-up to the Commission’s Communication.",
                "Through an [Implementing Regulation adopted on 17 July 2025](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32025R1422&qid=1753087782491) , American mink (Neovison vison) is now listed under the Invasive Alien Species Regulation. The listing of this species will enter into force in August 2027.",
                "The Commission launched a review of the Textile Labelling Regulation in August 2023. Among other objectives, the review aims to explore the possibility of an accurate and more detailed labelling of the presence of fur in all apparel and certain related products, notably clothing accessories. Read more on [dedicated webpage](https://single-market-economy.ec.europa.eu/sectors/textiles-ecosystem/regulation-eu-10072011_en) .",
                "On 4 July 2025, the Commission launched a [Call for evidence](https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14669-The-Fur-Free-Europe-initiative-assessment-_en) requesting input from stakeholders and citizens, on the follow-up to be given to the European Citizens’ Initiative “Fur Free Europe”. This Call aims to collect evidence on the economic, social, environmental impacts, animal health, public health and animal welfare impacts of the scenarios outlined in the [Commission’s Communication and suggestions of alternative ways to address the problems identified.](https://citizens-initiative.europa.eu/initiatives/details/2022/000002_en) The Call for evidence runs for four weeks, until 1 August 2025 and the feedback received are publicly available.",
                "Taking into account the EFSA opinion and the outcomes of its own assessment, the Commission will communicate, by March 2026,whether it considers it appropriate to propose a prohibition, after a transition period, on the keeping in farms and killing of farmed mink, foxes, raccoon dogs or chinchilla, whether it is appropriate to propose a prohibition, after a transition period, of the placing on the Union market of fur and fur products derived from such animals originating in fur farms, or alternatively to adopt, through EU legislation, appropriate standards suited to better address the welfare needs of the animals.",
                "Additional information regarding this European Citizens' Initiative are available on the [organisers' website](https://www.eurogroupforanimals.org/fur-free-europe) organisers' website and the [dedicated Commission's webpage.](https://citizens-initiative.europa.eu/fur-free-europe_en)",
            ],
        ),
        ("2024/000004", None, None),
    ]
