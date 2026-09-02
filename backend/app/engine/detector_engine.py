from app.engine.opportunity_engine import (
    build_opportunity_set
)

from app.detectors.recover.payment_degradation import (
    detect_payment_degradation
)

from app.detectors.recover.checkout_dropoff import (
    detect_checkout_dropoff
)

from app.detectors.recover.failed_subscription import (
    detect_failed_subscriptions
)

from app.detectors.recover.receivables import (
    detect_receivables
)

from app.detectors.recover.mandate_retry import (
    detect_mandate_retry
)

from app.detectors.recover.promise_to_pay import (
    detect_promise_to_pay
)

from app.detectors.recover.payment_method import (
    detect_payment_method_risk
)

from app.detectors.prevent.payment_failure import (
    detect_payment_failure_prevention
)

from app.detectors.prevent.churn import (
    detect_churn_risk
)

from app.detectors.grow.cross_sell import (
    detect_cross_sell
)

from app.detectors.grow.expansion import (
    detect_customer_expansion
)


def detect_all_opportunities(df):

    opportunities = []

    detectors = [

        detect_payment_degradation,

        detect_checkout_dropoff,

        detect_failed_subscriptions,

        detect_receivables,

        detect_mandate_retry,

        detect_promise_to_pay,

        detect_payment_method_risk,

        detect_payment_failure_prevention,

        detect_churn_risk,

        detect_cross_sell,

        detect_customer_expansion,
    ]


    for detector in detectors:

        try:

            result = detector(df)

            opportunities.extend(
                result
            )

        except Exception as exc:

            print(
                f"⚠ {detector.__name__}: "
                f"{exc}"
            )


    return build_opportunity_set(
        opportunities,
        max_results=200
    )