"""
Standalone UMLS pool builder - run in terminal, never in Jupyter.
Usage:
    cd /home/situser1/Entropy
    source .venv/bin/activate
    python build_umls_pool.py
"""
import spacy, scispacy, pandas as pd
from scispacy.linking import EntityLinker
from pathlib import Path

spacy.require_cpu()
print("Loading en_core_sci_md ...")
nlp = spacy.load("en_core_sci_md")
nlp.add_pipe("scispacy_linker",
             config={"resolve_abbreviations": True, "linker_name": "mesh"})
linker = nlp.get_pipe("scispacy_linker")
print(f"✓ EntityLinker ready | {len(linker.kb.cui_to_entity):,} concepts")

INTERMEDIATE = Path("outputs/rq1/intermediate")
df = pd.read_csv(INTERMEDIATE / "rq1_sampled_instances.csv")
mentions = df["gold_mention"].dropna().unique().tolist()
print(f"Processing {len(mentions)} unique mentions ...")

rows = []
for i, mention in enumerate(mentions):
    if i % 10 == 0:
        print(f"  [{i}/{len(mentions)}] pool={len(rows)}")
    gold_cui = str(df.loc[df["gold_mention"]==mention,"gold_cui"].iloc[0]) \
               if mention in df["gold_mention"].values else "NA"
    found = False
    try:
        doc = nlp(mention)
        for ent in doc.ents:
            for cui, score in ent._.kb_ents[:15]:
                if cui in linker.kb.cui_to_entity:
                    name = linker.kb.cui_to_entity[cui].canonical_name
                    rows.append({"candidate_text": name,
                                 "candidate_label": f"{cui}||{name}",
                                 "source_mention": mention,
                                 "linker_score": float(score)})
                    found = True
    except Exception as e:
        print(f"  [WARN] {mention}: {e}")
    rows.append({"candidate_text": mention,
                 "candidate_label": f"{gold_cui}||{mention}",
                 "source_mention": mention, "linker_score": 1.0})

out = pd.DataFrame(rows).drop_duplicates(subset=["candidate_label"])
out.to_csv(INTERMEDIATE / "umls_candidate_pool.csv", index=False)
print(f"\n✓ Saved {len(out)} candidates")
print(f"  avg {len(out)/max(len(mentions),1):.1f} per mention")
