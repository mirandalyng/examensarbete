| Nr | Låt | Artist | Fråga | Svar | Korrekt? | Avslöjar svaret? | Kommentar |
|---|---|---|---|---|---|---|---|
| 1 | Cada Vez Que Te Vas | Ladron | I vilket år släpptes den här låten? | 1997 | ja, enligt vår metadata | nej | Wikipedia saknade fakta om artisten, så reservregeln användes (årtal). Fungerade som avsett, men frågan är tråkig |
| 2 | Lovin' You | Tony! Toni! Toné! | En av medlemmarna i bandet bytte artistnamn till "Saadiq" på 90-talet. Vad betyder namnet på arabiska? | Man av sitt ord | ja | delvis | "Saadiq" ger en stark ledtråd om bandet, men följer regeln som den är skriven. Språkfel: ett av svarsalternativen: "Musikmann" ska vara "Musikman" |
| 3 | Dos Mil Trece | Zoé | Vilket år släpptes det femte studioalbumet som innehåller den här låten? | 2013 | ja | nja, svaret = låttiteln på spanska | valde bort en fråga för att den bedömde den som för svår: "Actually, let me think of something more fun/surprising. The article mentions that before the release, short clips of songs were uploaded to the official website and unlocked by tweeting a hashtag. That's a fun fact!
But that might be hard to turn into a simple multiple choice question."|
| 4 | Brokenhearted | Karmin | Koreografin till musikvideon gjordes av en person som är särskilt känd för att ha arbetat med vilken artist? | Lady Gaga | ja | nej | Orimligt svår, handlar om koreografen, inte om artisten eller låten. Valde bort: The 'cheerio' part came about when Claude Kelly asked Amy what she would say if pacing around her apartment waiting for a guy to call, she said 'Cheerio' |
| 5 | Aicha | Outlandish | Den här versionen av låten nådde förstaplats på listan i flera länder. I vilket av dessa länder blev den etta? | Tyskland | ja | nej | frågan stämmer, men konstigt att den inte nämns som ett i Danmark eftersom dem kommer från Danmark?|
| 6 | Mentiras | Selena y los Dinos | Vilken känd japansk låt från 1960-talet spelades in på spanska som en av singlarna från samma album? | Sukiyaki | ja | nej | Källa: Wikipedia "List of songs recorded by Selena". Handlar om en annan låt på albumet, inte om Mentiras. Agenten undvek medvetet "Ue o Muite Arukō" som felaktigt alternativ, eftersom det är samma låt. En intressant skillnad mot fråga 5: här kontrollerade agenten ett felaktigt alternativ och strök det, eftersom den visste att det var samma låt under ett annat namn. Den gör det alltså när den själv ser risken, men inte systematiskt. Det stärker förslaget att kräva det i prompten. |
| 7 | Suelo Soñar, Correr y Tropezarme | Gera MX | På vilken plats rankades artisten på Rolling Stones lista över de 50 bästa spanskspråkiga rapparna genom tiderna? | 37 | ja | nej (ledtråd: spanskspråkig rappare) | Källa: Wikipedia "Gera MX". En rankingsiffra går bara att gissa. Valde bort "Vad står MX för?" (Mexiko), som var lättare och roligare |
| 8 | Miss You | Louis Tomlinson | I vilken brittisk tv-shows final framförde artisten låten live för första gången? | The X Factor | ja | nej: (ledtråd: X Factor -> ONe direction) | Källa: Wikipedia "Miss You (Louis Tomlinson song)". Bra exempel: om låten, rimligt svår, fans kan resonera sig fram. Exempel i prompten till v2: "A good question is about the song or artist and can be reasoned out by a fan, like: [fråga 8]. |
| 9 | Show | Karpe | I vilket lands version av Coke Studio blev gruppen den första skandinaviska akten att medverka i? | Pakistan | ja | nej (ledtråd: skandinavisk) | Källa: Wikipedia "Karpe". "Sverige" kan uteslutas av logik. Valde bort namnbytet Karpe Diem → Karpe (2018), som fans kan svara på. Undvek ett "känsligt ämne" (avslutad karriär) enligt reglerna. Alternativet "Vad hette gruppen innan 2018?" hade fungerat som fråga 8, eftersom en fan vet svaret direkt. Agenten valde "mest överraskande" en gång till. |
| 10 | The Dragon Lies Bleeding | HammerFall | I vilken stad spelades liveversionen av denna låt in, som finns med som bonusspår på livealbumet One Crimson Night? | Guadalajara, Mexiko | ja | nej | Källa: Wikipedia "One Crimson Night", avsnittet Production. Agenten resonerade ut spårnumret själv. Mycket svår fråga. |


## Resultat v1
- **Korrekta:** 10/10 (fråga 1 enligt metadata, inte Wikipedia)
- **Avslöjar:** 0 helt, 1 delvis (2: medlemsnamn), 1 nja (3: svaret = låttiteln på spanska)
- **Ledtrådar om artisten:** 3 (7, 8, 9)
- **Bra frågor** (om låten/artisten, fans kan svara): 1 (fråga 8)
- **Orimligt svåra eller handlar inte om låten:** 4 (4, 6, 7, 10)
- **Årtalsfrågor:** 2 (1, 3). Användaren har redan valt decennium, så de blir nästan gratis

## Mönster
1. Agenten väljer den mest "överraskande" faktan i stället för den en fan kan svara på. I 4 av 10 fall fanns ett bättre alternativ i samma text (Cheerio, MX = Mexiko, Karpe Diem, hashtag-smakprov).
2. Felaktiga alternativ kontrolleras inte systematiskt (5 rätt av tur, 9 "Sverige" kan uteslutas).
3. Regeln om namn tolkas olika: en annan låttitel undveks i 7 men användes i 6.
4. Agenten fyller ibland i från minnet (Glory to the Brave, Coke Studio "Indien"), men det har inte påverkat något svar.
5. Tabeller (listplaceringar, låtlistor) når inte agenten, eftersom explaintext=1 tar bort dem.

## Slutsats
Kriterierna korrekt + avslöjar inte räcker inte. Inför ett tredje kriterium från v2:
**Rimlig svårighet:** frågan handlar om låten eller artisten, och en fan har en rimlig chans att svara.

# Förslag på ändring av prompt:
Your job is to create ONE follow-up question about the artist or the song that a fan of the artist would enjoy and have a fair chance to answer. Prefer facts about the song itself or the artist's own career over facts about other people around them (producers, choreographers, other songs).

Good example: "I vilken brittisk tv-shows final framförde artisten låten live för första gången?" (a fan can reason it out).
Bad example: "Koreografen till musikvideon är känd för att ha arbetat med vilken artist?" (about another person, only guessable).

Om användaren valt decennium blir årtal lättare:
- If you cannot find a confirmed fact, ask about the album or the genre instead. Do not ask about the release year.