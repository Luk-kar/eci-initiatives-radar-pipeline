import pytest

from data_pipeline.merger_csv.responses_followup_legislation.extractor.fields.rejected_legislation import (
    extract,
    check_tabling_law_committed,
)


class TestExtractRejectedLegislationBulk:
    """
    Bulk tests if you forgot to write explicit one
    """

    def test_extract_returns_bool_for_all_samples(
        self,
        commission_answers_rejection_legislation,
    ) -> None:
        """
        Ensure the extractor always returns a strict boolean for every sample.
        """
        for (
            _,
            registration_number,
            text_items,
            _,
        ) in commission_answers_rejection_legislation:

            actual = extract(text_items)

            assert isinstance(actual, bool), (
                f"registration_number={registration_number}: expected bool, got "
                f"{type(actual).__name__}"
            )

    def test_extract_matches_expected_rejected_legislation_flags(
        self,
        commission_answers_rejection_legislation,
    ) -> None:
        """
        Verify that rejected_legislation.extract() matches the expected boolean
        outcome for each commission-answer sample defined in conftest.py.
        """
        for (
            expected,
            registration_number,
            text_items,
            rejection_statement,
        ) in commission_answers_rejection_legislation:

            actual = extract(text_items)

            assert actual is expected, (
                f"registration_number={registration_number}:\n"
                "expected `rejected_legislation`:\n"
                f"  {expected}\n"
                "got:\n"
                f"  {actual}\n"
                "text_item:\n"
                f"  {text_items}"
            )


class TestExtractRejectedLegislationExplicit:
    """
    Individual explicit tests to get visibility on what went wrong.

    Indices map directly to ``commission_answers_rejection_legislation``,
    which is sorted ascending by registration number in conftest.py.
    """

    def _assert_sample(
        self,
        sample: tuple,
        expected_registration: str,
        expected_flag: bool,
        expected_phrases: list[str] | None,
    ) -> None:
        expected, registration_number, text_items, rejection_phrases = sample

        assert registration_number == expected_registration
        assert expected is expected_flag
        assert rejection_phrases == expected_phrases
        assert extract(text_items) is expected_flag

    def test_extract_returns_false_for_2012_000003(
        self, commission_answers_rejection_legislation
    ):
        self._assert_sample(
            commission_answers_rejection_legislation[0],
            "2012/000003",
            expected_flag=False,
            expected_phrases=None,
        )

    def test_extract_returns_true_for_2012_000005(
        self, commission_answers_rejection_legislation
    ):
        self._assert_sample(
            commission_answers_rejection_legislation[1],
            "2012/000005",
            expected_flag=True,
            expected_phrases=["not to submit a legislative proposal"],
        )

    def test_extract_returns_true_for_2012_000007(
        self, commission_answers_rejection_legislation
    ):
        self._assert_sample(
            commission_answers_rejection_legislation[2],
            "2012/000007",
            expected_flag=True,
            expected_phrases=["no repeal of that legislation was proposed"],
        )

    def test_extract_returns_false_for_2017_000002(
        self, commission_answers_rejection_legislation
    ):
        self._assert_sample(
            commission_answers_rejection_legislation[3],
            "2017/000002",
            expected_flag=False,
            expected_phrases=["will not make a legislative proposal to that effect"],
        )

    def test_extract_returns_true_for_2017_000004(
        self, commission_answers_rejection_legislation
    ):
        self._assert_sample(
            commission_answers_rejection_legislation[4],
            "2017/000004",
            expected_flag=True,
            expected_phrases=["no further legal acts are proposed"],
        )

    def test_extract_returns_false_for_2018_000004(
        self, commission_answers_rejection_legislation
    ):
        self._assert_sample(
            commission_answers_rejection_legislation[5],
            "2018/000004",
            expected_flag=False,
            expected_phrases=None,
        )

    def test_extract_returns_true_for_2019_000007(
        self, commission_answers_rejection_legislation
    ):
        self._assert_sample(
            commission_answers_rejection_legislation[6],
            "2019/000007",
            expected_flag=True,
            expected_phrases=["no new legislation will be proposed "],
        )

    def test_extract_returns_false_for_2019_000016(
        self, commission_answers_rejection_legislation
    ):
        self._assert_sample(
            commission_answers_rejection_legislation[7],
            "2019/000016",
            expected_flag=False,
            expected_phrases=None,
        )


class TestCheckTablingLawCommitted:
    """
    Covers every commitment surface form observed in commission_answers_rejection_legislation.
    Each test isolates a single item as skip_item (simulating the rejecting sentence)
    and asserts the OTHER items are recognised as a commitment.
    """

    # ── 2017/000002 ───────────────────────────────────────────────────────────

    def test_committed_to_come_forward_with_legislative_proposal(self) -> None:
        """'committed to come forward with a legislative proposal' — 2017/000002"""
        skip = "will not make a legislative proposal to that effect."
        items = [
            skip,
            (
                "the Commission committed to come forward with a legislative proposal"
                " by May 2018, amongst others, to strengthen the transparency of the"
                " EU risk assessment in the food chain."
            ),
        ]
        assert check_tabling_law_committed(items, skip_item=skip) is True

    # ── 2018/000004 ───────────────────────────────────────────────────────────

    def test_intention_to_table_legislative_proposal(self) -> None:
        """'communicated its intention to table a legislative proposal' — 2018/000004"""
        skip = "some unrelated rejection sentence."
        items = [
            skip,
            (
                "In its response to the ECI, the Commission communicated its intention"
                " to table a legislative proposal, by the end of 2023, to phase out"
                " the use of cages for all animals."
            ),
        ]
        assert check_tabling_law_committed(items, skip_item=skip) is True

    def test_sets_out_plans_for_legislative_proposal(self) -> None:
        """'Commission sets out plans for a legislative proposal' — 2018/000004"""
        skip = "some unrelated rejection sentence."
        items = [
            skip,
            (
                "In its communication the Commission sets out plans for a legislative"
                " proposal to prohibit cages for the species and categories of animals"
                " covered by the ECI."
            ),
        ]
        assert check_tabling_law_committed(items, skip_item=skip) is True

    # ── 2021/000006 ───────────────────────────────────────────────────────────

    def test_will_consider_future_potential_legislative_changes(self) -> None:
        """'will consider … future potential legislative changes' — 2021/000006"""
        skip = "some unrelated rejection sentence."
        items = [
            skip,
            (
                "The Commission will consider the outcome of the court cases in view"
                " of any future potential legislative changes."
            ),
        ]
        assert check_tabling_law_committed(items, skip_item=skip) is True

    # ── Negative cases ────────────────────────────────────────────────────────

    def test_returns_false_when_only_skip_item_present(self) -> None:
        """No other items — nothing to commit from."""

        skip = "the Commission committed to come forward with a legislative proposal."
        assert check_tabling_law_committed([skip], skip_item=skip) is False

    def test_returns_false_when_all_other_items_are_negated(self) -> None:
        """Other item contains a proposal term but is negated — not a commitment."""

        skip = "some unrelated rejection sentence."
        items = [
            skip,
            "The Commission will not submit a legislative proposal at this time.",
        ]
        assert check_tabling_law_committed(items, skip_item=skip) is False

    def test_returns_false_when_no_proposal_term_in_other_items(self) -> None:
        """Other items have no legislative/proposal term at all."""

        skip = "some unrelated rejection sentence."
        items = [
            skip,
            "The Commission will continue to monitor the situation.",
            "Official documents related to the decision:",
        ]
        assert check_tabling_law_committed(items, skip_item=skip) is False

    def test_skip_item_is_not_matched_as_commitment(self) -> None:
        """
        The rejecting sentence itself contains a proposal term (negated).
        skip_item must be excluded even if PROPOSAL_PATTERN would match it
        before the negation guard runs.
        """

        skip = (
            "the Commission decided not to submit a legislative proposal,"
            " given that Member States had only recently agreed EU policy."
        )
        assert check_tabling_law_committed([skip], skip_item=skip) is False
