from reference.runtime.rfc_explorer import build_rfc_index


def test_rfc_explorer_builds_index():
    idx = build_rfc_index()
    assert "rfcs" in idx
    assert len(idx["rfcs"]) >= 10
    ids = {r["id"] for r in idx["rfcs"]}
    assert "ARIA-RFC-001" in ids
