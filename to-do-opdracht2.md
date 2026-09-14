# To-Do Lijst: Tweede Visualisatieopdracht (MADS-DAV)
*Thema: Tijdreeksen, Events & Residuen ("Time, subtract the cycle, keep the residual")*

---

## Waar gaat Opdracht 2 over?
Waar **Opdracht 1** ging over een statische categorische vergelijking (het dagritme in 4 dagdelen), duikt **Opdracht 2** in het verloop van de **tijd**:
* **Het kernprincipe van Les 3:** *"Dat mensen slapen is geen interessante grafiek; het residu (de afwijking ten opzichte van wat normaal verwacht wordt) kan dat wél zijn."*
* **Het doel:** Je kiest een specifiek event dat je kent uit jullie WhatsApp-geschiedenis (bijvoorbeeld een vakantie, een verhuizing, een festival, een drukke werk-/tentamenweek of jullie drukste dag ooit).
* **De vergelijking:** Je vergelijkt die event-periode met een eerlijke baseline (normale dagen) en laat zien wat er daadwerkelijk veranderde (het *residu*: event min baseline).

---

## Fase 1: Theorie Les 2 voltooien (Dinsdagochtend / In-class)
*Doel: De concepten van Les 2 afronden die de basis vormen voor groepsvergelijkingen en betrouwbaarheid.*

- [ ] **`02.2-comparing_categories.ipynb`**:
  - Schwabish-principes op showcase-data (pinguïns en Titanic).
  - Keuze tussen staafdiagrammen, grouped bars en heatmaps.
  - Percentage altijd met de noemer tonen (geen losse percentages zonder absolute aantallen).
- [ ] **`02.3-simpsons_paradox.ipynb`**:
  - Simpson's paradox doorgronden: waarom een geaggregeerde trend compleet kan omdraaien als je uitsplitst naar subgroepen.
  - Leren zoeken naar verstorende variabelen (periode, activiteit, platform, etc.).
- [ ] **`02.4-counting-and-averages.ipynb`**:
  - Berichten tellen vs. mensen tellen (de valkuil van veelpraters).
  - Wat een 95%-betrouwbaarheidsinterval (error bar) betekent voor claims.

---

## Fase 2: Tijdreeksen & Data-engineering (Les 3 notebooks)
*Doel: Leren omgaan met tijd, kalenders, ontbrekende data en seizoenspatronen.*

- [ ] **`03.1-time.ipynb`**:
  - Werken met tijdstempels: `pd.to_datetime`, `.dt`-functies en `resample("D")`.
  - Continuïteit en gaten in de tijd: waarom `reindex` nodig is om te voorkomen dat seaborn een lijn trekt over ontbrekende periodes.
- [ ] **`03.2-statistics-of-time.ipynb`**:
  - Rolling windows: ruwe data vs. afgevlakte trend (raw & smoothed op één as).
  - Autocorrelatie (ACF): regelmatige cycli opsporen.
  - Seizoensontbinding (`seasonal_decompose`): trend, seizoen en residu splitsen.
- [ ] **`03.3-events-in-your-chat.ipynb`**:
  - De overstap naar jullie eigen WhatsApp-chat: piekdagen opsporen en koppelen aan herinneringen via `my_events`.

---

## Fase 3: Event & Hypothese kiezen in eigen chat
*Doel: Een helder verhaal en vooraf getoetste claim formuleren.*

- [ ] **Kies een concreet event uit jullie chat**:
  - *Optie A:* Een specifieke bekende gebeurtenis (bijv. een vakantie samen, een weekend weg, een verhuizing of festival).
  - *Optie B:* Jullie all-time drukste dag / week (data-gedreven piek die je kunt verklaren vanuit herinnering).
- [ ] **Formuleer de hypothese VÓÓR je de plot bouwt**:
  - Wat verwacht je dat er veranderde tijdens dit event? (Meer berichten? Andere tijdstippen? Eén iemand die ineens veel meer stuurde? Kortere reactietijden?).
  - Dit voorkomt *hindsight bias* (achteraf een verhaaltje verzinnen bij een willekeurige piek).

---

## Fase 4: Visualisatie 2 ontwerpen (Draft)
*Doel: Een overtuigende visualisatie bouwen volgens de Schwabish-principes en de rubric.*

- [ ] **Bepaal een eerlijke baseline**:
  - Vergelijk het event niet zomaar met "alle dagen op één hoop", maar met vergelijkbare normale dagen (bijvoorbeeld: een feest-vrijdag vergelijken met normale vrijdagen).
- [ ] **Bereken en toon het residu**:
  - Toon niet alleen de ruwe aantallen, maar laat het verschil zien ten opzichte van normaal (de werkelijke 'impact' van het event).
- [ ] **Ontwerpprincipes toepassen (Schwabish & Rubric)**:
  - *Start with grey:* Neutrale grijstinten voor de normale baseline / context.
  - *Accentkleur:* Felle focuskleur voor het specifieke event of het residu.
  - *Reduce clutter:* Geen spaghetti-lijnen, geen overbodige rasterlijnen of legenda's.
  - *Integrate text:* Een krantenkop als titel die direct de conclusie vertelt, en annotatiepijlen bij het specifieke moment.
- [ ] **Reflectie schrijven**:
  - Antwoord geven op preattentive processing (<50ms), Gestalt-principes en de onderbouwing van de claim.

---

## Fase 5: Presentatie Draft & Definitieve Inlevering (Les 4/5)
- [ ] Draft presenteren in de les en feedback ophalen bij docent Raoul en medestudenten.
- [ ] Feedback verwerken en definitieve versie inleveren voor het officiële cijfer van Opdracht 2.
