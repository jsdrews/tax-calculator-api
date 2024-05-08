import math

import httpx

from app.env import Env
from app.routes.tax_calculator.models import (
    TaxBracketsResponse,
    TestServerErrorResponse,
    TaxBracket,
    MarginalTaxAggregation,
    PerBandCalc,
)


env = Env()


class TestServerError(BaseException):
    pass


def calc_marginal_taxes(
    income: int, brackets: list[TaxBracket]
) -> MarginalTaxAggregation:
    taxes_owed_per_band = []
    total_owed = 0.0
    current = income
    for bracket in reversed(brackets):
        if bracket.min <= current and bracket.max >= current:
            tmp = current - bracket.min
            amount_owed = tmp * bracket.rate
            total_owed += amount_owed
            taxes_owed_per_band.insert(
                0,
                PerBandCalc(
                    range=(
                        [bracket.min]
                        if bracket.max == math.inf
                        else [bracket.min, bracket.max]
                    ),
                    rate=bracket.rate,
                    amount_owed=amount_owed,
                ),
            )
            current = bracket.min

    return MarginalTaxAggregation(
        total_owed=total_owed,
        owed_per_band=taxes_owed_per_band,
    )


def calc_effective_tax_rate(income: int, taxes_owed: float) -> float:
    if income == 0 or taxes_owed == 0:
        return 0.0
    return taxes_owed / income


async def fetch_tax_brackets(year: str, retries: int = 5) -> TaxBracketsResponse:
    async with httpx.AsyncClient() as client:
        url = f"{env.test_server_protocol}://{env.test_server_host}:{env.test_server_port}/tax-calculator/tax-year/{year}"
        current_retries = 0
        error_msg = "Issue communnicating with test server backend"

        # Given a set amount of retries, fetch data from test server
        #  Retries were added to ignore the random errors given back from
        #  the test server. However, if retry reached, send back an error
        while current_retries < retries:
            try:
                timeout = env.test_server_comm_timeout_seconds
                resp = await client.get(url, timeout=timeout)
            except httpx.ReadTimeout as e:
                raise TestServerError(
                    f"{error_msg}: Timeout hit while trying to "
                    f"communicate with the test server: {timeout}s"
                ) from e
            except Exception as e:
                raise TestServerError(f"{error_msg}: {e}") from e
            if resp.status_code < 400:
                break
            current_retries += 1

    # if the resp has a bad status code, send back that error
    if resp.status_code >= 400:
        error_response = TestServerErrorResponse(**resp.json())
        msg = f"{error_msg}: max retries exceeded."
        if error_response.errors:
            msg += f" Message from test server: {error_response.errors[0].message}"
        raise TestServerError(msg)

    # TODO: error handle unexpected response models
    return TaxBracketsResponse(**resp.json())
