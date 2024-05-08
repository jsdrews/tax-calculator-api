from fastapi import APIRouter, HTTPException

from app.routes.tax_calculator.models import Response
from app.routes.tax_calculator.controllers import (
    fetch_tax_brackets,
    calc_marginal_taxes,
    calc_effective_tax_rate,
    TestServerError,
)


router = APIRouter(
    prefix="/tax-calculator",
    tags=["tax-calculator"],
)


@router.get(
    "",
    response_model=Response,
)
async def calc_owed_income_tax(
    year: int = 2022,
    income: int = 0,
):
    if income < 0:
        raise HTTPException(status_code=400, detail="Income must be greater than 0")

    supported_years = [2019, 2020, 2021, 2022]
    if year not in supported_years:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Only the following years are supported: {supported_years}. "
                f"Recieved {year}."
            ),
        )

    try:
        tax_brackets = await fetch_tax_brackets(year)
    except TestServerError as e:
        raise HTTPException(status_code=500, detail=str(e))

    marginal_tax_aggregation = calc_marginal_taxes(income, tax_brackets.tax_brackets)
    total_taxes_owed = marginal_tax_aggregation.total_owed
    effective_rate = calc_effective_tax_rate(income, total_taxes_owed)

    return Response(
        total_taxes_owed=total_taxes_owed,
        effective_rate=effective_rate,
        taxes_owed_per_band=marginal_tax_aggregation.owed_per_band,
    )
