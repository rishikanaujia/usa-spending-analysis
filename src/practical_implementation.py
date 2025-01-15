"""
USASpending API Client Implementation

This module provides a client for interacting with the USASpending API
to answer specific questions about federal spending data.
"""

import requests
from typing import Dict, Any, Optional, Tuple


class USASpendingClient:
    """Client for interacting with the USASpending API."""

    BASE_URL = "https://api.usaspending.gov/api/v2"

    def __init__(self):
        """Initialize the API client with a requests session."""
        self.session = requests.Session()

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the API.

        Args:
            endpoint: API endpoint path
            params: Optional query parameters

        Returns:
            JSON response from the API

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _get_agency_code(self, abbreviation: str) -> str:
        """Get agency's toptier code by abbreviation.

        Args:
            abbreviation: Agency abbreviation (e.g., "NASA")

        Returns:
            Agency's toptier code

        Raises:
            ValueError: If agency not found
        """
        data = self._get("references/toptier_agencies/")
        for agency in data['results']:
            if agency['abbreviation'] == abbreviation:
                return agency['toptier_code']
        raise ValueError(f"Agency not found: {abbreviation}")

    def _get_state_fips(self, state: str) -> str:
        """Get state's FIPS code.

        Args:
            state: State name

        Returns:
            State FIPS code

        Raises:
            ValueError: If state not found
        """
        data = self._get("recipient/state/")
        for state_data in data:
            if state_data['name'].lower() == state.lower():
                return state_data['fips']
        raise ValueError(f"State not found: {state}")

    def get_texas_loans_2019(self) -> float:
        """Get average loan amount to Texas in FY 2019.

        Returns:
            Average loan amount
        """
        texas_fips = self._get_state_fips("texas")
        awards = self._get(
            f"recipient/state/awards/{texas_fips}/",
            params={"fiscal_year": 2019}
        )

        loans = next((item for item in awards if item['type'] == 'loans'), None)
        if not loans or loans['count'] == 0:
            return 0.0

        return loans['amount'] / loans['count']

    def get_highest_grant_state_2023(self) -> Tuple[str, float, float, int]:
        """Get state with highest grant value per resident in 2023.

        Returns:
            Tuple containing:
                str: State name
                float: Total grant amount
                float: Amount per resident
                int: State population
        """
        states = [s for s in self._get("recipient/state/") if s['type'] == 'state']

        max_per_capita = 0.0
        result = None

        for state in states:
            # Get state population
            details = self._get(
                f"recipient/state/{state['fips']}",
                params={"year": "2023"}
            )
            if not details.get('population'):
                continue

            # Get grant awards
            awards = self._get(
                f"recipient/state/awards/{state['fips']}/",
                params={"fiscal_year": 2023}
            )
            grants = next((item for item in awards if item['type'] == 'grants'), None)
            if not grants:
                continue

            # Calculate per resident amount
            per_resident = grants['amount'] / details['population']
            if per_resident > max_per_capita:
                max_per_capita = per_resident
                result = (
                    state['name'],
                    grants['amount'],
                    per_resident,
                    details['population']
                )

        return result or ("", 0.0, 0.0, 0)

    def get_nasa_budget_ratio_2024(self) -> Tuple[float, int, float]:
        """Get NASA's budget/awards ratio for FY 2024.

        Returns:
            Tuple containing:
                float: Total budgetary resources
                int: Number of new awards
                float: Ratio (resources per award)
        """
        nasa_code = self._get_agency_code("NASA")

        # Get budgetary resources
        budget = self._get(f"agency/{nasa_code}/budgetary_resources/")
        fy_2024 = next(
            (year for year in budget['agency_data_by_year']
             if year['fiscal_year'] == 2024),
            None
        )
        if not fy_2024:
            raise ValueError("No data for FY 2024")

        resources = fy_2024['total_budgetary_resources']

        # Get new awards count
        awards = self._get(
            f"agency/{nasa_code}/awards/new/count/",
            params={"fiscal_year": 2024}
        )
        count = awards.get('new_award_count', 0)

        ratio = resources / count if count > 0 else 0
        return resources, count, ratio


def main():
    """Run the required queries for the take-home assignment."""
    client = USASpendingClient()

    print("USASpending API Analysis\n")

    print("Calculating Q1: Average loan amount to Texas in FY 2019...")
    avg_loan = client.get_texas_loans_2019()
    print(f"Results for Q1:")
    print(f"${avg_loan:,.2f}\n")

    print("Calculating Q2: Finding state with highest grant value per resident in 2023...")
    state, total, per_resident, pop = client.get_highest_grant_state_2023()
    print(f"Results for Q2:")
    print(f"State: {state}")
    print(f"Population: {pop:,}")
    print(f"Total Grants: ${total:,.2f}")
    print(f"Amount per resident: ${per_resident:,.2f}\n")

    print("Calculating Q3: Determining NASA's budget/awards ratio for FY 2024...")
    resources, awards, ratio = client.get_nasa_budget_ratio_2024()
    print(f"Results for Q3:")
    print(f"Total Budgetary Resources: ${resources:,.2f}")
    print(f"New Awards: {awards:,}")
    print(f"Ratio (Resources per Award): ${ratio:,.2f}")


if __name__ == "__main__":
    main()