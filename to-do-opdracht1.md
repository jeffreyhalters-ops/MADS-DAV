# To-Do Lijst: Eerste Visualisatieopdracht (MADS-DAV)
*Voorbereiding op Les 2 (Draft presenteren) en Les 3 (Definitieve inlevering)*

---

### [x] WOENSDAG — FUNDAMENT & DATA GEREED (Afgerond!)
- [x] **MCP-concept ontrafeld**: Je weet dat `goad` en `codestyle` de coaches van Raoul zijn en dat je er zelf niets voor hoeft in te stellen.
- [x] **Topdataset gereed**: Nieuwe chat met 6.414 berichten (Jeffrey & Rick, 2021-2026) gepreprocessed naar `data/processed/whatsapp-20260909-185004.csv`.
- [x] **Config gekoppeld**: `config.toml` wijst direct naar jouw actieve dataset.
- [x] **Werkomgeving schoon**: Oude bestanden en tijdelijke testbestanden verwijderd.
- [x] **Les 0 begrepen**: Klassen, instanties en overerving onder de knie (100% score op de quiz!).
- [x] **Data-verkenning gedaan**: Twee ijzersterke patronen ontdekt in jullie chat.

---

### [x] DONDERDAGAVOND — LES 1 VERKENNEN (Afgerond!)
- [x] `notebooks/lesson1/01.1-goad-toolkit-101 jeffrey.ipynb`: Volledig afgerond (lopende band van `Pipeline` & `FreeShipping` succesvol gebouwd!).
- [x] `notebooks/lesson1/01.2-irc-chat jeffrey.ipynb`: Grotendeels doorlopen (regex, unmatched rijen analyseren, actieregels herstellen).
- [x] **Keuze voor visualisatie**: Gekozen voor **Het Dagritme & De Middagpiek** (Ochtend, Middag, Avond, Nacht).

---

### [x] ZATERDAGOCHTEND — DATA VERRIJKT & DRAFT VISUAL GEBOUWD (Afgerond!)
- [x] **01.2 Afgerond**: Pipeline voltooid en inzicht in bots vs. menselijke rituelen bekeken.
- [x] **01.3 Voltooid**: `load_own_chat()` en data verrijkt met 5 features (`DayPart`, `EmojiOnly`, `is_deleted`, `has_media`, `has_only_media`).
- [x] **Paragraaf 1.4**: Alle 5 de reflectievragen beantwoord en vastgelegd (zie onderaan dit document).
- [x] **Draft visualisatie ontworpen in `02.5-your_turn_jeffrey.ipynb`**:
  - Verticale grouped bar chart volgens Jonathan Schwabish (*Better Data Visualizations*).
  - Focus op het échte verhaal: **"Communicatiepiek in de middag!"** (47% van alle berichten valt tussen 12:00 en 18:00).
  - Schwabish ontwerpprincipes toegepast: Grey first, WhatsApp-groen accent (`#25D366`), directe labels in de ochtendstaven (geen aparte legenda), waarden in de staven bovenaan, en rustige Y-as (0, 1.000, 2.000).
  - Hoge resolutie afbeelding opgeslagen in `img/dagritme_vergelijking.png`.

---

### [x] ZONDAG — LES 2 THEORIE (2.1) & DESIGN ITERATIES (Afgerond!)
- [x] **`02.1-baseplot-101.ipynb`**: Volledig vertaald naar het Nederlands in `02.1-baseplot-101 jeffrey.ipynb`, elke regel code voorzien van heldere uitleg en verwijzingen, en de eindopdracht (`MaxHighlight`) werkend opgelost en getest!
- [x] **Hero-visualisatie gereed**: 4-staven grafiek met de WhatsApp-groene middagpiek (`img/dagritme_vergelijking.png`).
- [x] **Reflectietekst compleet**: Paragraaf 2.5 in `02.5-your_turn_jeffrey.ipynb` beantwoord volgens alle 5 criteria van de rubric (inclusief preattentive processing en reductie van clutter).
- [x] **Ontwerpproces vastgelegd**: Iteraties 1 t/m 4 en de waardevolle feedback van de klasgenoot beschreven in eigen woorden (zie onderaan).

---

### [ ] MAANDAGAVOND — VISUALISATIE INLEVEREN & COMMITTEN
- [ ] **Git commit maken op branch `les1`**:
  - Alle bestanden toevoegen (`img/dagritme_vergelijking.png`, notebooks van les 1 en les 2, to-do lijst).
  - Lefthook pre-commit controle laten slagen.
- [ ] **Inleverpunt controleren**:
  - Op Canvas controleren of Raoul een apart inleverbakje heeft geopend voor de draft van Visualisatie 1. Zo ja, de PNG of notebook uploaden.

---

### [ ] DINSDAGOCHTEND — LES 2 VOORBEREIDEN & PITCH KLAARZETTEN
- [ ] **Les 2 notebooks doornemen**:
  - [ ] `02.2-comparing_categories.ipynb`: Schwabish-principes op showcase-data (bar plots, grouped bars, heatmaps).
  - [ ] `02.3-simpsons_paradox.ipynb`: Simpson's paradox (waarom subgroepen een geaggregeerd beeld kunnen omdraaien).
  - [ ] `02.4-counting-and-averages.ipynb`: Berichten tellen vs. mensen tellen (valkuil van veelpraters en betrouwbaarheid).
- [ ] **Korte pitch voorbereiden (1-2 minuten)**:
  - De kernboodschap paraat hebben: onze communicatiepiek in de middag (47% van alle berichten).
  - Kunnen uitleggen waarom je n.a.v. feedback van je klasgenoot switchte van 8 naar 4 staven (snelle preattentive verwerking <50ms, één duidelijke groene staaf).
- [ ] **Eigen code nog even bestuderen**: Zodat je zonder haperen kunt uitleggen hoe je plot is opgebouwd.

---

### [ ] DINSDAG (MIDDAG & AVOND) — LES 2: DRAFT PRESENTATIE
- [ ] In Les 2 je draft visualisatie tonen en je pitch houden.
- [ ] Feedback en tips van docent Raoul en medestudenten noteren.

---

### [ ] RICHTING LES 3 — DEFINITIEVE INLEVERING (VOOR CIJFER)
- [ ] Feedback uit Les 2 verwerken in de visualisatie en reflectie.
- [ ] Definitieve inlevering van Visualisatie 1 voor de officiële beoordeling.

---

## Hoe de visualisatie tot stand is gekomen (mijn ontwerpproces)

Hieronder leg ik in mijn eigen woorden uit hoe ik stap voor stap tot de uiteindelijke grafiek ben gekomen, welke keuzes ik heb gemaakt en hoe feedback van een klasgenoot hierbij hielp:

### Iteratie 1: Focussen op het avondverschil (horizontale staven)
In eerste instantie keek ik naar het verschil tussen Rick en mij. Het viel me op dat ik 's avonds 31% meer berichten stuurde dan hij (645 om 493). Ik maakte daarom een horizontale staafgrafiek met 8 balkjes en liet mijn avondbalkje groen oplichten. 
- **Waarom ik switchte:** Toen ik naar het resultaat keek, merkte ik dat een horizontale tijdlijn niet lekker voelde; tijd loopt in je hoofd immers van links naar rechts (verticaal dus). Ook vond ik de losse legenda onderin onhandig: je ogen moeten steeds heen en weer springen tussen de kleurtjes en de grafiek. Maar het belangrijkste: toen ik nog eens goed naar de getallen keek, zag ik dat het echte verhaal helemaal niet in de avond zat, maar in de middag.

### Iteratie 2: Draaien naar de middagpiek & legenda weghalen
Ik gooide de grafiek om naar verticale staven en maakte de middag het hoofdonderwerp. Daar viel immers bijna de helft van al onze berichten (47%). Ik haalde de losse legenda weg en zette 'Partner' en 'Student' direct onderin de eerste twee ochtendstaven. Ook zette ik stippellijnen neer voor ons gemiddelde aantal berichten.
- **Waarom ik doorontwikkelde:** De grafiek was een stuk duidelijker, maar er stond nog steeds te veel ruis op. De stippellijnen maakten het beeld rommelig en de Y-as had veel te veel tussenstapjes (om de 250). Dat leidde af van waar het om ging.

### Iteratie 3: Ruis weghalen & Nederlandse notatie
Ik heb de stippellijnen eruit gegooid en de Y-as lekker rustig gemaakt: alleen nog 0, 1.000 en 2.000. De getallen zette ik strak bovenin de staven met Nederlandse punten (1.303 en 1.535) en de titel werd een duidelijke krantenkop: *"Communicatiepiek in de middag!"*.
- **De feedback van mijn klasgenoot:** Ik liet deze versie aan een klasgenoot zien om te testen wat hij zag. Hij zei meteen: 
  > *"Oeh, ik merk dat ik moeite heb om die twee staven per dagdeel te interpreteren. Waarom laat je dat onderscheid niet weg? Dan knalt de middag er nog veel duidelijker uit en is het contrast groter. Mijn blik gaat nu niet meteen naar het groen, omdat er twee groene staven naast elkaar staan."*

### Iteratie 4: De definitieve grafiek (4 strakke staven)
Die feedback vond ik ijzersterk. Ik wilde immers laten zien dat de *middag* onze gezamenlijke piek is. Door terug te gaan naar 4 staven (één per dagdeel) is er nu exact één felle WhatsApp-groene staaf en zijn de andere drie rustig grijs. Binnen een fractie van een seconde ziet iedereen direct waar het over gaat. De uitsplitsing tussen Rick en mij (1.303 vs. 1.535) heb ik niet weggegooid, maar subtiel in het tekstballonnetje bij de pijl gezet. Zo is de grafiek maximaal duidelijk en gaat er toch geen informatie verloren.

---

## Notities Paragraaf 1.4 ("Wat je moet noteren")

### 1. Wat stelt één rij nu precies voor?
> Eén rij is gewoon één verstuurd WhatsApp-bericht tussen Persoon A en Persoon B. Als iemand een lang bericht stuurde met meerdere enters, heeft het inlaadscript dat netjes samengevoegd tot één rij. We hebben aan elk bericht een tijdstempel en een dagdeel gekoppeld, en vlaggetjes toegevoegd voor verwijderde berichten, losse smileys en foto's. Zo kunnen we die er straks makkelijk uitfilteren als we alleen naar echte tekstgesprekken willen kijken.

### 2. Hoeveel rijen ben je kwijtgeraakt, en waaraan?
> Van de 8.358 ruwe regels zijn 6.414 berichten overgebleven (de rest waren afgebroken regels met enters die zijn samengevoegd). We zijn tijdens het inladen maar **17 regels kwijtgeraakt** (minder dan 0,3%). Dit bleek een doorgestuurd gesprekje te zijn met een derde persoon (Sian) waarin de tijd net andersom genoteerd stond. Dat die zijn weggevallen is eigenlijk alleen maar fijn, want zo blijft de chat puur tussen Persoon A en Persoon B.

### 3. Hoeveel mensen zitten er in je data?
> Er zitten precies **twee mensen** in de data: Persoon A (ikzelf) en Persoon B (mijn partner). Dat is belangrijk voor de analyse: we hebben wel heel veel berichten (6.414), maar het gaat over twee personen. Onze conclusies gaan dus puur over hoe wij met z'n tweeën appen, en niet over hoe mensen in het algemeen WhatsApp gebruiken.

### 4. Welke features heb je toegevoegd, en voor welke vraag dient elk?
> We hebben vijf handige kolommen toegevoegd aan de data:
> 1. **`day_part`**: Verdeelt de dag in 4 gelijke blokken van 6 uur (Ochtend, Middag, Avond, Nacht) om te zien wie van ons wanneer het meest appt.
> 2. **`is_deleted`**: Laat zien of een bericht later is verwijderd (29 keer).
> 3. **`only_emoji`**: Laat zien welke berichten alleen uit smileys bestaan zonder tekst (53 keer).
> 4. **`has_media`**: Laat zien of er een foto of video bij zit (394 keer).
> 5. **`has_only_media`**: Filtert de losse foto's eruit waar helemaal geen tekst bij staat (275 keer), zodat we die niet per ongeluk als volwaardig gesprek meetellen.

### 5. Wat zit erin dat er eigenlijk niet in thuishoort?
> Er zitten drie dingen in die geen echt inhoudelijk gesprek zijn:
> 1. Het allereerste bericht was de automatische beveiligingsmelding van WhatsApp over versleuteling.
> 2. 29 verwijderde berichten (die zijn nu leeg).
> 3. 275 losse foto's die zonder enige tekst zijn doorgestuurd.
> Omdat we hier nu vlaggetjes voor hebben gemaakt, kunnen we die er tijdens het maken van de grafiek heel simpel uitfilteren.




