import pdfplumber
from langchain_core.documents import Document
from src.config import config

def clean_text(text):
    """Removes newlines and extra spaces."""
    if text:
        return text.replace('\n', ' ').strip()
    return "N/A"

def parse_pdf():
    """
    Parses the Trade Notice PDF.
    - Page 1: Treated as raw text context.
    - Page 2 onwards: Treated as structured tables.
    """
    print(f"--- Starting Ingestion for: {config.RAW_PDF_PATH} ---")
    documents = []
    
    # State variables for Forward Filling (handling merged cells)
    last_chapter = "N/A"
    
    with pdfplumber.open(config.RAW_PDF_PATH) as pdf:
        for i, page in enumerate(pdf.pages):
            page_num = i + 1
            
            # PAGE 1 (Context) Strategy
            if i == 0:
                text = page.extract_text()
                if text:
                    doc = Document(
                        page_content=f"Notification Context (Page 1):\n{text}",
                        metadata={"source": "page_1_intro", "page": 1, "type": "context"}
                    )
                    documents.append(doc)
                continue

            # PAGE 2 onwards (Tables) Strategy
            # Extract table
            table = page.extract_table()
            
            if not table:
                continue
                
            for row in table:
                # General Row structure -- [S.No, Chapter, ITC_Code, Description, Export Policy, Policy Condition, Notification No, Date]
                
                # Skipping Header Rows
                row_str = "".join([str(x) for x in row if x]).lower()
                if "description" in row_str or "export policy" in row_str or "itc(hs)" in row_str:
                    continue
                
                # Extracting Data -- the columns might shift slightly, but usually:
                # Col 0: S.No (often empty)
                # Col 1: Chapter Number
                # Col 2: ITC Code
                # Col 3: Description
                # Col 4: Export Policy
                # Col 5: Condition
                
                try:
                    chapter_raw = row[0] # Sometimes Chapter is in Col 0 or 1 depending on S.No column existence
                    itc_code = row[1]
                    desc = row[2]
                    policy = row[3]
                    condition = row[4] if len(row) > 4 else "None"
                    
                    # Forward Fill Logic for chapters -- If current row has a chapter, update state. If not, use last seen.
                    if chapter_raw and str(chapter_raw).strip().isdigit():
                        last_chapter = str(chapter_raw).strip()
                    
                    # Filter Garbage Rows -- If ITC Code is None or empty, it's likely a formatting row or continuation of description
                    if not itc_code or len(str(itc_code)) < 2:
                        continue

                    # Create Semantic String (The "Document") -- this is what the LLM will actually read.
                    content = (
                        f"Export Policy Details:\n"
                        f"Chapter: {last_chapter}\n"
                        f"ITC(HS) Code: {clean_text(itc_code)}\n"
                        f"Item Description: {clean_text(desc)}\n"
                        f"Export Policy: {clean_text(policy)}\n"
                        f"Policy Conditions: {clean_text(condition)}"
                    )
                    
                    # Metadata (For Filtering)
                    meta = {
                        "page": page_num,
                        "itc_code": clean_text(itc_code),
                        "policy": clean_text(policy),
                        "chapter": last_chapter,
                        "type": "policy_entry"
                    }
                    
                    documents.append(Document(page_content=content, metadata=meta))
                    
                except Exception as e:
                    # Skipping malformed rows for now
                    continue

    print(f"--- Parsed {len(documents)} documents from PDF ---")
    return documents

if __name__ == "__main__":
    # Testing the ingestion independently
    config.validate()
    docs = parse_pdf()
    print(f"Sample Doc:\n{docs[5].page_content}")