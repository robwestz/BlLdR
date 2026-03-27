# Memory: Booking Projects

## Scars

### Scar: Clickable unavailable slots
**When:** Building the booking calendar
**What happened:** Rendered all time slots as clickable without checking availability
**Consequence:** Users selected unavailable slots, got errors after filling the whole form. Extremely frustrating.
**Now we:** Unavailable slots are visually distinct AND non-interactive. Users never start booking an unavailable slot.

### Scar: Payment before flow
**When:** Payment integration
**What happened:** Went straight to Stripe integration before the booking flow existed
**Consequence:** Built payment for a flow that didn't exist. Had to rewire everything when the actual flow differed.
**Now we:** Complete booking flow with mock payment first. Integrate real payment only after the flow works end-to-end.

### Scar: Missing currency
**When:** Package pricing display
**What happened:** Displayed prices without currency symbol or locale formatting
**Consequence:** "200" — dollars? Shillings? Euros? Users were confused and bounced.
**Now we:** Prices always include currency symbol, formatted for the target locale.

## Insights

### Insight: Three-step funnel
**When:** Booking flow design
**What worked:** Choose Package → Select Date/Time → Confirm & Pay. Three steps, no more.
**Why:** Users understood where they were and what came next. High completion rate.
**Apply:** Booking is a funnel. Each step is one clear action. Progress indicator visible.

### Insight: Visual availability
**When:** Calendar component
**What worked:** Available dates interactive, sold-out dates grayed but visible
**Why:** Users saw slots filling up (gentle urgency). Never tried to book unavailable dates.
**Apply:** Calendar shows all dates. Only available ones are clickable. Past and booked dates visually distinct.
