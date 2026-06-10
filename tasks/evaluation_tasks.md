# Programming Tasks

## 1. Flatten Nested JSON Keys
**Description:** Implement a function that converts a nested JSON/dictionary structure into a single-level dictionary using dot-separated key paths.

**Success Criterion:** All nested keys are flattened correctly while preserving values and hierarchy through key paths.

---

## 2. Binary Search Tree
**Description:** Implement a Binary Search Tree (BST) supporting insertion, search, and deletion operations.

**Success Criterion:** Insert, search, and delete operations maintain BST properties and produce correct results for all node cases.

---

## 3. LRU Cache
**Description:** Implement a Least Recently Used (LRU) cache with configurable capacity and `get`/`put` operations.

**Success Criterion:** Cache returns correct values and evicts the least recently used item when capacity is exceeded.

---

## 4. Rate Limiter
**Description:** Implement a rate limiter that allows at most **N** requests within a rolling one-minute window.

**Success Criterion:** Requests beyond the configured limit are consistently rejected until they fall outside the time window.

---

## 5. Duplicate File Detector
**Description:** Walk a directory tree, compute content hashes, and identify files with identical contents.

**Success Criterion:** Files with matching content are grouped together regardless of filename or location.

---

## 6. Log File Pattern Detector
**Description:** Analyze a log file and detect regex matches that occur at least **K** times within an **N-second** time window.

**Success Criterion:** All qualifying pattern bursts are detected and reported with accurate timestamps.

---

## 7. Retry Decorator with Exponential Backoff
**Description:** Create a decorator that automatically retries failed function calls using exponential backoff delays.

**Success Criterion:** Failed operations are retried according to the configured policy and stop after the maximum retry count.

---

## 8. Timing Context Manager
**Description:** Implement a context manager that measures execution time of code blocks and produces a summary report grouped by label.

**Success Criterion:** Execution times are accurately recorded and aggregated across multiple labeled blocks.

---

## 9. Event Emitter
**Description:** Implement an event emitter supporting event registration (`on`), emission (`emit`), and removal (`off`).

**Success Criterion:** Registered listeners receive events correctly and removed listeners are no longer invoked.

---

## 10. CSV Schema Validator
**Description:** Build a CSV validator that checks rows against a schema, performs type coercion, and accumulates validation errors.

**Success Criterion:** Valid rows are successfully coerced while all schema violations are reported without stopping validation.

---

## 11. JSON Diff Utility
**Description:** Compare two JSON objects and identify added, removed, and modified fields.

**Success Criterion:** The diff output accurately categorizes every change between the two inputs.

---

## 12. Inverted Index Builder
**Description:** Construct an inverted index mapping terms to the documents in which they appear.

**Success Criterion:** Queries for a term return the complete and correct set of matching documents.

---

## 13. TF-IDF Scorer
**Description:** Implement TF-IDF scoring for a corpus of documents to measure term importance.

**Success Criterion:** Scores reflect correct TF-IDF calculations and rank terms appropriately across documents.

---

## 14. Pipeline Builder
**Description:** Create a pipeline framework that chains callable processing steps, records execution times, and short-circuits on errors.

**Success Criterion:** Steps execute in order, timings are collected, and failures halt downstream execution.

---

## 15. Graph Traversal Library
**Description:** Implement a graph data structure with Breadth-First Search (BFS) and Depth-First Search (DFS) traversal methods.

**Success Criterion:** BFS and DFS return valid traversal orders covering all reachable nodes from a starting vertex.