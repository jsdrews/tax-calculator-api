import pytest
from mock import patch, MagicMock


@pytest.mark.asyncio
@patch("app.routes.tax_calculator.controllers.fetch_tax_brackets")
@patch("app.routes.tax_calculator.controllers.calc_marginal_taxes")
@patch("app.routes.tax_calculator.controllers.calc_effective_tax_rate")
async def test_tax_calculation_route(
    calc_effective_tax_rate_mock, calc_marginal_taxes_mock, fetch_tax_brackets_mock
):
    from fastapi import HTTPException
    from app.routes.tax_calculator.routes import calc_owed_income_tax, TestServerError
    from app.routes.tax_calculator.models import (
        TaxBracketsResponse,
        TaxBracket,
        MarginalTaxAggregation,
        PerBandCalc,
    )
    fetch_tax_brackets_mock.return_value = TaxBracketsResponse(
        tax_brackets = [
            TaxBracket(
                min=0,
                max=50197,
                rate=0.15,
            ),
            TaxBracket(
                min=50197,
                max=100392,
                rate=0.205,
            ),
            TaxBracket(
                min=100392,
                max=155625,
                rate=0.26,
            ),
            TaxBracket(
                min=155625,
                max=221708,
                rate=0.29,
            ),
            TaxBracket(
                min=221708,
                rate=0.33,
            ),
        ]
    )
    calc_marginal_taxes_mock.return_value = MarginalTaxAggregation(
        total_owed=308180.535,
        owed_per_band=[
            PerBandCalc(
                range=[221708.0],
                rate=0.33,
                amount_owed=256836.36000000002,
            ),
            PerBandCalc(
                range=[155625.0, 221708.0],
                rate=0.29,
                amount_owed=19164.07,
            ),
            PerBandCalc(
                range=[100392.0, 155625.0],
                rate=0.26,
                amount_owed=14360.58,
            ),
            PerBandCalc(
                range=[50197.0, 100392.0],
                rate=0.205,
                amount_owed=10289.974999999999,
            ),
            PerBandCalc(
                range=[0.0, 50197.0],
                rate=0.15,
                amount_owed=7529.549999999999,
            ),
        ]
    )
    calc_effective_tax_rate_mock.return_value = 0.308180535

    # Good response
    resp = await calc_owed_income_tax(income=1000000, year=2022)
    assert resp.total_taxes_owed == 308180.535
    assert resp.effective_rate == 0.308180535
    assert len(resp.taxes_owed_per_band) == 5

    # Errors
    # Bad year
    with pytest.raises(HTTPException):
        await calc_owed_income_tax(income=1000000, year=2000)

    # Bad income value
    with pytest.raises(HTTPException):
        await calc_owed_income_tax(income=-1, year=2000)

    # If there is bad communications with the test server
    fetch_tax_brackets_mock.side_effect = TestServerError()
    with pytest.raises(HTTPException):
        await calc_owed_income_tax()


@pytest.mark.asyncio
@patch("app.routes.tax_calculator.controllers.httpx.AsyncClient.get")
async def test_fetch_tax_brackets(httpx_mock):
    import httpx
    from app.routes.tax_calculator.controllers import fetch_tax_brackets, TestServerError
    from app.routes.tax_calculator.models import TaxBracketsResponse
    httpx_mock.return_value = httpx.Response(
        status_code=200,
        json={
            "tax_brackets": [
                {
                    "min": 0,
                    "max": 50197,
                    "rate": 0.15
                },
                {
                    "min": 50197,
                    "max": 100392,
                    "rate": 0.205
                },
                {
                    "min": 100392,
                    "max": 155625,
                    "rate": 0.26
                },
                {
                    "min": 155625,
                    "max": 221708,
                    "rate": 0.29
                },
                {
                    "min": 221708,
                    "rate": 0.33
                }
            ]
        },
        request=httpx.Request("GET", "test"),
    )
    
    # Good request
    resp = await fetch_tax_brackets(2022)
    assert isinstance(resp, TaxBracketsResponse)

    # Bad requests
    # Comms timeout
    httpx_mock.side_effect = httpx.ReadTimeout(message="timedout")
    with pytest.raises(TestServerError):
        resp = await fetch_tax_brackets(2022)

    # 500 error from test server
    httpx_mock.return_value.status_code = 500
    with pytest.raises(TestServerError):
        resp = await fetch_tax_brackets(2022)


def test_calc_marginal_taxes():
    from app.routes.tax_calculator.controllers import calc_marginal_taxes
    from app.routes.tax_calculator.models import TaxBracket

    tax_brackets = [
        TaxBracket(
            min=0,
            max=50197,
            rate=0.15,
        ),
        TaxBracket(
            min=50197,
            max=100392,
            rate=0.205,
        ),
        TaxBracket(
            min=100392,
            max=155625,
            rate=0.26,
        ),
        TaxBracket(
            min=155625,
            max=221708,
            rate=0.29,
        ),
        TaxBracket(
            min=221708,
            rate=0.33,
        ),
    ]

    ret = calc_marginal_taxes(income=1000000, brackets=tax_brackets)
    assert ret.total_owed == 308180.535
    assert len(ret.owed_per_band) == 5

    ret = calc_marginal_taxes(income=-1, brackets=tax_brackets)
    assert ret.total_owed == 0.0
    assert len(ret.owed_per_band) == 0

    ret = calc_marginal_taxes(income=0, brackets=tax_brackets)
    assert ret.total_owed == 0.0
    assert len(ret.owed_per_band) == 1

    ret = calc_marginal_taxes(income=50000, brackets=tax_brackets)
    assert ret.total_owed == 7500.00
    assert len(ret.owed_per_band) == 1

    ret = calc_marginal_taxes(income=100000, brackets=tax_brackets)
    assert ret.total_owed == 17739.165
    assert len(ret.owed_per_band) == 2

    ret = calc_marginal_taxes(income=1234567, brackets=tax_brackets)
    assert ret.total_owed == 385587.645
    assert len(ret.owed_per_band) == 5
