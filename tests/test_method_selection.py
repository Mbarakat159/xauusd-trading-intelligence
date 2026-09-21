from xauusd_intelligence.method_selection import (
    KnowledgeObject,
    MethodSpec,
    select_methods,
    retrieve_knowledge,
)


def test_missing_required_input_excludes_method_and_preserves_missing():
    methods = (
        MethodSpec("structure", "1", "structure", ("K006",), ("F008",)),
        MethodSpec("flow", "1", "order flow", ("K005",), ("DIRECT_DEPTH",)),
    )
    selected = select_methods(
        methods,
        question="structure",
        available_inputs=("F008",),
    )
    assert selected.selected_methods == ("structure",)
    assert "DIRECT_DEPTH" in selected.unavailable_inputs


def test_selection_does_not_use_method_count_as_evidence():
    methods = (
        MethodSpec("a", "1", "structure", ("K1",), ("F008",)),
        MethodSpec("b", "1", "structure", ("K2",), ("F008",)),
    )
    selected = select_methods(methods, question="structure", available_inputs=("F008",), max_methods=4)
    assert selected.selected_methods == ("a",)
    assert "b:same_required_inputs" in selected.redundancy_flags


def test_retrieval_is_domain_and_input_scoped():
    objects = (
        KnowledgeObject("K1", "Structure", "concept", ("structure",), ("F008",)),
        KnowledgeObject("K2", "Volatility", "state", ("volatility",), ("F004",)),
    )
    result = retrieve_knowledge(objects, domains=("structure",), required_inputs=("F008",))
    assert [x.object_id for x in result] == ["K1"]


def test_no_available_evidence_does_not_create_a_method():
    methods = (MethodSpec("structure", "1", "structure", ("K1",), ("F008",)),)
    selected = select_methods(methods, question="structure", available_inputs=())
    assert selected.selected_methods == ()
    assert "F008" in selected.unavailable_inputs
