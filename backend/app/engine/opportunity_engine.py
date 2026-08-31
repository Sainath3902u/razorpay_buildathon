from typing import List

from app.engine.opportunity import Opportunity


def deduplicate_opportunities(
    opportunities: List[Opportunity]
) -> List[Opportunity]:

    unique = {}

    for opportunity in opportunities:

        unique[
            opportunity.opportunity_id
        ] = opportunity

    return list(
        unique.values()
    )


def rank_opportunities(
    opportunities: List[Opportunity]
) -> List[Opportunity]:

    return sorted(
        opportunities,
        key=lambda x: x.expected_value,
        reverse=True
    )


def build_opportunity_set(
    opportunities: List[Opportunity],
    max_results: int = 200
):

    opportunities = (
        deduplicate_opportunities(
            opportunities
        )
    )

    opportunities = (
        rank_opportunities(
            opportunities
        )
    )

    return opportunities[
        :max_results
    ]