# TAX-CALCULATOR

## Description
This is a simple tax calculator that calculates the tax of a given income. The tax is calculated based on the tax brackets for the years: 2019, 2020, 2021 and 2022. The tax brackets for 2022 are as follows:
- 15% on the first $50,197 of income
- 20.5% on income between $50,197 and $100,392
- 26% on income between $100,392 and $155,625
- 29% on income between $155,625 and $221,708
- 33% on income over $221,708

## API Usage
The API has a single endpoint that calculates the tax of a given income. The endpoint is a GET request to /tax-calulator with a query parameter of income and year. The income and year should be a number. By default year is set to 2022 and income is set to 0. The response is a JSON object with the following format:
```bash
curl -X GET "http://localhost:8080/tax-calculator?income=100000&year=2022"
```
```json
{
    "total_taxes_owed": 17739.165,
    "effective_rate": 0.17739165,
    "taxes_owed_per_band": [
        {
            "range": [
                0.0,
                50197.0
            ],
            "rate": 0.15,
            "amount_owed": 7529.549999999999
        },
        {
            "range": [
                50197.0,
                100392.0
            ],
            "rate": 0.205,
            "amount_owed": 10209.615
        }
    ]
}
```

## Check out the API documentation
The API documentation can be found at http://localhost:8080/docs in your browser.

## Contributing
--8<-- "CONTRIBUTING.md"