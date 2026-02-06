# Table Handling Improvements for RAG

## The Problem

When dealing with structured data like nutritional tables, basic text chunking can break apart:
- Item names from their values
- Column headers from data rows
- Related information across columns

This leads to inaccurate retrieval and responses.

## What Changed

### 1. Better PDF Extraction (`extract_text_from_pdf`)

**Before (PyPDF2 only):**
```
Grilled Chicken Sandwich (Plain) 280 5 1 0 60 920 23 3 3 38
```
Problem: No context about what each number means!

**After (pdfplumber):**
```
Item: Grilled Chicken Sandwich (Plain) | Calories: 280 | Total Fat (g): 5 | 
Sat. fat (g): 1 | Trans Fat (g): 0 | Chol. (mg): 60 | Sodium (mg): 920 | 
Carbs (g): 23 | Fiber (g): 3 | Sugars (g): 3 | Protein (g): 38
```
Solution: Each value is labeled with its column header!

### 2. Smarter Chunking (`chunk_text`)

**Changes:**
- Increased chunk size: 500 → 1000 characters (keeps full rows together)
- Increased overlap: 50 → 100 characters (more context preservation)
- Breaks at newlines when possible (keeps paragraphs/rows intact)

### 3. More Retrieved Chunks (`search_documents`)

**Before:** Retrieved 3 chunks
**After:** Retrieved 5 chunks

Why? Tables often need multiple chunks to get complete information. Better to have too much context than too little.

### 4. Better AI Instructions (`system_message`)

Added specific instructions about handling tables:
- Look carefully for specific items
- Pay attention to column headers
- Match numbers to correct nutrients
- Be precise with numbers

## How to Update Your Code

```bash
# Install the new dependency
pip install pdfplumber

# Run the updated chatbot
streamlit run chatbot_workshop.py
```

## Testing the Improvements

1. Upload your Dairi-O nutritional table PDF
2. Ask: "What are the macronutrients for the plain grilled chicken sandwich?"
3. Expected answer:
   - Calories: 280
   - Protein: 38g
   - Carbs: 23g
   - Fat: 5g

4. Try other questions:
   - "How much protein is in the veggie burger?"
   - "Compare the calories between the hamburger and double burger"
   - "Which chicken sandwich has the most sodium?"

## If pdfplumber Doesn't Work

If you get an error installing pdfplumber, the code will fall back to PyPDF2 automatically. You'll see a warning:

```
⚠️ For better table extraction, install pdfplumber: pip install pdfplumber
```

The chatbot will still work, just with slightly less accurate table parsing.

## For Workshop Teaching

**Key Teaching Points:**

1. **"Not all text is created equal"**
   - Regular paragraphs: simple chunking works fine
   - Tables/structured data: need special handling
   
2. **"Context is everything in RAG"**
   - Without column headers, "280" is just a number
   - With headers, "Calories: 280" is meaningful
   
3. **"Retrieval is a trade-off"**
   - Too few chunks: might miss the answer
   - Too many chunks: might confuse the AI with irrelevant info
   - Tables often need more chunks than prose

4. **"The right tool for the job"**
   - PyPDF2: good for text documents
   - pdfplumber: built specifically for tables
   - Always choose tools that match your data type

## Advanced: Further Improvements

If you want to go even deeper in future workshops:

1. **Pre-process tables into a database**
   - Extract tables to pandas DataFrames
   - Store in SQLite
   - Use SQL queries instead of semantic search
   
2. **Hybrid search**
   - Use keyword search for exact matches (item names)
   - Use semantic search for concepts
   - Combine results

3. **Custom chunking strategies**
   - Detect tables automatically
   - Keep entire tables in single chunks
   - Or chunk by logical sections (entrees, sides, etc.)

4. **Vision-based extraction**
   - Use multimodal models that can "see" the table layout
   - Better for complex or poorly-formatted tables

## Common Issues

**"Still getting wrong numbers"**
- Check what text was actually extracted: print the chunks
- Verify pdfplumber installed correctly
- Try increasing n_results to 7-10
- Check if the PDF has images instead of text (use OCR)

**"Takes too long to process"**
- pdfplumber is slower than PyPDF2 (but more accurate)
- For workshops, pre-process documents before attendees arrive
- Or use smaller PDFs for demos

**"Chunks are still breaking awkwardly"**
- Increase chunk size to 1500 or 2000
- Adjust overlap to 200
- Try different break points (sentence endings, double newlines)

## Conclusion

These improvements significantly boost accuracy for table-based PDFs. The trade-off is:
- ✅ More accurate answers
- ✅ Better context preservation
- ❌ Slightly slower processing
- ❌ One more dependency to install

For a workshop focused on understanding RAG fundamentals, this is a great teachable moment about **why RAG isn't just "throw documents at an AI and hope for the best"** - it requires thoughtful design based on your data type.
