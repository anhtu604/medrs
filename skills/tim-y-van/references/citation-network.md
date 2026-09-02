# Citation-network mode

## Nodes and edges

A node contains canonical work ID, DOI/PMID/PMCID, citation metadata, discovery role (`seed`, `backward`, `forward`, `related`), parent work, source/API, retrieval time, abstract/full-text/access state, screening decision/reason, design and evidence classification with confidence/reason, correction/retraction check, and citation count with source/date and `DESCRIPTIVE_ONLY` use.

Allowed directed edge types are `cites`, `cited_by`, `updates`, `corrects`, `retracts`, and `related_by_source`. Every edge records source, retrieval date and verification status. `related_by_source` is not a citation. Preserve record-to-record correspondence when querying multiple seeds; do not convert an aggregate linked-UID set into invented pairs.

## Classification

Do not infer design or evidence level from title alone. Without adequate abstract/full text use `evidence_level: UNRESOLVED`, `classification_confidence: LOW`, and `classification_reason: ABSTRACT_OR_FULL_TEXT_REQUIRED`. Evidence level is not risk of bias or certainty; final appraisal belongs to `danh-gia-chat-luong-bang-chung`.

## Stopping and claims

Choose the stopping rule before expansion: all key papers searched backward/forward; two consecutive rounds yield no new eligible work or evidence cluster; a prespecified date cutoff is reached; or remaining records are duplicates/ineligible. Resource/API limits are an incomplete stop. The output always identifies itself as citation-network exploration unless the separate systematic-search and screening contracts are fully satisfied. Network size, centrality and citation count never substitute for quality.

