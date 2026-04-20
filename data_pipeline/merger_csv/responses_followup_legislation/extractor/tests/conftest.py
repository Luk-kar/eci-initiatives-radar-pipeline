import pytest


@pytest.fixture
def commission_answers_rejection_legislation() -> list[tuple[bool, str, list[str]]]:
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
            ],  # It is canceled by proposition of other legislation
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
            ["no repeal of that legislation was proposed"],
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
