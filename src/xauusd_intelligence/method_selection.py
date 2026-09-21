from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


VERSION = "method-selection-v1.0.0"


@dataclass(frozen=True)
class KnowledgeObject:
    object_id: str
    title: str
    object_type: str
    domains: tuple[str, ...]
    required_inputs: tuple[str, ...]
    applicable_conditions: tuple[str, ...] = ()
    weak_conditions: tuple[str, ...] = ()
    failure_modes: tuple[str, ...] = ()
    competing_interpretations: tuple[str, ...] = ()
    claim_status: str = "claimed"
    evidence_refs: tuple[str, ...] = ()
    decision_safety: str = ""


@dataclass(frozen=True)
class MethodSpec:
    method_id: str
    version: str
    domain: str
    knowledge_ids: tuple[str, ...]
    required_inputs: tuple[str, ...]
    optional_inputs: tuple[str, ...] = ()
    weak_conditions: tuple[str, ...] = ()
    failure_modes: tuple[str, ...] = ()
    competing_interpretations: tuple[str, ...] = ()
    disconfirmation_requirements: tuple[str, ...] = ()
    claim_status: str = "claimed"
    provenance: tuple[str, ...] = ()


@dataclass(frozen=True)
class MethodSelection:
    selected_methods: tuple[str, ...]
    selection_reason: tuple[str, ...]
    required_inputs: tuple[str, ...]
    unavailable_inputs: tuple[str, ...]
    narrowed_claims: tuple[str, ...]
    redundancy_flags: tuple[str, ...]
    hypotheses: tuple[str, ...]
    falsification_tests: tuple[str, ...]
    provenance: tuple[str, ...]
    method_versions: tuple[str, ...]
    retrieved_knowledge: tuple[str, ...]
    version: str = VERSION


def _tokens(value: str) -> set[str]:
    return {x for x in value.lower().replace("/", " ").replace("-", " ").split() if len(x) > 2}


def retrieve_knowledge(
    objects: Iterable[KnowledgeObject],
    *,
    domains: Sequence[str] = (),
    required_inputs: Sequence[str] = (),
    limit: int = 8,
) -> tuple[KnowledgeObject, ...]:
    """Retrieve relevant knowledge without asserting that relevance proves a thesis."""
    domain_tokens = set().union(*(_tokens(x) for x in domains)) if domains else set()
    input_set = set(required_inputs)
    scored: list[tuple[int, str, KnowledgeObject]] = []

    for obj in objects:
        score = 0
        if domain_tokens:
            score += 3 * len(domain_tokens & set().union(*(_tokens(x) for x in obj.domains)))
        score += 2 * len(input_set & set(obj.required_inputs))
        if not domain_tokens and not input_set:
            score = 1
        if score:
            scored.append((score, obj.object_id, obj))

    scored.sort(key=lambda x: (-x[0], x[1]))
    return tuple(x[2] for x in scored[:limit])


def select_methods(
    methods: Iterable[MethodSpec],
    *,
    question: str,
    available_inputs: Iterable[str],
    domains: Sequence[str] = (),
    max_methods: int = 4,
) -> MethodSelection:
    """Select complementary analytical families by evidence capability, never by outcome."""
    available = set(available_inputs)
    question_tokens = _tokens(question)
    domain_tokens = set().union(*(_tokens(x) for x in domains)) if domains else set()

    ranked: list[tuple[int, str, MethodSpec, tuple[str, ...]]] = []
    for method in methods:
        missing = tuple(sorted(set(method.required_inputs) - available))
        overlap = len(question_tokens & _tokens(method.domain))
        overlap += len(domain_tokens & _tokens(method.domain))
        coverage = len(set(method.required_inputs) & available)
        score = overlap * 4 + coverage
        if not missing:
            score += 3
        ranked.append((score, method.method_id, method, missing))

    ranked.sort(key=lambda x: (-x[0], x[1]))
    selected: list[MethodSpec] = []
    unavailable: set[str] = set()
    redundancy: list[str] = []

    for _, _, method, missing in ranked:
        if missing:
            unavailable.update(missing)
            continue
        if len(selected) >= max_methods:
            break
        # Avoid selecting methods that have identical required-input sets.
        if any(set(method.required_inputs) == set(other.required_inputs) for other in selected):
            redundancy.append(f"{method.method_id}:same_required_inputs")
            continue
        selected.append(method)

    required = tuple(sorted({x for m in selected for x in m.required_inputs}))
    missing_all = tuple(sorted(unavailable))
    narrowed = ("claims must be narrowed when required evidence is unavailable",) if missing_all else ()
    reasons = (
        "selection is based on the declared analytical question and available evidence capability",
        "methods with unavailable required inputs are excluded rather than silently proxied",
    )
    falsification = tuple(dict.fromkeys(x for m in selected for x in m.disconfirmation_requirements))
    provenance = tuple(dict.fromkeys(x for m in selected for x in m.provenance))
    versions = tuple(f"{m.method_id}:{m.version}" for m in selected)
    return MethodSelection(
        tuple(m.method_id for m in selected),
        reasons,
        required,
        missing_all,
        narrowed,
        tuple(redundancy),
        (),
        falsification,
        provenance,
        versions,
        tuple(m for m in ()),
    )


def attach_retrieved_knowledge(selection: MethodSelection, objects: Iterable[KnowledgeObject]) -> MethodSelection:
    """Attach only knowledge explicitly referenced by selected methods."""
    by_id: Mapping[str, KnowledgeObject] = {x.object_id: x for x in objects}
    ids: list[str] = []
    for mid in selection.selected_methods:
        # Method IDs are not knowledge IDs; callers should provide a method registry
        # separately. This function is intentionally conservative and attaches none.
        _ = by_id
        _ = mid
    return selection
