# Data provenance and author-confirmed replacement

Read when receiving data, reusing simulation examples, importing a returned analysis, or changing a project from demonstration data to real study data. The author decides which dataset is current and whether it has been updated. Record that decision accurately without presenting it as independent verification. An earlier confirmed decision is reused; ask again only for a consequential unresolved contradiction, not routine reassurance.

## Author decision and current document

If the author says the dataset is still simulated, retain its label and interpretation ceiling. If no explicit confirmation of real-data replacement exists, do not remove the label based on a renamed file, a script that strips prefixes, or the manuscript being called final. When actual replacement is received and the author confirms it was updated to real data, change obsolete simulation labels on the current working draft by default, propagate dependent Methods/Results/Discussion/tables/abstract changes and notify the author to check. Archive prior data, code, seeds, manifests and labels: do not erase historical provenance.

Change only labels associated with the replaced dataset. A simulation that remains part of the design, a sample-size simulation, a teaching example, or archived analysis stays labelled. Rewriting the same simulated values as real is not replacement. Partial replacement is scope-specific: separate real/simulated outcomes or subsets, never relabel the whole study. Continue independent writing conditionally while inconsistencies are resolved; no unsupported definitive claim belongs in a final accepted manuscript.

## Portable state helper

Use [../scripts/data_provenance.py](../scripts/data_provenance.py) and [../../../schemas/data-provenance.schema.json](../../../schemas/data-provenance.schema.json). `transition_data_state(previous, replacement, author_decision)` returns a new record, does not alter inputs, and retains prior lineage. Persist this record in the private Passport/work order and dated history using the project workspace contract. The helper does not edit DOCX text or decide that an output has passed research review.

- SIMULATED: simulation status retained.
- UNRESOLVED: absent digest, partial replacement or conflicting identical values requires scoped clarification.
- AUTHOR_DECLARED_REAL: author-confirmed replacement received; author declaration is recorded, independent verification not established.
- VERIFIED_REAL: a separate reviewer receipt is bound to that replacement digest. A caller-supplied status is not proof by itself; review the underlying verification evidence and reviewer provenance before relying on it.

Every permitted transition to real-data use triggers `author_recheck_required`. `remove_current_simulation_labels` refers only to stale labels in the working copy; it never authorizes deletion from history. Keep the author-facing notice short: “Đã cập nhật các nhãn mô phỏng lỗi thời theo dữ liệu anh xác nhận đã thay; anh kiểm tra lại nguồn dữ liệu và các phần liên quan.” Do not add these workflow messages to manuscript prose.

## Rename/reorder-resistant signal

A repeated declaration does not resolve an identical-value conflict. Check
simulated digests throughout retained history, including a historical version
returned after a newer replacement. Clear a known conflict only with an explicit
`author_decision.conflict_resolution` receipt containing `status: CONFIRMED`,
`scope: dataset-replacement`, the exact replacement `digest`, `author`, `timestamp`
and a substantive `reason`. Preserve that receipt in history and notify the author
to recheck; this remains an author resolution, not independent authenticity proof.

`fingerprint_records(rows, columns, key)` produces a keyed HMAC over versioned canonical selected records. It ignores row order, preserves duplicates, sorts column names and preserves value types; Unicode strings are NFC-normalized. It rejects missing columns, nonfinite numbers, empty inputs and short keys. Keep a randomly generated key of at least 32 bytes locally under the project's access control; never commit the key or row values. Store normalization version, selected variables, raw file SHA256, value fingerprint and source/version relationships in the private registry. Pseudonymous digests are still sensitive project metadata.

Identical selected-value fingerprints after rename are a review signal, not a finding of misconduct: small datasets, aggregate outputs or unchanged selected columns may match legitimately. Fingerprints are comparable only under the same key/normalization/variable mapping; a changed key must not falsely imply changed data. Renamed variables require explicit codebook mapping before fingerprinting. A different digest proves difference, not authenticity or independence. Explain this distinction when the author needs to resolve a conflict.

No participant values or identifiers belong in progress JSONL, public test fixtures or GitHub. Use synthetic data for regression tests. Preserve all local source/analysis history, and record transitions as dated decisions with source hashes, author and timestamp.
