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

### [x] MAANDAGAVOND — VISUAL INLEVEREN, CODE DOORGRONDEN & COMMITTEN (Afgerond!)
- [x] **Git commit gemaakt op branch `les1`**:
  - Alle bestanden veilig vastgelegd, linters en link-checkers met succes gedraaid!
- [x] **Visual ingeleverd**:
  - Draft visualisatie en toelichting via de mail gedeeld met docent Raoul.
- [x] **Code & transformaties volledig doorgrond**:
  - Zowel de dataverrijking (`DayPart`, `EmojiOnly`, `RegexFeature` in `01.3`) als de visualisatiecode (`02.5`) tot in detail begrepen.
  - Conceptueel architectuur-schema (`Source -> Graph -> Sinks -> Repository -> Serve`) vastgelegd in `img/data_architectuur_flow.png`.
- [x] **Pitch van 1-2 minuten voorbereid**:
  - Kernverhaal paraat: communicatiepiek in de middag (47% van alle berichten).
  - Ontwerpkeuzes paraat: preattentive processing (<50ms) met één WhatsApp-groene staaf, reductie van clutter (van 8 naar 4 staven n.a.v. feedback klasgenoot), directe data labels en krantenkop als titel.

---

### [x] DINSDAGOCHTEND — ONTSPANNEN CHECK VOOR DE LES (Afgerond!)
- [x] Pitch doorgenomen en draft visualisatie getoond in Les 2.

---

### [x] DINSDAG (MIDDAG & AVOND) — LES 2: DRAFT PRESENTATIE & FEEDBACK (Afgerond!)
- [x] **Draft visualisatie gepresenteerd & feedback Raoul ontvangen**:
  > *"Het optellen van berichten (wie appt het meest / dagdelen) is nog geen echte story; iedereen slaapt 's nachts en appt 's middags. Zoek iets wat je van tevoren nog niet wist door inhoudelijke features toe te voegen aan de pipeline."*

---

### [x] DINSDAGAVOND — FEEDBACK RAOUL VERWERKT: ITERATIE 5 (Afgerond!)
- [x] **Story omgegooid naar interactiedynamiek**: **Reactietijd (*Response Time*) per dagdeel**.
- [x] **Pipeline verrijkt in `01.3-your-own-chat_jeffrey.ipynb`**:
  - `PeriodFeature` (Week/Weekend) en `ResponseTimeFeature` met 3 regels: sprekerswisseling, dag-reset, 8-uursgrens.
  - Verrijkte dataset weggeschreven naar `data/processed/chat-20260915-190537.parq` en gekoppeld in `config.toml`.
- [x] **Barbell plot ontwikkeld in `notebooks/lesson2/02.5-your_turn_jeffrey.ipynb` (Cel 8)**:
  - Halterdiagram met Ochtend, Middag, Avond op de Y-as en mediaan reactietijd (minuten) op de X-as.
- [x] **Afbeelding geëxporteerd**: Opgeslagen in `img/reactietijd_per_dagdeel_barbell.png`.

---

### [x] WOENSDAGAVOND — RUBRIC-FEEDBACK VERWERKT: ITERATIE 6 & DEFINITIEVE INLEVERING (Afgerond!)
- [x] **Feedbackpunt 1 [Preattentive & Gestalt - Score 0.75 -> 0.95]**:
  - Schwabish *Grey First* toegepast in Cel 8: concurrerend groen/blauw vervangen.
  - Partner Rick is rustig leisteengrijs (`#4A5568`), Student Jeffrey is warm terracotta accent (`#C2410C`).
  - L-kegel stimulatie (<200ms) geoptimaliseerd; Figure-Ground en Connectedness strak neergezet.
- [x] **Feedbackpunt 2 [Tekstintegratie & As-uitlijning - Score 0.80 -> 0.95]**:
  - Semantische congruentie hersteld: titel gewijzigd van *"Partner moet langer wachten"* naar *"Jeffrey reageert beduidend langzamer dan zijn partner"*.
  - As (*Reactietijd*) en titel (*reageert beduidend langzamer*) zijn nu 1-op-1 congruent. Geen cognitieve frictie meer.
- [x] **Feedbackpunt 3 [Storytelling / Context: Het 'Waarom' - Score 0.60 -> 0.95]**:
  - Subtitel verklaart avondpiek: *"Overdag zorgen docenttaken voor vertraging, maar 's avonds is de responskloof maximaal doordat de telefoon vaker blijft liggen"*.
  - Gedragscontrast blootgelegd: Rick reageert in de avond direct (0,8 min), terwijl Jeffrey kiest voor schermvrije rust.
- [x] **Feedbackpunt 4 [Statistische Verantwoording & Spreiding - Score 0.80 -> 1.00]**:
  - *Spreidingsanalyse (IQR)*: Q1-pariteit aangetoond (~18 sec voor beiden bij actieve chatsessies). Jeffrey's Q3 explodeert 's avonds naar 31,16 min ($IQR = 30,86$ min vs. Rick 15,02 min).
  - *Significantietoets*: Mann-Whitney U test toont significant verschil aan ($U = 35.772, p = 0,0135$; toevalskans slechts 1,35%).
  - *Bootstrapping (2.000 runs)*: 95% betrouwbaarheidsinterval van de avondkloof is $[0,30 \text{ tot } 3,73]$ minuten (0 ligt buiten interval).
  - Begrijpelijke methodologische voetnoot met asterisk direct in de figuur geëtst.
- [x] **Data-integriteit & noemer-audit**:
  - Verantwoording van $n=2.728$ directe reacties over 6.059 inhoudelijke berichten (2021–2026) helder vermeld.
  - Nacht uitgesloten (slaap telt niet door wegens dag-reset).
- [x] **Definitieve export & Cel 8 gereed**:
  - Hoge resolutie afbeelding opgeslagen in `img/reactietijd_per_dagdeel_barbell.png` (DPI=200, bbox_inches=tight).

---

## Hoe de visualisatie tot stand is gekomen (mijn ontwerpproces)

Hieronder leg ik in mijn eigen woorden uit hoe ik stap voor stap tot de uiteindelijke grafiek ben gekomen, welke keuzes ik heb gemaakt en hoe feedback van een klasgenoot en docent Raoul hierbij hielp:

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

### Iteratie 4: De 4-staven grafiek (Middagpiek als volume)
Die feedback vond ik ijzersterk. Ik ging terug naar 4 staven (één per dagdeel) met exact één felle WhatsApp-groene staaf en de andere drie rustig grijs. Binnen een fractie van een seconde zag iedereen direct waar het over ging. De uitsplitsing tussen Rick en mij (1.303 vs. 1.535) zette ik subtiel in het tekstballonnetje bij de pijl, en onderaan voegde ik een bescheiden verantwoording toe over de noemer (6.059 berichten).

### Iteratie 5: Van volume naar interactie — De Barbell Plot (Feedback Raoul)
In Les 2 gaf docent Raoul cruciale feedback:
> *"Het optellen van berichten is nog geen story. Iedereen slaapt 's nachts en appt 's middags. Zoek iets wat je vooraf nog niet wist door andere features toe te voegen aan de pipeline."*
- **De transformatie naar reactietijd:** In plaats van te tellen *hoeveel* we appen, ben ik gaan meten *hoe snel* we op elkaar reageren. In `01.3` heb ik een `ResponseTimeFeature` gebouwd met een dagelijkse reset (om nachtelijke slaap niet als vertraging te tellen) en een 8-uursgrens.
- **De keuze voor de Barbell plot:** Conform Les 2.3 heb ik gekozen voor een **Barbell plot** (halterdiagram) met dagdelen op de Y-as en de mediaan reactietijd op de X-as. Dit toont direct *the gap* tussen ons beiden: Rick reageert op elk dagdeel structureel sneller (in de avond zelfs in 49 seconden!), terwijl de kloof 's middags en 's avonds oploopt. Dit is een écht, verrassend en menselijk verhaal.

### Iteratie 6: De Wetenschappelijke & Visuele Fine-tuning (Rubric Feedback Raoul)
Na de formele rubric-beoordeling van Raoul zijn de 4 feedbackpunten structureel doorgevoerd:
- **Preattentive kleurhiërarchie**: Het concurrerende groen/blauw is vervangen door Schwabish *Grey First*. Rick vormt de rustige baseline in leisteengrijs (`#4A5568`), terwijl Jeffrey de actieve focus is in warm terracotta (`#C2410C`). Dit activeert de L-kegels in de retina (<200ms) zonder frictie.
- **Titel-as congruentie**: De titel sprak over "wachten" (passief/ontvanger), terwijl de as "reactietijd" meet (actief/zender). Dit dwong de lezer tot een cognitieve bocht. De nieuwe titel *"Jeffrey reageert beduidend langzamer dan zijn partner"* lijnt semantisch 1-op-1 uit met de X-as.
- **Storytelling (Het 'Waarom')**: In de subtitel is het contrast verklaard: overdag zorgen docenttaken voor vertraging, maar 's avonds is de kloof maximaal doordat Jeffrey kiest voor schermvrije ontspanning terwijl Rick direct paraat is op de bank.
- **Statistische verantwoording**:
  - *Spreiding (IQR)*: Aangetoond dat bij actieve gesprekken ($Q_1$) beiden even snel reageren (~18 sec). De avondkloof ontstaat doordat Jeffrey's $Q_3$ doorschiet naar 31,16 minuten ($IQR = 30,86$ min vs. 15,02 min bij Rick).
  - *Toevalstoets*: Tweezijdige Mann-Whitney U test ($U = 35.772, p = 0,0135$) toont aan dat het verschil significant is (slechts 1,35% toevalskans).
  - *Bootstrapping*: 2.000 iteraties leveren een 95%-betrouwbaarheidsinterval op van $[0,30 \text{ tot } 3,73]$ minuten vertraging. Nul valt buiten het interval; de avondkloof is structureel bewezen.
  - Een begrijpelijke voetnoot met asterisk is direct in de figuur geplaatst.

---

## Notities Paragraaf 1.4 ("Wat je moet noteren")

### 1. Wat stelt één rij nu precies voor?
> Eén rij is één verstuurd WhatsApp-bericht tussen Persoon A (Jeffrey/Student) en Persoon B (Rick/Partner). Aan elk bericht is een tijdstempel gekoppeld, evenals het dagdeel, de periode (week/weekend) en de berekende reactietijd tot het vorige bericht van de ander.

### 2. Hoeveel rijen ben je kwijtgeraakt, en waaraan?
> Van de 8.358 ruwe regels zijn 6.414 berichten overgebleven (afgebroken regels met enters zijn netjes samengevoegd). Tijdens het inladen zijn er maar 17 regels weggevallen (doorgestuurd berichtje met omgekeerde tijdnotatie).

### 3. Hoeveel mensen zitten er in je data?
> Precies **twee mensen**: Student (Jeffrey) en Partner (Rick). 

### 4. Welke features heb je toegevoegd, en voor welke vraag dient elk?
> We hebben de data in `01.3` verrijkt met 7 krachtige features:
> 1. **`day_part`**: Knipt de dag op in 4 blokken van 6 uur (Ochtend, Middag, Avond, Nacht).
> 2. **`is_weekend` / `period`**: Onderscheidt weekdagen (ma–vr) van weekenddagen (za–zo) om te corrigeren voor weekritmes.
> 3. **`response_time_min`**: Berekent de zuivere reactietijd in minuten met uitsluiting van reacties op jezelf, nacht-reset en 8-uursgrens (2.872 geldige interacties).
> 4. **`is_deleted`**: Markeert verwijderde berichten (29 keer).
> 5. **`only_emoji`**: Markeert berichten die enkel smileys bevatten (53 keer).
> 6. **`has_media`**: Markeert berichten met bijlagen zoals foto's/video's (394 keer).
> 7. **`has_only_media`**: Filtert losse foto's zonder tekst uit (275 keer).

### 5. Wat zit erin dat er eigenlijk niet in thuishoort?
> Automatische versleutelingstekst, 29 verwijderde berichten en 275 losse mediaberichten zonder tekst. Deze filteren we er via onze boolean-vlaggetjes netjes uit voor de inhoudelijke analyses.

---

## Notities Paragraaf 2.5.4 ("Reflect" uit het Notebook)

### 1. Veranderde het antwoord toen we van berichten tellen naar reactietijd gingen?
> **Ja, radicaal.** Bij het tellen van berichten (volume) leek het alsof Rick en Jeffrey vrijwel symmetrisch communiceerden met een gezamenlijke middagpiek. Pas toen we de interactiedynamiek (reactietijd per bericht) analyseerden, kwam het echte relationele patroon naar voren: Rick reageert de hele dag door binnen 1 minuut, terwijl Jeffrey's responstijd gedurende de dag oploopt en 's avonds verdrievoudigt.

### 2. Is er een variabele die de vergelijking kan splitsen (Simpson's Paradox)?
> **Ja, weekdag vs. weekend.** We hebben dit getoetst in `02.5-verdieping_simpsons_jeffrey.ipynb`. De avondkloof blijft op weekdagen én in het weekend dezelfde kant op wijzen (Jeffrey blijft trager), maar op weekenddagen reageren beiden overdag iets sneller. Er is dus géén sprake van een paradoxale omkering, wat de robuustheid van de hoofdconclusie bevestigt.

### 3. Zou een vreemde de conclusie binnen 30 seconden begrijpen zonder toelichting?
> **Ja.** Door de krantenkop (*"Jeffrey reageert beduidend langzamer dan zijn partner"*), de directe labeling van de bolletjes (`0,8 min` vs `2,9 min`), het preattentieve oranje accent op Jeffrey en de contextuele subtitel, ziet een lezer in minder dan 5 seconden wie er vertraagt en waarom.

### 4. Wat zou ervoor nodig zijn om van gedachten te veranderen over deze claim?
> Als uit een uitsplitsing op sessielengte zou blijken dat Jeffrey 's avonds veel langere, inhoudelijke epistels typt (hoge woordenaantallen) en Rick enkel korte bevestigingen ("is goed"). In dat geval zou de vertraging geen "niet bereikbaar zijn" betekenen, maar "meer tijd besteden aan formuleren".