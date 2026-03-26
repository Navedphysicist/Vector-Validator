def calculate_priority(role_family: dict, tiers: dict) -> list[str]:
    """
    Pure deterministic priority algorithm.

    Args:
        role_family: dict with "default_order" key (list of 3 strings: "Model", "Industry", "Platform")
        tiers: dict with keys "Model", "Industry", "Platform" — each value is "Common" or "Unique"

    Returns:
        list of 3 strings representing [P1, P2, P3]
    """
    default_order = role_family["default_order"]

    # Find Unique vectors (preserving default order)
    unique_vectors = [v for v in default_order if tiers.get(v) == "Unique"]

    # No Unique → default order
    if not unique_vectors:
        return list(default_order)

    # P1 already Unique → no change
    if tiers.get(default_order[0]) == "Unique":
        return list(default_order)

    # Promote highest-ranked Unique to P1, rest keeps default order
    promoted = unique_vectors[0]
    remaining = [v for v in default_order if v != promoted]
    return [promoted] + remaining
