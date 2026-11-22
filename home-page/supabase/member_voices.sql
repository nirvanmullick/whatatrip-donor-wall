-- Migration: member_voices (NOT YET APPLIED: waiting for Nirvan's OK, Nov 22 2026)
-- Lets the public home page list what members wrote as "why I'm supporting this film".
-- Returns only: the name shown, the quote, and when it was last updated.
-- Leaves out anyone who is anonymous, private, not approved, or who has hidden their quote.
-- No table changes. Same pattern as member_photos().
create or replace function public.member_voices()
returns table(k text, name text, quote text, updated_at timestamptz)
language sql
stable
security definer
set search_path to ''
as $$
  select lower(trim(pp.display_name)), trim(pp.display_name), trim(pp.testimonial), pp.updated_at
  from public.public_profiles pp
  where coalesce(trim(pp.testimonial), '') <> ''
    and coalesce(trim(pp.display_name), '') <> ''
    and pp.approval_status = 'approved'
    and not coalesce(pp.is_anonymous, false)
    and not coalesce(pp.is_private, false)
    and not ('quote' = any (coalesce(pp.hide_sections, '{}')))
$$;
revoke all on function public.member_voices() from public;
grant execute on function public.member_voices() to anon, authenticated;
