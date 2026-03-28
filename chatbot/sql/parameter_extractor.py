import re


def extract_parameters(question: str, query_name: str) -> dict:
    q = question.lower().strip()
    params = {}

    if query_name == "revenue_last_n_months":
        match = re.search(r"last\s+(\d+)\s+months?", q)
        if not match:
            raise ValueError("Could not extract the number of months from the question.")
        months = int(match.group(1))

        if months < 1:
            raise ValueError("Number of months must be at least 1.")
        if months > 24:
            raise ValueError("Number of months is too large for this MVP. Try 24 or fewer.")

        # If latest month is October 2025 and user asks for last 3 months,
        # we usually want Aug, Sep, Oct -> subtract 2 months from latest.
        params["months_back"] = months - 1

    elif query_name == "top_k_channels_last_month":
        match = re.search(r"top\s+(\d+)", q)
        if not match:
            raise ValueError("Could not extract the top-K value from the question.")
        top_k = int(match.group(1))

        if top_k < 1:
            raise ValueError("Top-K must be at least 1.")
        if top_k > 20:
            raise ValueError("Top-K is too large for this MVP. Try 20 or fewer.")

        params["top_k"] = top_k

    elif query_name == "top_k_channels_previous_month":
        match = re.search(r"top\s+(\d+)", q)
        if not match:
            raise ValueError("Could not extract the top-K value from the question.")
        top_k = int(match.group(1))

        if top_k < 1:
            raise ValueError("Top-K must be at least 1.")
        if top_k > 20:
            raise ValueError("Top-K is too large for this MVP. Try 20 or fewer.")

        params["top_k"] = top_k

    return params