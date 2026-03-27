# Category Modules Reference

Fullständig katalog: varje projektkategori med alla tillgängliga moduler,
deras beroenden, och vilka onboarding-signaler som aktiverar dem.

> Viktigt: den här filen är en **referenskatalog + roadmap**, inte en garanti om
> att varje modul nedan redan är fullt wired i `engines/forge_engine.py`.
> Kärnmodulerna och de vanligaste signalerna är runtime-stödda; vissa övriga
> moduler här är fortfarande planeringsnivå för framtida waves.

---

## Gemensamma moduler (alla kategorier)

| Modul | Alltid | Beskrivning |
|-------|--------|-------------|
| `foundation` | ✅ | Projektsetup, filstruktur, beroenden, config |
| `design-system` | ✅ | Färger, typografi, spacing, baskomponenter |
| `deploy` | ✅ | Build, optimering, deployment |

---

## Website

| Modul | Aktiveras av | Beroenden |
|-------|-------------|-----------|
| `pages` | Alltid | design-system |
| `contact-form` | "formulär", "kontakt", "contact" | pages |
| `seo` | Alltid för websites | design-system |
| `blog` | "blogg", "artiklar", "nyheter" | pages |
| `gallery` | "bilder", "galleri", "portfolio" | pages |

---

## Booking

| Modul | Aktiveras av | Beroenden |
|-------|-------------|-----------|
| `booking-catalog` | Alltid för booking | design-system |
| `booking-calendar` | Alltid för booking | booking-catalog |
| `payment` | "betala", "pay", "online" | booking-calendar |
| `whatsapp` | Plats: Afrika, Zanzibar | design-system |
| `multilingual` | Flera språk detekterade | pages |
| `seo` | Alltid | design-system |

---

## E-Commerce

| Modul | Aktiveras av | Beroenden |
|-------|-------------|-----------|
| `product-catalog` | Alltid för e-commerce | design-system |
| `cart` | Alltid för e-commerce | product-catalog |
| `checkout` | Alltid för e-commerce | cart |
| `order-management` | "hantera ordrar" | checkout |
| `shipping` | "frakt", "leverans" | checkout |
| `seo` | Alltid | design-system |

---

## Web App

| Modul | Aktiveras av | Beroenden |
|-------|-------------|-----------|
| `auth` | "inlogg", "konto", "login" | design-system |
| `dashboard` | Alltid för web-app | auth |
| `data-management` | Alltid för web-app | dashboard |
| `notifications` | "notiser", "meddelanden" | auth |
| `settings` | "inställningar" | auth |

---

## SaaS

| Modul | Aktiveras av | Beroenden |
|-------|-------------|-----------|
| `auth` | Alltid för SaaS | design-system |
| `onboarding` | Alltid för SaaS | auth |
| `dashboard` | Alltid för SaaS | auth |
| `billing` | Alltid för SaaS | auth |
| `admin` | "admin", "roller" | auth |
| `api-keys` | "API", "integration" | auth |

---

## Tool

| Modul | Aktiveras av | Beroenden |
|-------|-------------|-----------|
| `input-handler` | Alltid för tool | foundation |
| `processing` | Alltid för tool | input-handler |
| `output-renderer` | Alltid för tool | processing |
| `cli-interface` | CLI-verktyg | foundation |
| `web-interface` | Webb-baserat | design-system |

---

## Signal-aktiverade moduler (kategorioberoende)

| Modul | Signal | Beskrivning |
|-------|--------|-------------|
| `whatsapp` | Plats i Afrika/Mellanöstern | WhatsApp-kontaktknapp |
| `multilingual` | Flera språk | Språkväxlare + översättningsstruktur |
| `seo` | Website/Booking/E-commerce | Meta, OG, sitemap |
| `analytics` | "statistik", "analytics" | GA4 eller Plausible |
| `cookie-consent` | EU-baserad målgrupp | GDPR-banner |

---

## Designsystem-derivering

### Känsla → Design

| Känsla | Primärfärg | Font | Knappar | Border-radius |
|--------|-----------|------|---------|---------------|
| Professionell | #1E40AF | Inter | Rounded | 0.5rem |
| Lekfull | #7C3AED | Nunito | Pill | 1rem |
| Lyxig | #1C1917 | Playfair Display | Square | 0 |
| Minimal | #18181B | Inter | Square | 0.25rem |
| Varm | #B45309 | Merriweather | Rounded | 0.5rem |
| Trygg | #1E40AF | Source Sans 3 | Rounded | 0.5rem |

### Färgord → Palette

Användarens färgord överskriver känsla-paletten:
blå → #2563EB, röd → #DC2626, grön → #16A34A, svart → #18181B,
lila → #7C3AED, guld → #B45309, turkos → #0D9488, orange → #EA580C

### Plats → Kontextjusteringar

| Plats | Justeringar |
|-------|------------|
| Zanzibar/Afrika | WhatsApp-modul, mobile-first, lätta assets |
| Sverige | Swish som betalalt., svenska som default |
| Global | Engelska, multi-currency om betalning |
