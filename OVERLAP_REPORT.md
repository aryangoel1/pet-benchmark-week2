# Overlap audit — Week-2 independent benchmark

Every candidate measurement was screened against **all seven shared datasets**, **Luke's Week-2 training dataset**, **Luke's Week-1 pH database** and **my own Week-1 conditions database** before anything was shipped. This is the audit trail.

## What was indexed

| Source | Records indexed | Keys extracted |
|---|---|---|
| Tsuboyama2023 (Training set 1 - Tsuboyama2023.csv) | 250,000 | sequence+uniprot+fingerprint |
| Domainome (Training set 2 - Domainome.csv) | 250,000 | sequence+uniprot+fingerprint |
| Domainome (Training set 3 - Domainome.csv) | 207,943 | sequence+uniprot+fingerprint |
| Tsuboyama2023_double (training set 4 - Tsuboyama2023_double.csv) | 138,275 | sequence+uniprot+fingerprint |
| Tsuboyama2023 (Training set 5 - Tsuboyama2023.csv) | 107,155 | sequence+uniprot+fingerprint |
| Meltome (Training set 6 - Meltome.csv) | 27,884 | sequence+uniprot+fingerprint |
| S669 (Benchmark data set - S669.pdf) | 658 | pdb+mutation+ddG |
| Luke week-2 training/test proteins | 37,448 | protein_id+sequence+split |
| Luke week-2 measurement records | 563,076 | measurement fingerprint |
| Luke week-1 pH database | 12,082 | sequence+uniprot+pmid+fingerprint |
| Aryan week-1 conditions database | 25,340 | uniprot+pmid/pmcid+fingerprint |

**Resulting index:** 970,289 distinct protein sequences · 970,289 Luke-format `protein_id`s · 16,297 UniProt accessions · 6,941 paper identifiers (PMID/PMCID) · 1,579,354 measurement fingerprints · 89 PDB codes.

Of the indexed proteins, **31,426** are in Luke's `split_homology == train` and **5,957** in his held-out test split.

## The seven datasets, as supplied

| # | Dataset | Source sheet |
|---|---|---|
| 1 | Training set 1 — Tsuboyama2023 | [sheet](https://docs.google.com/spreadsheets/d/1D3SuYcpPAwwzgpMgnGXvrUmYaYQPGNLIjH0o40ePdu4/edit?usp=sharing) |
| 2 | Training set 2 — Domainome | [sheet](https://docs.google.com/spreadsheets/d/1cqGczP84zkfsTa4W1-ShitCEsA-PQCmlNGHRUWLkYlA/edit?usp=sharing) |
| 3 | Training set 3 — Domainome | [sheet](https://docs.google.com/spreadsheets/d/1XCAng1bQq44u9irqOnaZkmuadzf3OhHN5fuUzkloyB0/edit?usp=sharing) |
| 4 | Training set 4 — Tsuboyama2023_double | [sheet](https://docs.google.com/spreadsheets/d/1W471dUgXm867lDDywmUTkvQVA1ApmoXhRRY9WwLWd50/edit?usp=sharing) |
| 5 | Training set 5 — Tsuboyama2023 | [sheet](https://docs.google.com/spreadsheets/d/1FEkmSDK-VEdkCQixbRBepH68cyyv1XvWbLMG-xTFNQA/edit?usp=sharing) |
| 6 | Training set 6 — Meltome | [sheet](https://docs.google.com/spreadsheets/d/1iXVdyaI80a0pbtrHPlHw5OSNkJrRuHDGYLoV20_fNfo/edit?usp=sharing) |
| 7 | Benchmark data set — S669 | [sheet](https://docs.google.com/spreadsheets/d/19qZetoMKP4HD63f0MPpMKQhIAeflJyjed730rcKMv88/edit?usp=sharing) |

## Screens applied to every candidate row

| Screen | What it compares | Rows it fired on |
|---|---|---|
| S1 sequence identity | SHA-1 of the resolved sequence vs all indexed sequences | 106 |
| S2 Luke join key | `protein_id` = `"P"+sha1(seq.upper().replace("*",""))[:12]` vs his split | 106 |
| S3 UniProt accession | accession vs every accession in every prior dataset | 99 |
| S4 paper identity | PMCID/PMID vs every paper any prior dataset cites | 0 |
| S5 measurement tuple | (protein, mutation, type, pH, T, value) vs 1.58 M fingerprints | 0 |
| S6 PDB code | PDB codes named in the paper vs the S669 roster | 0 |
| S7 internal duplicate | the same measurement extracted twice within this build | 77 |

## Verdicts

| Verdict | Rows | Outcome |
|---|---|---|
| `DROP_TRAIN_OVERLAP` | 82 | protein sits in Luke's **training** split — deleted |
| `DROP_DUPLICATE` | 0 | already present in a prior dataset — deleted |
| `DROP_INTERNAL_DUP` | 77 | duplicate within this build — deleted |
| `KEEP_TIER_A` | 138 | appears in **no** prior dataset — shipped as the gold benchmark |
| `KEEP_TIER_B` | 11 | protein is in Luke's **held-out test** split only — shipped, flagged |
| `KEEP_NO_SEQUENCE` | 482 | real measurement, no sequence resolvable — shipped as conditions-only |

### Why paper-level exclusion matters

Screen S4 removes any article already mined by my Week-1 build (all 199 of them) or cited by any prior dataset — **before the article is even downloaded**. That prevents the same measurement re-entering the benchmark through a different enzyme name.


## Independence statement

- **0** shipped rows carry a protein in `split_homology == "train"`.
- **137** shipped rows carry a protein that appears in **none** of the seven datasets and **none** of Luke's data.
- **11** rows are on proteins already inside Luke's held-out test split. They are not training contamination, but they are not novel either — they are tiered separately so they can be excluded with one filter.
- **99** distinct source articles, none of which appears in any prior dataset.

