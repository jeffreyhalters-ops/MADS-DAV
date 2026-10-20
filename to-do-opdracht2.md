# To-Do Lijst: Tweede Visualisatieopdracht (MADS-DAV)
*Thema: Tijdreeksen, Events & Residuen ("Time, subtract the cycle, keep the residual")*

---

## Kernprincipe & Onderzoeksvraag
> **Onderzoeksvraag:** *"Welke invloed had de reis van Rick naar Thailand (5 à 6 uur tijdsverschil) op hoeveel we appen per dag en op welke tijdstippen we elkaar berichten?"*  
> **Kernprincipe Les 3:** Dat mensen 's nachts slapen of in het weekend minder appen is geen interessante grafiek; het residu (de netto afwijking ten opzichte van wat normaal verwacht wordt) is dat wél.

---

## Roadmap & Status

### [x] 1. VOORBEREIDING & THEORIE LES 3 (Afgerond)
- [x] **Opdracht 1 afgerond:** Barbell-plot met Schwabish *Grey First*, as-congruente titel en $p=0,0135$ significantie (`img/figuur1_reactietijd_barbell.png`).
- [x] **Les 3.1 & 3.2 doorlopen:** Seizoenscycli, data-gaten expliciteren met `.reindex()`, falen van `seasonal_decompose` (70% onverklaard residu bij asymmetrische cycli) en het gevaar van overfitting met Fourier/ACF op persoonlijke chats.

### [/] 2. EIGEN CHAT & VISUALISATIE 2 (Huidige Focus in 03.3)
- [x] **Stap 2A — Data & Event:** 21 sept t/m 6 okt 2025 (Rick naar Thailand: 1 week retraite + 1 week rondreis).
- [x] **Stap 2B — Hypotheses (vooraf geformuleerd in verhalende vorm):**
  - **H1 (Volume):** *"Vooraf verwachten we tijdens de reisperiode een uitzonderlijke piek in ons dagelijkse WhatsApp-volume. Omdat we twee weken lang gescheiden zijn en elkaar niet fysiek zien, moet WhatsApp plotseling alle gesprekken vervangen die we normaal thuis aan de keukentafel of op de bank voeren. Buiten dagelijks even kort bellen hebben we geen andere communicatiemiddelen gebruikt, waardoor de chat de enige levenslijn is voor het delen van onze dagelijkse belevenissen."*
  - **H2 (Dagritme & Residu):** *"Door het tijdsverschil van 5 à 6 uur verwachten we dat ons vertrouwde dagritme compleet overhoop wordt gegooid. Waar we normaal gesproken 's avonds samen thuis zijn en weinig appen, verwachten we nu dat het zwaartepunt van onze communicatie naar de namiddag verschuift. Zodra ik in Nederland rond 07:00 of 08:00 uur ontwaak, is het bij Rick al vroeg in de middag; hij is dan al volop actief, waardoor we de dag meteen beginnen met een eerste contactmoment. De échte piek van de dag verwachten we echter tussen 15:00 en 17:00 uur Nederlandse tijd. In Thailand is het dan avond (20:00–22:00 uur) en is Rick na het eten terug op zijn hotelkamer om rustig de hele dag door te nemen voordat hij gaat slapen. Tegen de tijd dat ik 's avonds in Nederland op de bank plof (na 20:00 uur), is het in Bangkok al diepe nacht. Waar een normaal Nederlands stel 's avonds appt, verwachten we hier juist een complete radiostilte omdat Rick al slaapt."*
- [x] **Stap 2C — Twee Visualisaties Ontworpen & Uitgevoerd:**
  - **Figuur 1 (Cel 3.3.3 — Spoor A Volume):** Single panel 2025 met 14-daags voortschrijdend gemiddelde, aangescherpte titel (*"Twee weken Thailand, zeven keer zoveel appjes"*), subtitel met 4-jarige baseline, congruente stippellijn-legenda (`- - -  Normale baseline: gem. 3,5 ber./dag`), tweekleurige oranje markering (`#FB923C` spillover, `#C2410C` reisdagen), kwartalen Q1–Q4, strakke Y-as (15/30) en voetnoot. Opgeslagen: `img/figuur1_volume_2025.png`.
  - **Figuur 2 (Cel 3.3.4 — Spoor B Uur-residu):** Relatieve uuraandelen reis minus baseline (`SubtractBaseline`), aangescherpte titel (*"Reis naar Thailand gooit het vertrouwde dagritme om"*), 95%-betrouwbaarheidsband via Bootstrapping ($N = 1.000$ herhalingen), 24-uurs eerlijk gat meegenomen, Y-as (-12.2% t/m +14.8%), X-as in 4 dagdelen (*Nacht*, *Ochtend*, *Middag*, *Avond*), 3 annotaties met 95% CI (08:00 surplus +5,6%, 11:00 dal -6,2% verplaatst naar links onder nachtzone voor optimale ademruimte, 16:00 dagpiek +10,0%), avonddal leeg conform Tufte. Opgeslagen: `img/figuur2_dagritme_residu.png`.
- [x] **Stap 2D — Paragraaf 3.3.6 Inlevervragen (Reflectie voorbereid):**
  - [x] 1. Event en hypotheses letterlijk citeren (verhalend uitgewerkt).
  - [x] 2. Toetsing & falsificatie via Figuur 1 en 2 beschrijven (inclusief $N=1.000$ bootstrap-validatie).
  - [x] 3. Nulresultaat beschrijven (korte eerlijke alinea over foto-aandeel en steekproefomvang).

### [x] 3. FINETUNING, PITCH & BEOORDELING
- [x] **WCAG- & Contrastcontrole:** Titels `#1A202C` (15,3:1 AAA), tekst `#2D3748` (10,7:1 AAA), leisteengrijs `#4A5568` (7,0:1 AAA), terracotta accent `#C2410C` (5,4:1 AA), staalblauw `#2B6CB0` (5,9:1 AA).
- [x] **Beoordeling & Feedback Docent Raoul Grouls:**
  - **Cijfer Timeseries (Figuur 2 / Cel 3.3.4): 8,25**
  - **Cijfer Comparing Categories: 8,0**
  - **Feedback docent:** *"Voeg betrouwbaarheid toe aan de visualisatie via een proef met 1.000 herhalingen om te kijken of de residugrafiek nagenoeg hetzelfde blijft."*
  - **Uitvoering feedback:** Doorgerekend met $N=1.000$ permutaties ($p < 0,001$) én $N=1.000$ bootstraps. Gekozen voor Bootstrapping als 95%-betrouwbaarheidsband rondom de residulijn (Optie B), waardoor visueel en statistisch direct bewezen is dat het dagritme rotsvast standhoudt.
- [ ] **Git commit op branch `les1`:** Veilige commit met schone notebooks en geëxporteerde afbeeldingen.

---

## Onderzoeks- & Ontwerpnotities (Naslagwerk)

### 1. Kwantitatieve Resultaten (Chatdata Thailand)
| Indicator | Normale Baseline (4 jaar) | Reisperiode Thailand (16 dagen) | Conclusie & Residu |
|---|---|---|---|
| **Dagelijks Volume (H1)** | **3,5** ber./dag ($N=6.004$) | **25,6** ber./dag ($n=410$) | **+700% stijging.** Piekdag 24 sept (83 ber., all-time top 2). |
| **Ochtendsurplus (08:00 NL)** | 7,54% van dagtotaal | 13,17% van dagtotaal | **+5,63% residu.** NL ontwaakt, Rick al actief in TH (13:00). |
| **Ochtenddal (11:00 NL)** | 9,11% van dagtotaal | 2,93% van dagtotaal | **-6,18% residu.** Normale werkdag-koffiepiek blijft uit door lesgeven en middagprogramma TH. |
| **Absolute Dagpiek (16:00 NL)** | 6,88% van dagtotaal | 16,83% van dagtotaal | **+9,95% residu.** Rick na het eten in hotel vóór slapengaan (21:00 TH). |
| **Avondstilte (22:00-23:00 NL)** | 2,23% van dagtotaal | **0,00%** (exact 0 berichten) | **-2,23% residu.** Radiostilte; diepe nacht in Thailand (03:00-05:00). |
| **Foto-/Media-aandeel (Vraag 3)** | **6,21%** (373 media) | **5,12%** (21 media) | **Nulresultaat:** Reisfoto's via iCloud gedeeld; WhatsApp puur tekstvervanger. |

### 2. Belangrijkste Ontwerp-Iteraties
* **Figuur 1 (Volume 2025):**
  1. *Small multiples 2x2 verworpen:* Squashte 16 reisdagen en wekte valse suggestie dat Thailand een jaarlijks terugkerend seizoenseffect was.
  2. *Single Panel 2025 met 14-daags venster:* 14-daags venster sluit perfect aan op de 16 reisdagen (piekt op 27, passend bij het 25,6 daggemiddelde).
  3. *Tufte & Schwabish De-cluttering:* Y-as strak op 0–35 (ticks op 15 en 30), X-as op kwartalen Q1–Q4, open spines.
  4. *Spillover-flanken:* 7-daagse aan- en uitloop van het gecentreerde venster getoond in harmonieus lichtoranje (`#FB923C`), kernreis in terracotta (`#C2410C`).
  5. *Titel-aanscherping & Legenda-congruentie:* Titel verfijnd naar *"Twee weken Thailand, zeven keer zoveel appjes"* met subtitel die 4-jarige baseline noemt. De doorgetrokken em-dash `—` in de badge vervangen door `- - - ` om 100% congruent te zijn met de onderbroken stippellijn (`linestyle='--'`).
* **Figuur 2 (Uur-residu):**
  1. *Het eerlijke gat:* Alle 24 uren gemerged, zodat nul-uren (22:00 en 23:00) niet verdwijnen maar netjes dalen tot -1,5% en -0,75%.
  2. *Macro-structuur:* Y-as in stappen van 5%, X-as geclusterd in 4 dagdelen (*Nacht*, *Ochtend*, *Middag*, *Avond*).
  3. *Titel geëxpliciteerd:* *"Reis naar Thailand gooit het vertrouwde dagritme om"* met subtitel *"Verschil in aandeel berichten per uur (Nederlandse tijd) t.o.v. de 4-jarige baseline."*.
  4. *Statistische betrouwbaarheid via Bootstrapping ($N = 1.000$ herhalingen):* Doorgerekend n.a.v. feedback van Raoul. Zowel een Permutatietest ($p < 0,001$ voor alle kernuren) als Bootstrapping uitgevoerd. Gekozen voor Bootstrapping: toont een zachte 95%-betrouwbaarheidsband rondom de blauwe residulijn die bewijst dat de curve nagenoeg exact hetzelfde blijft en nergens de nullijn kruist.
  5. *Annotatie-de-cluttering & ademruimte:* Het tekstvak van het ochtenddal (11:00) verplaatst naar links (`xytext=(5.0, -8.2)`) in de vrije ruimte onder de nachtzone, met een schuine pijl naar het dal. Y-as onderaan verruimd naar `-12.2%` voor royale ademruimte.
  6. *Jupyter-padoplossing:* `Path("../../img/figuur2_dagritme_residu.png")` voorkomt `FileNotFoundError` in de notebook-kernel.

### 3. Discussiepunten voor Dinsdag (Les 4)
* **De 'Venster-Paradox' (14 vs. 30 dagen):** De 16 reisdagen hadden gemiddeld 25,6 ber./dag. Het 14-daagse venster piekt op 27 (matcht het getal), maar een 30-daags maandvenster dempt naar 17,8 (omdat het 14 normale dagen meerekent). Vraag voor Raoul: *Is het beter de highlight op de 14-daagse lijn te leggen (congruent met de annotatie), of op de 30-daagse lijn met verantwoording van de afvlakking?*
* **Toolkit-afwijking verantwoorden:** Waarom we pure Matplotlib gebruikten in plaats van `LinePlot` (omdat `goad_toolkit` geen ingebouwde segment-arcering en custom flanken ondersteunt).

### 4. Definitieve Uitwerking Inlevervragen (Paragraaf 3.3.6: What to write down)

#### Vraag 1: The event and the predicted impact — written before you plotted. Quote yourself.
* **Aanleiding en exacte periode:**  
  De reis van Rick naar Thailand van **21 september t/m 6 oktober 2025** (16 dagen: 1 week yoga/retraite gevolgd door 1 week rondreis). Door het forse tijdsverschil (5 uur in de Nederlandse zomertijd, 6 uur na wintertijdverschuiving) leefden we tijdelijk in een compleet ander dagschema. Buiten dagelijks even kort bellen verliep al ons contact via WhatsApp.

* **Hypothese 1 (Volume — verhalend geciteerd):**  
  > *"Vooraf verwachtten we tijdens de reisperiode een uitzonderlijke piek in ons dagelijkse WhatsApp-volume. Omdat we twee weken lang gescheiden waren en elkaar niet fysiek zagen, moest WhatsApp plotseling alle gesprekken vervangen die we normaal thuis aan de keukentafel of op de bank voeren. Buiten dagelijks even kort bellen hebben we geen andere communicatiemiddelen gebruikt, waardoor de chat de enige levenslijn was voor het delen van onze dagelijkse belevenissen."*  
  * **Falsificatiecriterium H1:** Als het gemiddelde dagvolume tijdens de reis niet substantieel zou afwijken van onze normale 4-jarige baseline van 3,5 berichten per dag (of zelfs zou dalen door slecht bereik of drukte), dan verwerpen we de hypothese.

* **Hypothese 2 (Dagritme & Residu — verhalend geciteerd):**  
  > *"Door het tijdsverschil van 5 à 6 uur verwachtten we dat ons vertrouwde dagritme compleet overhoop zou worden gegooid. Waar we normaal gesproken 's avonds samen thuis zijn en weinig appen, verwachtten we nu dat het zwaartepunt van onze communicatie naar de namiddag zou verschuiven. Zodra ik in Nederland rond 07:00 of 08:00 uur ontwaak, is het bij Rick al vroeg in de middag; hij is dan al volop actief, waardoor we de dag meteen beginnen met een eerste contactmoment. De échte piek van de dag verwachtten we echter tussen 15:00 en 17:00 uur Nederlandse tijd. In Thailand is het dan avond (20:00–22:00 uur) en is Rick na het eten terug op zijn hotelkamer om rustig de hele dag door te nemen voordat hij gaat slapen. Tegen de tijd dat ik 's avonds in Nederland op de bank plof (na 20:00 uur), is het in Bangkok al diepe nacht. Waar een normaal Nederlands stel 's avonds appt, verwachtten we hier juist een complete radiostilte omdat Rick al slaapt."*  
  * **Falsificatiecriterium H2:** Als het residu na aftrek van het 4-jarige ritme rond de nullijn zou blijven hangen (geen structurele verandering in uuraandelen), of als er na 20:00 uur Nederlandse tijd juist nog volop geappt zou worden, dan verwerpen we de hypothese.

---

#### Vraag 2: The plot that could have falsified it, and whether it did.

* **Toetsing Spoor A (Volume via Figuur 1 — `img/figuur1_volume_2025.png`):**  
  * **Aanpak & Verantwoording:** We hebben voor het volledige jaar 2025 een lijngrafiek gebouwd met het voortschrijdend gemiddelde over een venster van 14 dagen. Dit venster van twee weken sluit inhoudelijk exact aan op de 16 dagen van de reis. Omdat een 14-daags gecentreerd gemiddelde 7 dagen vóór en 7 dagen na de reisperiode al oploopt en uitdooft, hebben we deze wiskundige overgangsflanken expliciet geaccentueerd in lichtoranje (`#FB923C`), terwijl de werkelijke 16 reisdagen in donker terracotta (`#C2410C`) zijn gemarkeerd. De 4-jarige baseline (3,5 berichten/dag) is als benchmark aangegeven. Door het 14-daagse venster over heel 2025 te trekken, zien we direct of er andere uitschieters waren. We hebben ook naar de eerdere jaren gekeken (2022, 2023, 2024); daar waren geen vergelijkbare pieken, waardoor we die jaren niet nodeloos hebben geplot (Tufte).  
  * **Falsificatie-oordeel:** **Niet gefalsifieerd; krachtig bevestigd.** Tijdens de reis explodeert het dagvolume naar gemiddeld **25,6 berichten per dag (+700%)**, met een all-time topdag op 24 september (83 berichten). De 14-daagse rolling line piekt op 27 berichten. De uitschieter is uniek in de data en bevestigt H1 volledig.

* **Toetsing Spoor B (Dagritme via Figuur 2 — `img/figuur2_dagritme_residu.png`):**  
  * **Aanpak & Verantwoording:** Om te zien hoe het gedrag veranderde ten opzichte van een normale dag, hebben we de 4-jarige baseline berekend (de normale verdeling per uur over $N = 6.004$ berichten, zónder de reis). Deze normale cyclus hebben we met `SubtractBaseline` afgetrokken van het uuraandeel tijdens de reis. Hiermee is de reguliere dagcyclus teruggebracht naar $0\%$; wat overblijft is het pure Residu. We hebben alle 24 uren gemerged, zodat uren waarin tijdens de reis exact 0 berichten vielen (22:00 en 23:00 uur) een eerlijk negatief residu tonen (-1,48% en -0,75%) in plaats van te verdwijnen. De X-as is geclusterd in de vier dagdelen (*Nacht*, *Ochtend*, *Middag*, *Avond*).  
  * **Falsificatie-oordeel:** **Niet gefalsifieerd; tot op het uur bevestigd én statistisch gevalideerd.** Het residu is allerminst vlak, maar toont vier scherpe, inhoudelijk verklaarbare gedragsverschuivingen die met $N = 1.000$ herhalingen (bootstrapping en permutatietest) robuust standhouden:  
    1. *Ochtendsurplus (08:00 NL, +5,63% residu, 95% CI: [+2,7%, +8,8%], p < 0,001):* NL ontwaakt en Rick is in Thailand al in de vroege middag (13:00/14:00 uur) actief; direct een eerste intensief contactmoment.  
    2. *Ochtenddal (11:00 NL, -6,18% residu, 95% CI: [-7,6%, -4,2%], p < 0,001):* Onze normale werkdag-koffiepauze (normaal goed voor 9,11% van de dag) valt helemaal stil omdat ik lesgeef en Rick bezig is met middagactiviteiten in Thailand.  
    3. *Absolute Dagpiek (16:00 NL, +9,95% residu, 95% CI: [+6,5%, +13,9%], p < 0,001):* De onbetwiste hoofdpiek van de dag (16,83% van alle reisberichten). In Nederland loopt de werkdag ten einde, terwijl Rick na het diner terug op zijn hotelkamer is (21:00/22:00 uur TH) om de hele dag door te nemen voor het slapengaan.  
    4. *Avondstilte (na 20:00 NL, exact 0 berichten om 22:00 en 23:00):* Waar Nederlandse stellen normaal gesproken 's avonds op de bank appen, heerst hier een volledige radiostilte (-2,23% residu). In Bangkok is het dan diepe nacht (03:00 à 05:00 uur).

---

#### Vraag 3: One expected impact you could not find, with the sample it would have needed to show up.
* **Het Nulresultaat:**  
  Een intuïtieve verwachting vooraf was dat een verre rondreis in Zuidoost-Azië zou leiden tot een flinke toename van het percentage verstuurde foto's en video's in de chat. In de data vonden we hier echter geen enkel spoor van: het media-aandeel lag tijdens de reis met **5,12%** (21 mediabestanden op 410 berichten) zelfs iets láger dan onze normale 4-jarige baseline van **6,21%** (373 op 6.004 berichten).

* **Kwalitatieve Verklaring & Methodologische Les:**  
  Kwalitatief bleek dat Rick zijn vakantiefoto's rechtstreeks in een gedeeld iCloud-album plaatste; WhatsApp fungeerde puur als tekstuele gesprekslijn om elkaars dag door te nemen. Methodologisch illustreert dit bovendien de grenzen van persoonlijke chatdata bij zeldzame events: omdat foto's sowieso maar ~6% van alle berichten uitmaken, is een reisperiode van 16 dagen ($n = 410$) statistisch veel te klein om een subtiele procentuele verschuiving hard aan te tonen (daarvoor zou een dataset van minimaal $N \approx 3.800$ berichten nodig zijn geweest, oftewel een reis van ruim 5 maanden). Een kwantitatieve analyse toont dus scherp het volume en de tijdzoneverschuiving aan, maar vergt domeinkennis om te begrijpen waarom specifieke sub-artefacten (zoals foto's) naar andere kanalen verhuizen.
