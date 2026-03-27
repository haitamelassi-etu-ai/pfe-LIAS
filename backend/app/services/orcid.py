from typing import Any

import httpx

from app.core.config import settings


def _safe_extract_title(work: dict[str, Any]) -> str:
    title = work.get("title", {})
    title_value = title.get("title", {})
    return title_value.get("value") or "Untitled"


def _safe_extract_year(work: dict[str, Any]) -> int | None:
    publication_date = work.get("publication-date", {})
    year = publication_date.get("year", {})
    if isinstance(year, dict) and year.get("value"):
        try:
            return int(year["value"])
        except ValueError:
            return None
    return None


def _safe_extract_doi(work: dict[str, Any]) -> str | None:
    ext_ids = work.get("external-ids", {}).get("external-id", [])
    for ext_id in ext_ids:
        if str(ext_id.get("external-id-type", "")).lower() == "doi":
            return ext_id.get("external-id-value")
    return None


async def fetch_orcid_works(orcid_id: str) -> list[dict[str, Any]]:
    headers = {"Accept": "application/json"}
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(
            f"{settings.orcid_api_base}/{orcid_id}/works", headers=headers
        )
        response.raise_for_status()
        payload = response.json()

    groups = payload.get("group", [])
    results: list[dict[str, Any]] = []
    for group in groups:
        summaries = group.get("work-summary", [])
        if not summaries:
            continue
        work = summaries[0]
        results.append(
            {
                "title": _safe_extract_title(work),
                "year": _safe_extract_year(work),
                "doi": _safe_extract_doi(work),
                "type": work.get("type", "journal-article").lower(),
            }
        )
    return results
