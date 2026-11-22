-- Migration `gifts_source_allow_event_cost` (applied Nov 21, 2026, asked for by Nirvan).
-- Adds 'event_cost' (a donor paid the costs of a fundraising event) to the allowed gift sources
-- and relabels the two Oct 15, 2026 manual gifts from 'private' to 'event_cost'.
alter table public.gifts drop constraint gifts_source_check;
alter table public.gifts add constraint gifts_source_check check (source = any (array['pledge','gofundme','check','wire','in_kind','private','event_cost','sample']));
update public.gifts set source = 'event_cost' where source = 'private' and source_reference in ('manual-gifts.csv 2026-10-15 Eva Dillon','manual-gifts.csv 2026-10-15 Jade Netanya Ullmann');
