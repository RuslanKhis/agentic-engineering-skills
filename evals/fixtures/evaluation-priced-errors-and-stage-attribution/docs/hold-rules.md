# Hold rules (applied by `decide_hold`)

Hold the invoice for a clerk when any of these is true; otherwise pay it.

1. **Duplicate.** `find_paid_invoice(invoice_number)` returns an earlier
   payment for the same invoice number.
2. **Over the purchase order.** The invoice total exceeds the purchase
   order amount by more than 2%. A total up to 2% over is paid.
3. **No purchase order.** The invoice carries no purchase order number.

The supplier name is shown to the clerk on a held invoice and printed on
the remittance advice. No rule reads it.
