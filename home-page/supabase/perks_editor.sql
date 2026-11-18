-- Perks editor: one saved copy of the perk wording, icons and hover text,
-- plus a "Perks Management" permission that can be given on top of any team role.

create table if not exists public.site_content (
  key text primary key check (key in ('perks')),
  data jsonb not null,
  updated_at timestamptz not null default now(),
  updated_by uuid references public.members(id)
);
alter table public.site_content enable row level security;
drop policy if exists site_content_read on public.site_content;
create policy site_content_read on public.site_content for select to anon, authenticated using (true);
grant select on public.site_content to anon, authenticated;

create table if not exists public.staff_permissions (
  member_id uuid not null references public.members(id) on delete cascade,
  perm text not null check (perm in ('perks')),
  granted_by uuid references public.members(id),
  granted_at timestamptz not null default now(),
  primary key (member_id, perm)
);
alter table public.staff_permissions enable row level security;
drop policy if exists staff_permissions_read on public.staff_permissions;
create policy staff_permissions_read on public.staff_permissions for select to authenticated
  using (member_id = (select private.current_member_id()) or (select private.has_role('owner','admin','manager')));
grant select on public.staff_permissions to authenticated;

create or replace function private.can_edit_perks() returns boolean
language sql stable security definer set search_path to '' as $$
  select private.has_role('owner','admin') or exists (
    select 1 from public.staff_permissions p join public.members m on m.id = p.member_id
    where m.auth_user_id = (select auth.uid()) and m.status = 'active' and p.perm = 'perks')
$$;

create or replace function public.save_site_content(p_key text, p_data jsonb) returns timestamptz
language plpgsql security definer set search_path to '' as $$
declare old jsonb; t timestamptz := now();
begin
  if p_key <> 'perks' then raise exception 'Not allowed'; end if;
  if not private.can_edit_perks() then raise exception 'Not allowed'; end if;
  if p_data is null or jsonb_typeof(p_data) <> 'object' or length(p_data::text) > 200000 then raise exception 'Bad data'; end if;
  select data into old from public.site_content where key = p_key;
  insert into public.site_content(key, data, updated_at, updated_by) values (p_key, p_data, t, private.current_member_id())
    on conflict (key) do update set data = excluded.data, updated_at = t, updated_by = excluded.updated_by;
  insert into public.audit_log(actor_member_id, actor_auth_id, action, table_name, row_id, before, after)
    values (private.current_member_id(), (select auth.uid()), case when old is null then 'INSERT' else 'UPDATE' end, 'site_content', p_key, old, p_data);
  return t;
end $$;

create or replace function public.set_staff_permission(p_member uuid, p_perm text, p_on boolean) returns boolean
language plpgsql security definer set search_path to '' as $$
begin
  if p_perm <> 'perks' then raise exception 'Not allowed'; end if;
  if not private.has_role('owner','admin') then raise exception 'Not allowed'; end if;
  if p_on then
    insert into public.staff_permissions(member_id, perm, granted_by) values (p_member, p_perm, private.current_member_id())
      on conflict do nothing;
    insert into public.audit_log(actor_member_id, actor_auth_id, action, table_name, row_id, after)
      values (private.current_member_id(), (select auth.uid()), 'INSERT', 'staff_permissions', p_member::text, jsonb_build_object('perm', p_perm));
  else
    delete from public.staff_permissions where member_id = p_member and perm = p_perm;
    insert into public.audit_log(actor_member_id, actor_auth_id, action, table_name, row_id, before)
      values (private.current_member_id(), (select auth.uid()), 'DELETE', 'staff_permissions', p_member::text, jsonb_build_object('perm', p_perm));
  end if;
  return p_on;
end $$;

create or replace function public.can_edit_perks() returns boolean
language sql stable security definer set search_path to '' as $$ select private.can_edit_perks() $$;

revoke all on function public.save_site_content(text, jsonb) from public, anon;
revoke all on function public.set_staff_permission(uuid, text, boolean) from public, anon;
revoke all on function public.can_edit_perks() from public, anon;
grant execute on function public.save_site_content(text, jsonb) to authenticated;
grant execute on function public.set_staff_permission(uuid, text, boolean) to authenticated;
grant execute on function public.can_edit_perks() to authenticated;
