"""
Psychonauts 2 Archipelago - Access Rules

This module translates the Item_Required strings from the check CSV into
Archipelago access-rule functions (``CollectionState → bool``).

Requirement string grammar (informal):
  - Comma-separated tokens are ANDed together.
  - A token containing " or " is an OR between two alternatives.
  - A token that starts with "or " (preceded by a comma in the original CSV)
    is an OR alternative that is merged with the *previous* token.
  - "All_ScavHunt_Items" expands to requiring all 16 scavenger-hunt items.
  - "NULL" or empty string means no requirement.

Item-key normalisation:
  - Progressive-group CSV keys are mapped to their progressive display names
    (e.g. "MentalConnection_Upgrade3" → "Progressive Mental Connection" count 4)

Progressive ability / equipment rules:
  For progressive items the rule checks ``state.has(name, player, count)``
  where count is derived from the item's position in ALL_PROGRESSIVE_GROUPS:
    first key in group  → count 1
    second key in group → count 2
    …and so on.
"""

from typing import Callable, Dict, List, Optional, Tuple, TYPE_CHECKING
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from BaseClasses import CollectionState, MultiWorld
    from . import Psy2World

from .items import (
    ALL_PROGRESSIVE_GROUPS,
    SCAV_HUNT_DISPLAY_NAMES,
    WIN_CONDITION_REQUIRED_ITEMS,
    csv_key_to_display_name,
)
from .locations import REGION_ACCESS_ITEM, victory_location
from .options import WIN_COND_TO_COL

# ---------------------------------------------------------------------------
# Progressive-item count table
# ---------------------------------------------------------------------------

# Derive (progressive_name, count) for each CSV key from ALL_PROGRESSIVE_GROUPS.
# Counts are assigned in insertion order: the first key in a group gets count 1,
# the second gets count 2, etc.  This mirrors the hand-coded table it replaces
# without duplicating the group definitions.
def _build_progressive_counts() -> Dict[str, Tuple[str, int]]:
    group_counters: Dict[str, int] = {}
    result: Dict[str, Tuple[str, int]] = {}
    for key, group_name in ALL_PROGRESSIVE_GROUPS.items():
        group_counters[group_name] = group_counters.get(group_name, 0) + 1
        result[key] = (group_name, group_counters[group_name])
    return result

_PROGRESSIVE_COUNTS: Dict[str, Tuple[str, int]] = _build_progressive_counts()


# ---------------------------------------------------------------------------
# Single-token rule builder
# ---------------------------------------------------------------------------

CollectionRule = Callable[["CollectionState"], bool]


def _rule_for_key(key: str, player: int) -> CollectionRule:
    """
    Return a CollectionRule for a single item key.

    Handles progressive items (by count), the All_ScavHunt_Items macro, and
    plain items.
    """
    # ── Scavenger-hunt macro ─────────────────────────────────────────────────
    if key == "All_ScavHunt_Items":
        # Require all 16 scavenger-hunt collectibles.
        items = list(SCAV_HUNT_DISPLAY_NAMES)
        return lambda state, items=items, p=player: all(
            state.has(name, p) for name in items
        )

    # ── Progressive item ─────────────────────────────────────────────────────
    if key in _PROGRESSIVE_COUNTS:
        prog_name, count = _PROGRESSIVE_COUNTS[key]
        return lambda state, n=prog_name, c=count, p=player: state.has(n, p, c)

    # ── Plain item ───────────────────────────────────────────────────────────
    # Use the display name from the item table when available; otherwise use
    # the raw key (which may correspond to an Important item whose display name
    # equals the key, e.g. "Motherlobe_Access").
    display = csv_key_to_display_name.get(key, key)
    return lambda state, name=display, p=player: state.has(name, p)


# ---------------------------------------------------------------------------
# Requirement-string parser
# ---------------------------------------------------------------------------

def _parse_token(token: str, player: int) -> CollectionRule:
    """
    Parse a single comma-separated token and return a CollectionRule.

    Tokens may contain " or " to express alternatives between plain keys or
    compound "A and B" expressions.  Example:
        "TimeBubble or Levitation"
        "TimeBubble or Levitation and Levitation_Upgrade2"
    """
    token = token.strip()

    if " or " not in token:
        return _rule_for_key(token, player)

    # Build one rule per OR branch.
    branches: List[CollectionRule] = []
    for branch in token.split(" or "):
        branch = branch.strip()
        if " and " in branch:
            # Compound AND within an OR branch
            sub_rules = [_rule_for_key(k.strip(), player) for k in branch.split(" and ")]
            rule: CollectionRule = lambda state, sr=sub_rules: all(r(state) for r in sr)
        else:
            rule = _rule_for_key(branch, player)
        branches.append(rule)

    return lambda state, br=branches: any(r(state) for r in br)


def make_rule(requirement_str: str, player: int) -> Optional[CollectionRule]:
    """
    Convert an Item_Required string from the check CSV into a CollectionRule.

    Returns None when there is no requirement (NULL or empty string), which
    the caller can treat as "always accessible".

    Comma-separated tokens are ANDed together.  A token that begins with
    "or " is merged into the *previous* token as an additional OR branch
    (the CSV sometimes encodes complex OR/AND expressions this way):

        "TimeBubble, or Levitation and Levitation_Upgrade2, Cassie_Access"
        →  (TimeBubble OR (Levitation AND Levitation_Upgrade2)) AND Cassie_Access
    """
    if not requirement_str or requirement_str.upper() == "NULL":
        return None

    # Split by comma, then handle the "or X" continuation syntax.
    raw_tokens = [t.strip() for t in requirement_str.split(",")]

    # Merge "or …" continuations into the preceding token so they end up in
    # the same OR expression.
    merged: List[str] = []
    for token in raw_tokens:
        if token.startswith("or ") and merged:
            merged[-1] = merged[-1] + " or " + token[3:]
        else:
            merged.append(token)

    # Build a list of sub-rules that must ALL be satisfied (AND semantics).
    rules: List[CollectionRule] = [_parse_token(t, player) for t in merged if t]

    if not rules:
        return None
    if len(rules) == 1:
        return rules[0]
    return lambda state, rs=rules: all(r(state) for r in rs)


# ---------------------------------------------------------------------------
# Apply rules to the world
# ---------------------------------------------------------------------------

def set_rules(world: "Psy2World") -> None:
    """
    Assign access rules to every randomised location in the world.

    Each location's rule is derived from its Item_Required field in the CSV.
    Region-entry rules (area-access items) are set separately in __init__.py;
    the rule set here therefore strips the area-access token and only adds the
    *remaining* requirements as a location-level rule.

    The Maligula victory location's rule is also set here because it depends
    on the player's chosen win condition.
    """
    multiworld: "MultiWorld" = world.multiworld
    player: int = world.player

    # ── Per-location rules ───────────────────────────────────────────────────
    for loc_data in world.all_location_data:
        req_str = loc_data.requirements

        # Strip the area-access key from the requirement string so it is not
        # double-checked (the region entrance already handles it).
        area_access = REGION_ACCESS_ITEM.get(loc_data.region)
        if area_access and req_str:
            # Remove the area-access token (and any leading/trailing commas)
            tokens = [t.strip() for t in req_str.split(",") if t.strip() != area_access]
            req_str = ", ".join(tokens)

        rule = make_rule(req_str, player)
        if rule is not None:
            location = multiworld.get_location(loc_data.name, player)
            set_rule(location, rule)

    # ── Victory location rule (Maligula fight) ───────────────────────────────
    _set_victory_rule(world, player)


def _set_victory_rule(world: "Psy2World", player: int) -> None:
    """
    Set the access rule for the Maligula fight (victory) event location.

    The rule combines:
      1. GNG_Access (the fight always takes place in Green Needle Gulch).
      2. All items required by the player's chosen win condition.
    """
    col = WIN_COND_TO_COL.get(world.options.win_condition.value, "WinCondition_Normal")
    required_display_names: List[str] = WIN_CONDITION_REQUIRED_ITEMS.get(col, [])

    # Build a list of individual has() checks.
    gng_display = csv_key_to_display_name.get("GNG_Access", "GNG_Access")
    required_items: List[str] = [gng_display] + [
        n for n in required_display_names if n != gng_display
    ]

    checks: List[CollectionRule] = [
        lambda state, n=display, p=player: state.has(n, p)
        for display in required_items
    ]

    if checks:
        combined: CollectionRule = lambda state, cs=checks: all(c(state) for c in cs)
        victory_loc = world.multiworld.get_location(
            victory_location.name, player
        )
        set_rule(victory_loc, combined)
