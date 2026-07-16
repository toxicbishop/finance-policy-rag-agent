from scripts.ingest import chunk_by_section, extract_header

def test_extract_header():
    assert extract_header("# Travel Policy\nContent here") == "Travel Policy"
    assert extract_header("1. Expense Policy\nContent here") == "1. Expense Policy"
    assert extract_header("Just some text without a header") == "General Policy"

def test_chunk_by_section():
    text = "# Policy A\nThis is a short policy.\n# Policy B\nAnother short one."
    chunks = chunk_by_section(text)
    
    # Depending on regex behavior, we might get empty chunks or just 2 chunks
    non_empty = [c for c in chunks if c["text"].strip()]
    assert len(non_empty) == 2
    assert non_empty[0]["section"] == "Policy A"
    assert non_empty[1]["section"] == "Policy B"
