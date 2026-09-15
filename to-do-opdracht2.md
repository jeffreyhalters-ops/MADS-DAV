# To-Do Lijst: Tweede Visualisatieopdracht (MADS-DAV)
*Thema: Tijdreeksen, Events & Residuen ("Time, subtract the cycle, keep the residual")*

---

## Waar gaat Opdracht 2 over?
Waar **Opdracht 1** ging over een statische categorische vergelijking (het dagritme in 4 dagdelen), duikt **Opdracht 2** in het verloop van de **tijd**:
* **Het kernprincipe van Les 3:** *"Dat mensen slapen is geen interessante grafiek; het residu (de afwijking ten opzichte van wat normaal verwacht wordt) kan dat wél zijn."*
* **Het doel:** Je kiest een specifiek event dat je kent uit jullie WhatsApp-geschiedenis (bijvoorbeeld een vakantie, een verhuizing, een festival, een drukke werk-/tentamenweek of jullie drukste dag ooit).
* **De vergelijking:** Je vergelijkt die event-periode met een eerlijke baseline (normale dagen) en laat zien wat er daadwerkelijk veranderde (het *residu*: event min baseline).

---

## Tijdplanning & Roadmap (De 4 Werkblokken)

### [x] 1. VOORBEREIDING LES 2 — Afronding Theorie, Verantwoording & Verdieping (Afgerond!)
*Doel: De theorie van Les 2 beheersen, verantwoording toevoegen aan de Hero visual, en een empirische achtervang bouwen.*

- [x] **`02.2-comparing_categories.ipynb`**:
  - Volledig vertaald en doorgenomen in `02.2-comparing_categories jeffrey.ipynb`.
  - Schwabish-principes op showcase-data (pinguïns en Titanic) doorgrond.
  - Percentage altijd met de noemer tonen (nooit losse percentages zonder absolute aantallen).
- [x] **`02.3-simpsons_paradox.ipynb`**:
  - Volledig vertaald en doorgenomen in `02.3-simpsons_paradox jeffrey.ipynb`.
  - Simpson's paradox doorgrond: waarom een geaggregeerde trend kan omdraaien op subgroepniveau.
  - Barbell plot leren toepassen om de kloof (*the gap*) direct inzichtelijk te maken.
- [x] **`02.4-counting-and-averages.ipynb`**:
  - Volledig vertaald en doorgenomen in `02.4-counting-and-averages jeffrey.ipynb`.
  - Berichten tellen vs. mensen tellen (de valkuil van veelpraters) en 95%-betrouwbaarheidsintervallen.
- [x] **Hero Visualisatie aangescherpt met dataverantwoording (Richting 3)**:
  - Subtiele cursieve noot toegevoegd onder de X-as van `img/dagritme_vergelijking.png` en in `02.5-your_turn_jeffrey.ipynb`.
  - Noemer en filtercontext direct inzichtelijk: 6.059 inhoudelijke berichten (355 gefilterd) over 928 actieve dagen (2021–2026).
- [x] **Verdiepingsanalyse & Achtervang gereed (`02.5-verdieping_simpsons_jeffrey.ipynb`)**:
  - **Deel A (Weekdag vs. Weekend)**: Genormaliseerd op relatieve percentages om de 5 vs 2 dagen bias op te heffen. Toont dat in het weekend de ochtend nét iets actiever is dan de middag (39,8% vs 38,8%).
  - **Deel B (Partner vs. Student via Barbell Plot)**: Toont aan dat de gap tussen Jeffrey en Rick maximaal 2,0%-punt is (middag 46,8% vs 46,9%). Er is géén sprake van een verborgen Simpson's paradox tussen personen.
  - Hoge resolutie figuur geëxporteerd naar `img/dagritme_verdieping_simpsons.png` als achtervang voor de pitch.

---

### [ ] 2. DONDERDAGAVOND (ca. 2 tot 2,5 uur) — Vliegende Start Tijdreeksen (Les 3)
*Doel: De theorie en techniek van tijdreeksen onder de knie krijgen, zodat zaterdag direct naar de eigen data kan gaan.*

- [ ] **`03.1-time.ipynb` (ca. 60 min)**:
  - Werken met tijdstempels: `pd.to_datetime`, `.dt`-functies en `resample("D")`.
  - Continuïteit en gaten in de tijd: waarom `reindex` nodig is om te voorkomen dat seaborn een lijn trekt over ontbrekende periodes.
- [ ] **`03.2-statistics-of-time.ipynb` (ca. 60 min)**:
  - Rolling windows: ruwe data vs. afgevlakte trend (raw & smoothed op één as).
  - Autocorrelatie (ACF): regelmatige cycli en seizoensritmes opsporen.
  - Seizoensontbinding (`seasonal_decompose`): trend, seizoen en residu splitsen.

---

### [ ] 3. ZATERDAGOCHTEND (ca. 4 tot 5 uur, max 6 uur) — Het Hart van Opdracht 2
*Doel: Eigen chat induiken, event & hypothese kiezen, baseline aftrekken en de draft-visualisatie bouwen.*

- [ ] **Stap 3A: Data verkennen met `03.3-events-in-your-chat.ipynb` (ca. 45 min)**:
  - De overstap naar jullie eigen WhatsApp-chat: piekdagen opsporen en koppelen aan herinneringen via `my_events`.
- [ ] **Stap 3B: Event & Hypothese vastleggen (ca. 45 min)**:
  - *Kies een concreet event:* bijv. een vakantie samen, weekend weg, verhuizing, festival of jullie all-time drukste dag.
  - *Formuleer de hypothese VÓÓR het plotten:* wat verwacht je dat er veranderde? (Aantal berichten, tijdstip, één persoon actiever?). Dit voorkomt *hindsight bias*.
- [ ] **Stap 3C: Visualisatie 2 ontwerpen (Draft) (ca. 2 uur)**:
  - *Eerlijke baseline bepalen:* bijv. een feest-vrijdag vergelijken met normale vrijdagen (niet met "alle dagen").
  - *Residu berekenen:* toon het verschil ten opzichte van normaal (event min baseline).
  - *Schwabish-principes toepassen:* neutrale grijstinten voor baseline, felle focuskleur voor residu/event, rustige assen, geen clutter.
  - *Tekst integreren:* krantenkop als titel en directe annotatiepijlen bij het cruciale punt.
- [ ] **Stap 3D: Reflectie schrijven (ca. 45 min)**:
  - Beantwoorden van de rubric-vragen (preattentive visual processing <50ms, Gestalt-principes en de onderbouwing van je claim).

---

### [ ] 4. MAANDAGAVOND (ca. 1,5 tot 2 uur) — Uitloop, Finetuning & Klaarzetten
*Doel: Rustig met een frisse blik de laatste puntjes op de i zetten en de pitch voorbereiden.*

- [ ] **Visuele check & finetuning (ca. 30 min)**:
  - Laatste controle van labels, titels, as-notaties en leesbaarheid.
  - Hoge resolutie afbeelding exporteren naar `img/`.
- [ ] **Korte pitch voorbereiden (ca. 30 min)**:
  - Kernverhaal paraat hebben in 1-2 minuten: welk event, wat was de hypothese, en wat laat het residu zien?
- [ ] **Git commit & inlevering (ca. 15 min)**:
  - Veilige commit maken op branch `les1` met werkende linters.
  - Draft visualisatie klaarzetten voor presentatie in Les 3/4.

---

### [ ] 5. IN DE LES & DAARNA — PRESENTATIE & DEFINITIEVE INLEVERING (Les 4/5)
- [ ] Draft presenteren in de les en gerichte feedback ophalen bij docent Raoul en medestudenten.
- [ ] Eventuele verbetersuggesties verwerken en definitieve versie inleveren voor het officiële cijfer.
