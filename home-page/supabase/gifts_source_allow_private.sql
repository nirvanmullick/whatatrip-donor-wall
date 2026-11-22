-- Migration `gifts_source_allow_private` (applied Nov 21, 2026, approved by Nirvan).
-- Adds 'private' to the allowed gift sources, matching manual-gifts.csv, and relabels the two
-- Oct 15, 2026 manual gifts that were first entered as 'in_kind' (they were paid in money).
alter table public.gifts drop constraint gifts_source_check;
alter table public.gifts add constraint gifts_source_check check (source = any (array['pledge','gofundme','check','wire','in_kind','private','sample']));
update public.gifts set source = 'private' where source = 'in_kind' and source_reference in ('manual-gifts.csv 2026-10-15 Eva Dillon','manual-gifts.csv 2026-10-15 Jade Netanya Ullmann');
