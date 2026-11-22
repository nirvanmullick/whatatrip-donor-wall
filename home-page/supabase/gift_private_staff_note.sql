-- Migration `gift_private_staff_note` (applied Nov 21, 2026, approved by Nirvan).
-- A staff-only note about a gift. gift_private rows are readable by Owner and Admin only,
-- so the note is never shown publicly or to the donor. (gifts.staff_note is NOT private in
-- that way: a member can read their own gift rows.)
alter table public.gift_private add column if not exists staff_note text;
comment on column public.gift_private.staff_note is 'Staff-only note about a gift. Readable by Owner and Admin only (gift_private row policies). Never shown publicly or to the donor.';
