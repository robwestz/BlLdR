# Skill: Payment Flow

## When to Use
Implementing any online payment.

## Steps
1. Build the complete purchase/booking flow WITHOUT real payment first
2. Create an order summary showing: items, quantities, prices, total
3. Add a mock "Pay Now" button that simulates success
4. Build the confirmation/receipt page
5. Test the complete flow end-to-end with mock payment
6. Only then: integrate the real payment provider (Stripe, etc.)
7. Use the provider's hosted/embedded form (never collect card numbers yourself)
8. Handle three states: processing (spinner), success (confirmation), failure (retry option)
9. On success: save order, show confirmation, send receipt

## Verification
- [ ] Order summary shows correct items and total
- [ ] Mock payment flow completes end-to-end
- [ ] Confirmation page displays order details
- [ ] Payment failure shows clear error with retry option
- [ ] Double-submit prevented (button disabled during processing)

## Common Mistakes
- Integrating payment before the flow exists: Build flow first, payment last
- Collecting card numbers directly: Use provider's hosted form (PCI compliance)
- No error handling: Payment fails often — show clear errors and retry options
