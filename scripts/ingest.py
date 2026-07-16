import re

def extract_header(section_text: str) -> str:
    """Extracts the header from a section of text, if any."""
    lines = section_text.strip().split("\n")
    if not lines:
        return "Unknown Section"
        
    first_line = lines[0].strip()
    # If the first line looks like a Markdown header or a numbered list
    if re.match(r'^#+\s', first_line) or re.match(r'^\d+\.\s+[A-Z]', first_line):
        return re.sub(r'^#+\s', '', first_line).strip()
        
    return "General Policy"

def chunk_by_section(text: str) -> list[dict]:
    """
    Split policy text on section headers, then sub-chunk if a section is > 300 words.
    This preserves semantic boundaries (e.g. keeping 'Travel Policy' separate from 'Expense Policy').
    """
    # Regex to split on numbered headers (e.g. "1. Expense Policy") or Markdown headers ("# Policy")
    sections = re.split(r'\n(?=\d+\.\s+[A-Z]|\#{1,3}\s)', text)
    chunks = []
    
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
            
        words = sec.split()
        header = extract_header(sec)
        
        if len(words) <= 300:
            chunks.append({
                "text": sec, 
                "section": header
            })
        else:
            # Sub-chunk with overlap if section is too large
            for i in range(0, len(words), 170):
                sub = ' '.join(words[i:i+200])
                chunks.append({
                    "text": sub, 
                    "section": header
                })
                
    return chunks

if __name__ == "__main__":
    # Example usage
    sample_text = """
# Reimbursement Policy
Employees must submit reimbursement requests within 30 days of the expense.
Late submissions will require VP approval.

# Travel Advance
Travel advances are limited to $500 per trip.
Advances must be requested at least 14 days prior to travel.
"""
    result = chunk_by_section(sample_text)
    for c in result:
        print(f"[{c['section']}] -> {c['text'][:50]}...")
