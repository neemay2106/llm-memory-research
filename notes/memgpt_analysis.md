What MemGPT does:
Flat text in, flat text out. It saves messages and summaries into external storage and pulls them back when needed. The trigger is reactive — it offloads when the context window fills up.
What it's missing for your use case:
Two things. First, it stores what happened not why decisions were made. Second, everything is flat — there's no way to query "what decisions depended on this constraint?" You'd have to read through everything.
Why your graph fixes this:
Typed edges (depends_on, was_constrained_by, implements) let the continuation agent immediately find connected decisions without reading the full history. It's structured retrieval vs. linear search through text.