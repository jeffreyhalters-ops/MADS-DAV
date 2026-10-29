# wa-analyzer — Modulaire Data & Visualisatie Pipeline (MADS-DAV)

**Auteur:** Jeffrey Halters  
**Opleiding:** Master Applied Data Science (MADS) — Hogeschool Utrecht (HU)  
**Vak:** Data Analysis & Visualization (DAV) — Docent: Raoul Grouls  

## Architectuur (Source-to-Sinks)

Dit project implementeert een 100% modulaire, reproduceerbare en **Atlas-proof** pipeline voor de kwantitatieve en visuele analyse van 4 jaar 1-op-1 WhatsApp-communicatie ($N = 6.414$ berichten, 2022–2026) tussen **Jeffrey** (`Student`) en **Rick** (`Partner`).

```text
wa-analyzer/
├── pyproject.toml              # Dependencies: pandas, numpy, scikit-learn, sentence-transformers, goad-toolkit, ruff, ty
├── .lefthook.yml               # Pre-commit hooks: ruff format, ruff check, ty check, notebooktester
├── data/
│   ├── raw/                    # _chat.txt (ruwe iOS WhatsApp-export)
│   └── processed/              # chat.parq (geanonimiseerd & verrijkt) en sessions.parq (384D MiniLM + 2D PCA)
├── src/
│   └── wa_analyzer/
│       ├── __init__.py         # Publieke package-exports
│       ├── config.py           # Thema-definities, 16 regexes, paden, Thailand-event en stijlen
│       ├── preprocess.py       # Raw _chat.txt -> parsen -> anonimiseren -> basis DataFrame
│       ├── features/
│       │   ├── __init__.py
│       │   ├── time_bursts.py  # Dagdelen, reactietijden, empirische pauzedrempel (~14 min) & sessies
│       │   ├── text_regex.py   # Emoji-filters, schone woordlengtes en de 16 thematische regexes (4 domeinen)
│       │   └── embeddings.py   # Hugging Face all-MiniLM-L6-v2 (384D) + L2-normalisatie + 2D PCA
│       ├── pipeline.py         # Centrale Pipeline-orchestratie: combineert tijd, regex en embeddings
│       ├── visualizer.py       # Jeffrey DAV-thema, JeffreyPlotSettings, format_header, format_footnote, badges
│       └── plots/
│           ├── figuur1.py      # Les 1/2: Reactietijden per dagdeel (Barbell plot + Mann-Whitney U) & Middagvolume
│           ├── figuur2.py      # Les 3: Events & uur-residu (Thailand vs. 4-jarige baseline met 1.000 bootstraps)
│           ├── figuur3.py      # Les 4: Verdelingen voor & na (Negatief-binomiaal nbinom + permutatietoets)
│           ├── figuur4.py      # Les 5: Relaties: Woordlengte vs. Reactietijd (2-fasen stuksgewijze regressie bij 10,5w)
│           ├── figuur5.py      # Les 6: 384D PCA vectorruimte (Jeffrey huisman vs. Rick werk)
│           └── figuur6.py      # Les 7: Netwerkanalyse & Thematische Gesprekstransities
├── notebooks/                  # Slanke consumptie-notebooks (max 3 codecellen: laad data, fit model, plot)
└── main.py                     # Centrale CLI/orchestrator: draait preprocess -> pipeline -> plots -> img/
```

## Gebruik

Draai de volledige pipeline van ruwe tekst tot en met alle 6 publicatiewaardige figuren in `img/`:

```bash
uv run python main.py
```

Kwaliteitscontroles (Ruff formatter, Ruff linter, Astral `ty` typechecker en `notebooktester`):

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run notebooktester notebooks/*.ipynb
```
