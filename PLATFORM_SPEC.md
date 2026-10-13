# QORGAU — product, UX and implementation specification

**Audience:** product, design, engineering, legal and survivor-support teams  
**Status:** implementation brief; legal and hotline details require named local owners and recurring verification  
**Languages:** қазақша (kk), русский (ru)  
**Product posture:** private-by-default, survivor-led, accessible on a low-end phone, useful without an account

> **Safety framing:** This service provides information and pathways to human support. It is not an emergency dispatch service, legal representation, a clinical assessment, or a guarantee of anonymity. Never imply that browsing history, ISP logs, device monitoring, screenshots, or service-provider logs can be reliably erased by a website.

## Prototype implementation status — 13 October 2026

The current first implementation pass updates the existing static site and Django trusted-contact app:

- Replaced Google navigation on Quick Exit with a same-origin neutral recipe page; removed remote font loading and added `no-referrer`. The UI does not claim that device or browser traces are erased.
- Added a six-question, bilingual KK/RU safety check with local-only answers and non-diagnostic urgency guidance. Skipped or uncertain answers cannot lower the result.
- Removed unsupported service statistics and hid stale Article 147/115 text pending legal review. Added the current Article 115-1 reference and a link to the official code.
- Added a local complaint draft preview/download. It does not submit data, and warns that downloaded files may remain on the device.
- Stopped checklist persistence in local storage and removed the external form endpoint. The support form is not available until a verified, privacy-reviewed service exists.
- Disabled the trusted-contact UI and Django delivery endpoints. They previously returned demo verification codes and claimed messages were sent without sending them. Existing database records are not automatically deleted; decide retention and deletion with the data owner before production.
- Added platform security guidance and a link to the official Gov.kz crisis-centre list. This is not yet a maintained in-app regional directory or map; users are told to call first and verify availability.

**Still required before launch:** full-site Russian localization and professional Kazakh copy review; current regional directory ownership and verification; complete Instagram/Telegram/WhatsApp/TikTok guidance review; a survivor-reviewed risk rule set; secure human support workflow; backend security headers, logging/data-retention policy and independent review; accessibility and device/browser review. The current implementation is a working prototype, not a production-ready zero-trace or encrypted service.

## 1. Product decisions and critical corrections

1. **Quick exit is a navigation aid, not erasure.** A button can open a neutral page and clear this app's in-memory state, but cannot guarantee deletion of browser history, network logs, downloads, screenshots, or monitoring software. Do not silently redirect or claim “no trace.” Offer a safe-device note and a neutral exit page; do not clear saved evidence without the user's deliberate action.
2. **Masking mode is a risk-managed option.** Replacing visible content with a neutral recipe page can reduce casual shoulder-surfing, but may raise risk if a person expects the original site. Explain what it changes, provide a fast reversible switch, avoid pretending it conceals network/device activity, and never label it “invisible.”
3. **Emergency contacts:** 102 is police; 103 is ambulance; 112 is the unified emergency number. 111 is the government contact center for family, women and children's rights; 150 is a helpline for people experiencing violence. Do not characterize 111/150 as dispatch. Verify operator availability, cost, language, and channels before publishing. Current official references are listed in §10.
4. **Legal generator:** Kazakhstan's Criminal Code includes Article 115-1 “Stalking” (Статья 115-1. Сталкинг). The tool must quote or link to the current official text, help describe facts, and avoid asserting that conduct meets the offence elements or promising admissibility/outcomes. Keep legal copy versioned and reviewed by Kazakhstan counsel.
5. **No account by default.** Risk answers and evidence inventories stay in the browser unless the user explicitly chooses export or a support contact. Do not create a central victim registry, analytics profile, or automatic report submission.
6. **Existing implementation note:** the workspace currently has a large static `index.html`/`style.css` and a Django `trusted_network` app. Treat this brief as a target architecture, not a claim that present features already meet these controls. Audit current storage, authentication, logging, SMS and third-party dependencies before production.

## 2. Information architecture

### Global shell

- Persistent compact header: QORGAU wordmark; language toggle (ҚАЗ / РУС); **Leave this page**; **Neutral view** toggle with explicit label and state.
- On mobile, emergency action remains reachable but must not be the visually dominant control except on an emergency-focused page.
- Footer: privacy in plain language; accessibility; source/update dates; feedback route; “This site cannot see or erase activity on your device/network.”

### Sitemap

```text
/
├── Home / Immediate options
│   ├── Call emergency services (102 / 112 / 103)
│   ├── Talk to support (111 / 150)
│   ├── Quick safety plan
│   └── Risk check (optional, local-only)
├── Safety check
│   ├── Six questions
│   ├── Results: urgent / elevated / lower-indicated
│   └── Personalized next steps + print/save/clear controls
├── Make a safety plan
│   ├── Today / next 24 hours
│   ├── Safe people and code word
│   └── Leaving / shelter considerations
├── Keep records
│   ├── Evidence checklist
│   ├── Incident timeline (local-only)
│   └── Export / delete locally
├── Report and legal information
│   ├── What Article 115-1 says (official link + review date)
│   ├── Describe what happened (neutral prompts)
│   ├── Draft complaint (download locally; no auto-submit)
│   └── Get legal help
├── Secure your accounts and devices
│   ├── Instagram / Telegram / WhatsApp / TikTok guides
│   ├── Account access and location sharing
│   ├── Unknown trackers and device safety
│   └── If changing settings could alert someone
├── Find support
│   ├── National hotlines
│   ├── Region selector and crisis-centre directory
│   └── Legal / psychological / shelter filters
├── Contact support (optional, consent-first)
├── About / how this works
├── Privacy and data controls
└── Neutral view (recipe content; no account or incident state displayed)
```

## 3. Key flows

### A. Immediate danger

Home → user chooses “Someone is here / I may be hurt now” → plain instruction to move toward a safer public/locked place if possible → buttons `Call 102`, `Call 112`, `Call 103` → one short call-preparation prompt (location, immediate danger, injuries) → optional “I can’t call safely” support alternatives. Do not require completing the risk check first.

### B. Risk check

Intro and skip → six one-at-a-time questions → local scoring → result with non-diagnostic wording → action plan → review/clear answers. Always show emergency options regardless of score. The score cannot rule out danger.

### C. Evidence and complaint draft

Choose evidence type → preservation steps → optional incident notes stored locally → choose “Create a draft” → preview with explicit legal caveat → download as PDF/DOCX/text generated in browser where possible → user decides whether/when to share. Never auto-email, upload evidence, geotag, or submit to police.

### D. Find a service

Choose region → show verified entries with service type, languages, hours, phone, address-publicity caveat and last-checked date → tap-to-call / open official route. Avoid exposing a user's live location by default; manual region selection first. Map is optional; accessible list is primary.

## 4. Kazakh and Russian UX copy

Copy below is a safe starting point for professional localization. Keep sentence structure short. Have fluent Kazakh and Russian survivor-support reviewers validate tone, legal terminology, and dialect/region comprehension before launch.

### Home / hero

**KK title:** Қазір сізге қандай көмек керек?  
**KK body:** Сізге не істеу керегін өзіңіз таңдайсыз. Жауаптарыңыз аккаунтсыз да осы құрылғыда қалуы мүмкін. Қауіп дәл қазір төніп тұрса, 102 немесе 112 нөміріне қоңырау шалыңыз.  
**KK actions:** `Қазір қауіп төніп тұр` · `Қолдау қызметімен сөйлесу` · `Қауіпсіздік жоспарын жасау` · `Қауіпсіздікті тексеру`

**RU title:** Какая помощь вам нужна сейчас?  
**RU body:** Вы сами выбираете, что делать дальше. Ответы можно оставить на этом устройстве без создания аккаунта. Если опасность непосредственная, позвоните 102 или 112.  
**RU actions:** `Мне угрожает опасность сейчас` · `Поговорить со службой поддержки` · `Составить план безопасности` · `Оценить ситуацию`

### Emergency and support bar

**KK:** `Полиция — 102` · `Бірыңғай шұғыл қызмет — 112` · `Жедел жәрдем — 103` · `111 — отбасы, әйелдер мен балалар мәселелері бойынша байланыс орталығы` · `150 — зорлық-зомбылыққа тап болған адамдарға арналған сенім желісі`. `Қоңырау шалу`  
**RU:** `Полиция — 102` · `Единый номер экстренной помощи — 112` · `Скорая помощь — 103` · `111 — контакт-центр по вопросам семьи, женщин и детей` · `150 — линия доверия для людей, столкнувшихся с насилием`. `Позвонить`

### Quick exit and neutral view

**KK exit label:** `Беттен тез шығу`  
**KK helper:** `Бейтарап бетке өтеді. Бұл браузер тарихын немесе құрылғыдағы іздерді өшірмейді.`  
**KK neutral toggle:** `Бейтарап көрініс` / `Көмек бетіне қайту`  
**RU exit label:** `Быстро уйти со страницы`  
**RU helper:** `Откроется нейтральная страница. История браузера и данные на устройстве не удаляются.`  
**RU neutral toggle:** `Нейтральный вид` / `Вернуться к помощи`

### Risk check: six prompts

Use **Yes / No / Not sure / Skip** (KK: `Иә / Жоқ / Сенімді емеспін / Өткізу`; RU: `Да / Нет / Не уверена(ен) / Пропустить`). Avoid asking for names, precise address, or perpetrator identity.

| # | Қазақша | Русский |
|---|---|---|
| 1 | Қазір ол адам сізге жақын жерде ме немесе сізге жетуге тырысып жатыр ма? | Этот человек сейчас рядом или пытается добраться до вас? |
| 2 | Ол сізді өлтіремін, жарақаттаймын немесе өзіне/басқаға зиян келтіремін деп қорқытты ма? | Он угрожал убить или ранить вас либо причинить вред себе или кому-то ещё? |
| 3 | Жақында сізді итерді, ұрды, қамады, жолыңызды бөгеді немесе келісіміңізсіз жыныстық әрекет жасады ма? | В последнее время вас толкали, били, удерживали, перекрывали вам путь или совершали сексуальные действия без вашего согласия? |
| 4 | Қудалау жиілеп, күшейіп немесе үйіңізге, жұмысыңызға не оқуыңызға дейін жетті ме? | Преследование участилось, стало интенсивнее или дошло до вашего дома, работы или учёбы? |
| 5 | Ол адам сіздің орналасқан жеріңізді, аккаунттарыңызды немесе құрылғыларыңызды бақылауы мүмкін деп ойлайсыз ба? | Вы думаете, что этот человек может отслеживать ваше местоположение, аккаунты или устройства? |
| 6 | Қазір өзіңізді қауіпсіз жерге бара аламын немесе сенімді адамға хабарласа аламын деп сезінесіз бе? | Можете ли вы сейчас попасть в безопасное место или связаться с человеком, которому доверяете? |

### Risk results (non-diagnostic)

Do not expose a numeric score or call it a validated assessment until one has been independently validated with local specialists. Use transparent rules: any current proximity, credible severe threat, recent assault/confinement/sexual violence, or inability to reach safety escalates to urgent guidance. Multiple escalation indicators produce elevated guidance. Otherwise show lower-indicated, never “safe.” “Not sure” and skipped responses must not lower urgency.

**KK urgent:** `Қазір шұғыл көмек керек болуы мүмкін.` `Егер қауіп жақын болса, тестті тоқтатып, қауіпсіз орынға өтіңіз және 102 немесе 112 нөміріне қоңырау шалыңыз. Жарақат болса — 103. Қоңырау шалу қауіпті болса, сенімді адамнан көмек сұраңыз.`  
**RU urgent:** `Вам может понадобиться срочная помощь.` `Если опасность рядом, прекратите тест, по возможности перейдите в безопасное место и позвоните 102 или 112. При травме — 103. Если звонить небезопасно, попросите помощи у человека, которому доверяете.`

**KK elevated:** `Жағдайды байыппен жоспарлаған жөн.` `Сенімді адамға айтыңыз, қауіпсіздік жоспарын жасаңыз және қолдау қызметіне хабарласыңыз. Жағдай өзгерсе, кез келген уақытта шұғыл көмекке жүгініңіз.`  
**RU elevated:** `Стоит заранее продумать безопасность.` `Расскажите человеку, которому доверяете, составьте план безопасности и свяжитесь со службой поддержки. Если ситуация изменится, обращайтесь за экстренной помощью в любое время.`

**KK lower-indicated:** `Жауаптарыңызда шұғыл қауіп белгісі байқалмады, бірақ бұл қауіп жоқ дегенді білдірмейді.` `Қаласаңыз, оқиғаларды тіркеп, құпиясөздер мен орналасқан жер бөлісу параметрлерін тексеріңіз. Күмәніңіз болса, маманмен сөйлесіңіз.`  
**RU lower-indicated:** `По вашим ответам явных признаков немедленной опасности не выявлено, но это не означает, что риска нет.` `При желании фиксируйте события и проверьте пароли и передачу геопозиции. Если сомневаетесь, поговорите со специалистом.`

### Evidence checklist

**KK heading/body:** `Оқиғаларды өзіңізге қауіпсіз тәсілмен тіркеңіз.` `Хабарламаның толық контекстін, аккаунт атауын және күнін сақтаңыз. Түпнұсқаны өзгертпеңіз. Көшірмені сізден басқа адам кіре алмайтын жерде сақтаңыз. Жазба жасау заңдылығы туралы күмән болса, заңгерден кеңес алыңыз.`  
**RU heading/body:** `Фиксируйте события способом, который безопасен для вас.` `Сохраняйте полный контекст сообщения, имя аккаунта и дату. Не изменяйте оригинал. Храните копию там, куда другой человек не имеет доступа. Если сомневаетесь в законности записи разговора, сначала посоветуйтесь с юристом.`

Checklist items: original unedited files; date/time and timezone as displayed; platform/account/source; brief factual incident note; witnesses and publicly visible context; secure second copy if safe; chain-of-custody notes if handed to a professional. Warn users not to confront someone to obtain evidence, trespass, install tracking tools, or put themselves at risk. A screenshot/export is a lead, not a promise of court admissibility.

### Legal information and complaint draft

**KK:** `Бұл құрал оқиғаларды ретімен сипаттауға көмектеседі. Ол заңгердің кеңесін алмастырмайды және арызды автоматты түрде жібермейді. Құқықтық баға мен істің нәтижесін уәкілетті органдар анықтайды.`  
**RU:** `Этот инструмент помогает последовательно описать события. Он не заменяет консультацию юриста и не отправляет заявление автоматически. Правовую оценку и решение по делу принимают уполномоченные органы.`

Form labels: `Арыз берілетін орган (белгілі болса)` / `Орган, куда подаётся заявление (если известно)`; `Оқиға күні мен орны` / `Дата и место события`; `Не болды? Тек өзіңіз көрген/естіген фактілерді жазыңыз` / `Что произошло? Опишите факты, которые вы лично видели или слышали`; `Бұған дейінгі оқиғалар` / `Предыдущие эпизоды`; `Қандай материалдар бар?` / `Какие материалы имеются?`; `Қандай көмек сұрайсыз?` / `О какой помощи просите?`; `Жобаны жүктеу` / `Скачать черновик`; `Мәліметтерді тазалау` / `Очистить данные`.

Generator uses neutral first-person factual language and a configurable current legal reference, with no preselected offence or fabricated article citations. Any Article 115-1 mention is reviewed by counsel. Offer a blank template if the person does not wish to disclose identifying details.

### Account/device safety

**KK:** `Кейбір өзгерістер басқа адамға хабарлануы немесе күдік туғызуы мүмкін. Қауіпсіз құрылғыны пайдалану мүмкіндігін қарастырыңыз. Қадамды орындау қауіпті болса, тоқтап, маманмен кеңесіңіз.`  
**RU:** `Некоторые изменения могут отправить уведомление другому человеку или вызвать подозрение. По возможности используйте безопасное устройство. Если этот шаг может быть опасен, остановитесь и посоветуйтесь со специалистом.`

## 5. Functional specification

### Frontend

- Responsive, mobile-first progressive web app; core pages render without JavaScript; service worker caches only static public help content, never form answers, evidence or identifiers.
- KK/RU content is authored as keyed locale resources, not machine-translated at runtime. Persist language only in session/local preference after explaining shared-device risk; provide visible reset.
- Accessibility target: WCAG 2.2 AA; semantic landmarks; keyboard operation; visible focus; 44px minimum touch targets; screen-reader announcement of question/result; no color-only risk meaning; reduced motion; zoom/reflow; plain language.
- Risk check is a client-side rules engine with published explanation and version. Answers are memory-only by default; session persistence is optional and explicit. Clear on leave, with warning that browser/device traces may persist.
- Quick exit opens neutral content in same tab, uses `location.replace` when supported, drops in-memory app state and avoids adding app-controlled history entries. Do not claim browser history is cleared. Provide configurable destination with a safe default.
- Recipe neutral view should be a self-contained, ordinary-looking neutral page. It must not request geolocation, notifications, permissions, or remote recipe assets. No user status appears there.
- PWA install is optional and never prompted during acute-risk flows. Offline message distinguishes cached guidance from live contacts; emergency numbers work without app network only if phone has connectivity.
- Hotline links use `tel:` and are manually tested on common mobile devices; desktop fallback displays number and copy action.
- Regional directory works as a list-first interface with manual region selection, accessible filters, no geolocation until explicit consent, source attribution and last verification timestamp.
- User can export locally generated notes and permanently clear app-controlled local data; explain browser downloads and backups may remain.

### Backend/API

- Public content and risk-check pages should not require account/login. Separate public read-only content API from optional support case API.
- Directory schema: service ID, region, type, address visibility policy, public phone, text/contact channel, languages, hours, eligibility, accessibility notes, source URL, verified-by, verified-at, review-due-at, status. Hide overdue/unverified records or label clearly; provide a steward workflow.
- Complaint draft is generated client-side from user-entered facts. If server generation is unavoidable, use an ephemeral endpoint: no request-body logging, no persistence, strict TTL and explicit consent; delete generated artifacts after download.
- Anonymous assistance form is **not anonymous merely because name is optional**. Offer a no-contact resource flow first. If user chooses contact: consent language, preferred safe channel/time, minimum fields, avoid file upload in v1, provide non-sensitive reference token, retention/deletion policy, human responder access control and clear response-time limits. Never promise end-to-end encryption unless independently implemented and reviewed.
- Trusted contacts are opt-in and distinct from anonymous support. Never auto-notify or activate threat logging. SMS verification does not prove a contact is safe; notification preview can reveal sensitive details. Confirmation, quiet hours, revoke, test mode, rate limits and abuse handling are required.
- No victim identifiers or assessment answers in analytics. If operational metrics are necessary, use aggregate counts with small-cell suppression and no IP/device identifiers.

## 6. Security and privacy requirements

### Threat model

Protect against an abusive partner/family member with shared device/account access; account takeover; malicious third-party scripts; compromised hosting/admin account; accidental disclosure through notifications, downloads, logs, referrals and support workflows; and service-directory abuse. The platform cannot protect a device already controlled by spyware or guarantee safety from an in-person threat.

### Minimum controls before collecting sensitive data

- Data minimization, local-first storage, no third-party advertising, trackers, session replay, remote fonts, social embeds or nonessential analytics on sensitive routes.
- TLS everywhere; HSTS; CSP with strict script allowlist/nonces; `frame-ancestors 'none'`; `Referrer-Policy: no-referrer`; `Permissions-Policy` deny-by-default; secure same-site cookies if accounts exist; CSRF protection; output encoding; dependency pinning/SBOM and routine patching.
- Redact query strings and request bodies from access/error logs. Consider whether IP logging is necessary; document retention and access. Do not place names, answers or evidence in URLs.
- Encrypt server-held personal data at rest; keys managed separately; staff least privilege and audited access; backups encrypted and subject to deletion/retention. Separate contact data from case content.
- No plaintext SMS codes in database or logs; use a keyed hash for verification tokens, short expiry, attempt limits and abuse controls. Avoid unsalted SHA-256 for phone lookup: telephone numbers have a small guessable space. Prefer keyed HMAC and strict access controls—or do not retain the number after verification if functionality allows.
- Incident response, breach notification process, security contact, regular independent testing and a documented data inventory before pilot.
- Disable browser persistence by default for sensitive answers; use `Cache-Control: no-store` on any server-rendered sensitive response; service worker explicitly excludes such routes and API calls.
- Directory moderation and admin access require MFA, audit trail, provenance and dual review for crisis contact changes.
- Provide user-facing data map: what stays on device, what reaches the server, how long it is kept, who can read it, and how to delete it.

### Kazakhstan compliance gates

Have Kazakhstan privacy counsel confirm applicability and implementation under the current Law on Personal Data and their Protection, including consent, purpose limitation, storage/localization, cross-border transfer, retention, access/correction/deletion, children, and processor contracts. Validate hosting/data location and any support-provider transfers before collecting personal data. Have counsel review Criminal Code, Criminal Procedure Code, police complaint language, electronic evidence guidance, and translations at release and after amendments. This spec is not legal advice.

## 7. Risk-check scoring and safety governance

- A licensed/local violence-risk specialist and survivor advisory panel must approve the rule set and action plans before release.
- User answers are not a clinical, forensic or validated lethality assessment. Do not show “low risk” or “you are safe.” Use urgency-oriented language only.
- Immediate-danger flags: present perpetrator/attempt to reach, credible serious threat, recent physical restraint/assault/sexual violence, or cannot reach safety. These trigger urgent actions regardless of total score.
- Elevated guidance may be triggered by escalation, unwanted location/account monitoring, repeated unwanted pursuit, or uncertainty; never down-rank a user because they skipped or are unsure.
- Include “I don't want to answer” and an always-visible exit. No forced narrative. Do not store score for product analytics.
- Review decision logic after pilot feedback and annually at minimum; keep version/date and a rollback procedure.

## 8. Delivery phases and acceptance criteria

### Phase 0 — readiness

Legal review; survivor safety review; threat model; verify hotline contacts and crisis centre directory; data inventory; platform/security architecture; localization review.

### Phase 1 — static support MVP

KK/RU home, verified call links, risk guidance, safety plan, local-only evidence checklist, legal-information page, platform-specific security guides, accessible regional service list, neutral page, clear privacy notices. No account, evidence upload or contact form.

### Phase 2 — optional user-controlled tools

Local complaint draft/export, locally stored incident timeline with clear/export, optional human support request after privacy and operational service are ready. Threat-model each new feature before launch.

### Acceptance checklist

- User can reach call actions in one tap and skip all assessment questions.
- No assessment/evidence payload reaches backend, analytics, URLs, service worker cache, logs or third parties in the static MVP (verify with network inspection).
- Risk messages never state the user is safe or guarantee a legal outcome.
- “Quick exit” disclosure accurately states browser/device traces may remain.
- KK and RU parity is complete and reviewed by fluent humans.
- Offline cached pages clearly mark phone/directory facts as requiring live verification.
- Keyboard and screen-reader users can complete all flows; WCAG audit has no critical blockers.
- Hotline directory has named owner, sources, date checked and alert for overdue review.
- Security review confirms headers, dependency inventory, no unnecessary third-party scripts, and safe logging.

## 9. Maintenance and ownership

- Hotline/service directory owner checks contact availability monthly and after public policy changes; each entry records source and verification date.
- Legal owner checks official code at each release and on legislative amendments; display “Reviewed on” date.
- Security owner maintains incident response, dependencies, access reviews and yearly external assessment.
- Survivor-support lead owns tone, escalation language, referral quality and a route for safely reporting errors.
- Any withdrawal of a hotline/service is deployed promptly; stale or unverified contacts are hidden rather than presented as current.

## 10. Sources to verify at implementation

- Kazakhstan emergency service numbers, official Gov.kz page updated 2026-08-03: [Emergency service contacts](https://www.gov.kz/situations/729/1519?lang=ru)
- Gov.kz guidance on domestic violence support, updated 2026-10-07; includes 102, 103, 111, 150 and crisis centres: [Where to apply in case of domestic violence](https://www.gov.kz/situations/677/1395?lang=ru.)
- Official Adilet Criminal Code, Article 115-1: [Criminal Code of the Republic of Kazakhstan](https://adilet.zan.kz/rus/docs/K1400000226)
- Government information on the 150 helpline and crisis centres: [Family policy and support](https://www.gov.kz/org/din/activities/1956)

**Source discipline:** hotline operations, charges, language availability, regional capacity, law text and amendments can change. The production directory must link to primary sources and display the latest manual verification date. Recheck before launch.
