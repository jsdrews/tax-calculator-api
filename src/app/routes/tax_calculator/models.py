import math
from typing import List

from pydantic import BaseModel


class TaxBracket(BaseModel):
    """Each tax bracket item returned with the TaxBracketsResponse"""

    max: float = math.inf
    min: float = 0
    rate: float = 0.0


class TaxBracketsResponse(BaseModel):
    """Successful response given back to the API from the test server"""

    tax_brackets: List[TaxBracket]


class TestServerError(BaseModel):
    """Error item include in the errors list of the TestServerErrorResponse"""

    code: str
    message: str
    field: str


class TestServerErrorResponse(BaseModel):
    """Error response given back from the test server"""

    errors: List[TestServerError]


class PerBandCalc(BaseModel):
    """The amount owed at a given tax bracket"""

    range: List[float]
    rate: float
    amount_owed: float


class MarginalTaxAggregation(BaseModel):
    """The summation tax owed from all brackets and the individual amounts owed at each bracket"""

    total_owed: float
    owed_per_band: List[PerBandCalc]


class Response(BaseModel):
    """Response sent back from the API on a successful request"""

    total_taxes_owed: float
    effective_rate: float
    taxes_owed_per_band: List[PerBandCalc]
