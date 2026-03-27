# Memory: CLI/Tool Projects

## Scars

### Scar: No input validation
**When:** First user test
**What happened:** Tool crashed on unexpected input format without helpful error
**Consequence:** User assumed the tool was broken. Filed a bug. Never came back.
**Now we:** Validate all input immediately. Show clear, specific error: what's wrong and what format is expected.

## Insights

### Insight: Output before logic
**When:** Architecture
**What worked:** We designed the output format first, then built the processing to produce it
**Why:** The output IS the product. Working backward from desired output kept scope tight.
**Apply:** Define exact output format before writing processing logic.

### Insight: Progressive output
**When:** Long-running operations
**What worked:** Showed progress output during processing instead of silence until done
**Why:** Users thought the tool was frozen during long operations. Progress output fixed this.
**Apply:** Any operation over 2 seconds should print progress indicators.
