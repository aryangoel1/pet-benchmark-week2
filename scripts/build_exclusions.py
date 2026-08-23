#!/usr/bin/env python3
"""Build the exclusion index the Week-2 benchmark is screened against.

Nothing may enter the benchmark that already appears in ANY of:

  A. the seven shared datasets  (Training set 1-6 + the S669 benchmark PDF)
  B. Luke's Week-2 final training dataset (temp_pH_dataset_ML_homology*)
  C. Luke's Week-1 pH database          (folded into B, indexed separately anyway)
  D. Aryan's Week-1 conditions database (25,340 rows, 150 mined OA papers)

Three independent keys are indexed so an overlap cannot slip through on a
naming difference:

  seq_sha1     full-sequence SHA-1  -> the only identity that cannot be faked
  protein_id   Luke's join key, "P" + sha1(seq.upper().strip("*"))[:12]
  uniprot      accession, upper-cased, isoform suffix stripped
  pmid/pmcid   the *paper* level - a paper already mined is off-limits entirely
  fingerprint  (protein, mutation, type, pH, T, value) measurement-level tuple

Output: data/exclusions.json  (+ data/exclusions.sqlite for the big sequence sets)
"""
import csv, hashlib, json, os, re, sqlite3, sys

csv.field_size_limit(10 ** 9)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESK = "/Users/aryan/Desktop"
DATA_DIR = os.path.join(DESK, "PET_Labs_Task_2", "Data")
LUKE2 = os.path.join(DESK, "PET_Labs_Task_2", "Luke_Week 2_ temperature_ph_dataset_v2")
LUKE1 = os.path.join(DESK, "PET_Labs_1", "submission")
ARYAN1 = os.path.join(DESK, "PET_Labs_1", "aryan_submission")
OUT_DB = os.path.join(ROOT, "data", "exclusions.sqlite")
OUT_JSON = os.path.join(ROOT, "data", "exclusions.json")

# the seven shared datasets, in the order the task lists the seven Sheets links
SEVEN = [
    ("Training set 1 - Tsuboyama2023.csv", "Tsuboyama2023"),
    ("Training set 2 - Domainome.csv", "Domainome"),
    ("Training set 3 - Domainome.csv", "Domainome"),
    ("training set 4 - Tsuboyama2023_double.csv", "Tsuboyama2023_double"),
    ("Training set 5 - Tsuboyama2023.csv", "Tsuboyama2023"),
    ("Training set 6 - Meltome.csv", "Meltome"),
    ("Benchmark data set - S669.pdf", "S669"),
]


def clean_seq(s):
    return re.sub(r"[^A-Z]", "", (s or "").upper())


def sha1(s):
    return hashlib.sha1(s.encode()).hexdigest()


def protein_id(seq):
    """Luke's join key, verbatim from his DATA_READINESS_HANDOFF.md."""
    return "P" + hashlib.sha1(seq.upper().replace("*", "").encode()).hexdigest()[:12]


def norm_acc(a):
    a = (a or "").strip().upper()
    a = a.split("-")[0].split(".")[0]
    return a if re.fullmatch(r"[A-Z0-9]{6,10}", a) else ""


def main():
    if os.path.exists(OUT_DB):
        os.remove(OUT_DB)
    db = sqlite3.connect(OUT_DB)
    db.executescript("""
        PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF;
        CREATE TABLE seq  (sha1 TEXT PRIMARY KEY, protein_id TEXT, source TEXT, split TEXT);
        CREATE TABLE acc  (uniprot TEXT PRIMARY KEY, source TEXT, split TEXT);
        CREATE TABLE pid  (protein_id TEXT PRIMARY KEY, source TEXT, split TEXT);
        CREATE TABLE paper(ident TEXT PRIMARY KEY, kind TEXT, source TEXT);
        CREATE TABLE fp   (fingerprint TEXT PRIMARY KEY, source TEXT);
        CREATE TABLE pdb  (pdb_id TEXT PRIMARY KEY, source TEXT);
    """)
    cur = db.cursor()
    stats = {}

    def add_seq(s, src, split=""):
        s = clean_seq(s)
        if len(s) < 20:
            return
        cur.execute("INSERT OR IGNORE INTO seq VALUES (?,?,?,?)", (sha1(s), protein_id(s), src, split))
        cur.execute("INSERT OR IGNORE INTO pid VALUES (?,?,?)", (protein_id(s), src, split))

    def add_acc(a, src, split=""):
        a = norm_acc(a)
        if a:
            cur.execute("INSERT OR IGNORE INTO acc VALUES (?,?,?)", (a, src, split))

    def add_paper(ident, kind, src):
        ident = (ident or "").strip().upper()
        if ident and ident not in ("NA", "NONE"):
            cur.execute("INSERT OR IGNORE INTO paper VALUES (?,?,?)", (ident, kind, src))

    def add_fp(*parts, src=""):
        # A measurement fingerprint is only a duplicate key if it identifies a PROTEIN.
        # "pH optimum = 7.0" with no accession and no sequence describes thousands of
        # unrelated enzymes; indexing it would drop legitimately new measurements as
        # false duplicates. Identity-less tuples are therefore never indexed.
        if not str(parts[0]).strip():
            return
        key = "|".join(str(p).strip().lower() for p in parts)
        cur.execute("INSERT OR IGNORE INTO fp VALUES (?,?)", (key, src))

    # ---------------------------------------------------------------- A: the seven
    for fname, label in SEVEN:
        path = os.path.join(DATA_DIR, fname)
        if fname.endswith(".pdf"):
            import pypdf
            n = 0
            rdr = pypdf.PdfReader(path)
            # the row index and the 4-character PDB code run together in the
            # extracted text once the index reaches 3 digits ("1001FXA" = 100 + 1FXA),
            # so the index is matched greedily and allowed to back-track into the code.
            row_re = re.compile(r"^\s*\d+\s*([0-9][A-Za-z0-9]{3})\s+([A-Za-z])\s+(\S+)\s+(\S+)\s+"
                                r"(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s*$")
            for page in rdr.pages:
                for line in (page.extract_text() or "").splitlines():
                    m = row_re.match(line)
                    if not m:
                        continue
                    n += 1
                    pdbid, chain, mut, _mp, ph, t, ddg = m.groups()
                    cur.execute("INSERT OR IGNORE INTO pdb VALUES (?,?)", (pdbid.upper(), label))
                    add_fp(pdbid.upper(), mut.upper(), "ddg", ph, t, ddg, src=label)
            stats[f"{label} ({fname})"] = {"rows_indexed": n, "kind": "pdb+mutation+ddG"}
            db.commit()
            print(f"  [{label:22}] {n:>7} rows  <- {fname}", file=sys.stderr)
            continue

        n = 0
        with open(path, newline="") as f:
            for row in csv.DictReader(f):
                n += 1
                add_seq(row.get("wt_sequence"), label)
                add_seq(row.get("mut_sequence"), label)
                add_acc(row.get("uniprot_id"), label)
                if row.get("pdb_id"):
                    cur.execute("INSERT OR IGNORE INTO pdb VALUES (?,?)", (row["pdb_id"].upper(), label))
                add_paper(row.get("pmid"), "pmid", label)
                add_fp(norm_acc(row.get("uniprot_id")) or (row.get("wt_seq_hash") or "")[:16],
                       row.get("mutation"), row.get("measurement_type"),
                       row.get("ph"), row.get("assay_temperature_c"),
                       row.get("measured_value"), src=label)
                if n % 100000 == 0:
                    db.commit()
        db.commit()
        stats[f"{label} ({fname})"] = {"rows_indexed": n, "kind": "sequence+uniprot+fingerprint"}
        print(f"  [{label:22}] {n:>7} rows  <- {fname}", file=sys.stderr)

    # -------------------------------------------------- B: Luke's Week-2 training set
    n = 0
    with open(os.path.join(LUKE2, "all_unique_proteins_homology.csv"), newline="") as f:
        for row in csv.DictReader(f):
            n += 1
            split = row.get("split_homology", "")
            s = clean_seq(row.get("sequence"))
            if len(s) >= 20:
                cur.execute("INSERT OR REPLACE INTO seq VALUES (?,?,?,?)",
                            (sha1(s), row["protein_id"], "Luke_week2", split))
                cur.execute("INSERT OR REPLACE INTO pid VALUES (?,?,?)",
                            (row["protein_id"], "Luke_week2", split))
            add_acc(row.get("uniprot_id"), "Luke_week2", split)
    db.commit()
    stats["Luke week-2 training/test proteins"] = {"rows_indexed": n, "kind": "protein_id+sequence+split"}
    print(f"  [Luke_week2 proteins  ] {n:>7} proteins", file=sys.stderr)

    n = 0
    with open(os.path.join(LUKE2, "temp_pH_dataset_ML_homology.csv"), newline="") as f:
        for row in csv.DictReader(f):
            n += 1
            add_fp(row.get("protein_id"), row.get("mutation"), row.get("measurement_type"),
                   row.get("pH"), row.get("temperature_c"), row.get("measured_value"),
                   src="Luke_week2")
            add_paper(row.get("source_id") if str(row.get("source_id", "")).isdigit() else "",
                      "pmid", "Luke_week2")
            if n % 100000 == 0:
                db.commit()
    db.commit()
    stats["Luke week-2 measurement records"] = {"rows_indexed": n, "kind": "measurement fingerprint"}
    print(f"  [Luke_week2 records   ] {n:>7} records", file=sys.stderr)

    # ------------------------------------------------------ C: Luke's Week-1 pH database
    n = 0
    with open(os.path.join(LUKE1, "plastic_enzyme_pH_database.csv"), newline="") as f:
        for row in csv.DictReader(f):
            n += 1
            add_seq(row.get("sequence"), "Luke_week1")
            add_acc(row.get("accession"), "Luke_week1")
            add_paper(row.get("pubmed_id"), "pmid", "Luke_week1")
            add_fp(norm_acc(row.get("accession")), row.get("mutation"),
                   row.get("measurement_type"), row.get("pH"), "", row.get("outcome"),
                   src="Luke_week1")
    db.commit()
    stats["Luke week-1 pH database"] = {"rows_indexed": n, "kind": "sequence+uniprot+pmid+fingerprint"}
    print(f"  [Luke_week1           ] {n:>7} rows", file=sys.stderr)

    # -------------------------------------------- D: Aryan's Week-1 conditions database
    n = 0
    with open(os.path.join(ARYAN1, "plastic_enzyme_conditions.csv"), newline="") as f:
        for row in csv.DictReader(f):
            n += 1
            add_acc(row.get("uniprot_accession"), "Aryan_week1")
            add_paper(row.get("pubmed_id"), "pmid", "Aryan_week1")
            add_paper(row.get("pmcid"), "pmcid", "Aryan_week1")
            add_fp(norm_acc(row.get("uniprot_accession")), row.get("mutation"),
                   row.get("measurement_type"), row.get("pH"), row.get("temperature_c"),
                   row.get("value_std") or row.get("value_raw"), src="Aryan_week1")
    db.commit()
    # every PMCID Aryan's week-1 harvester TOUCHED, even if it yielded no row
    touched = 0
    p1 = os.path.join(ARYAN1, "data", "papers.json")
    if os.path.exists(p1):
        for p in json.load(open(p1)):
            add_paper(p.get("pmcid"), "pmcid", "Aryan_week1_mined")
            add_paper(p.get("pmid"), "pmid", "Aryan_week1_mined")
            touched += 1
    db.commit()
    stats["Aryan week-1 conditions database"] = {"rows_indexed": n, "papers_mined": touched,
                                                 "kind": "uniprot+pmid/pmcid+fingerprint"}
    print(f"  [Aryan_week1          ] {n:>7} rows, {touched} papers already mined", file=sys.stderr)

    totals = {t: db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("seq", "acc", "pid", "paper", "fp", "pdb")}
    train_pids = db.execute("SELECT COUNT(*) FROM pid WHERE split='train'").fetchone()[0]
    test_pids = db.execute("SELECT COUNT(*) FROM pid WHERE split='test'").fetchone()[0]

    summary = {"per_source": stats, "index_totals": totals,
               "luke_train_protein_ids": train_pids, "luke_test_protein_ids": test_pids}
    json.dump(summary, open(OUT_JSON, "w"), indent=1)
    print("\nExclusion index:", json.dumps(totals), file=sys.stderr)
    print(f"  Luke split: {train_pids} train protein_ids / {test_pids} test protein_ids", file=sys.stderr)
    db.close()


if __name__ == "__main__":
    main()
