from datetime import date

import httpx

from backend.config import settings


class MLAPIError(Exception):
    pass


async def fetch_health_prediction(
    *,
    date_of_birth: date,
    glucose: float,
    haemoglobin: float,
    cholesterol: float,
) -> str:
    payload = {
        "date_of_birth": date_of_birth.isoformat(),
        "glucose": glucose,
        "haemoglobin": haemoglobin,
        "cholesterol": cholesterol,
    }

    url = f"{settings.ml_api_url.rstrip('/')}/predict"

    try:
        async with httpx.AsyncClient(
            timeout=settings.ml_api_timeout_seconds
        ) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError as exc:
        raise MLAPIError(
            "Unable to reach the health prediction API. "
            "Ensure the ML API service is running."
        ) from exc

    remarks = data.get("remarks")
    if not remarks:
        raise MLAPIError("Health prediction API returned an invalid response.")

    return str(remarks)
