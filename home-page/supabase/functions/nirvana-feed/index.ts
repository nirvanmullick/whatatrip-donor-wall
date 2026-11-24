// What a Trip: a read-only to-do feed for NIRVANA (Nirvan's task system).
// NIRVANA calls this every few minutes and turns each new item into a task assigned to the right team member.
// Deployed to the "What a Trip" Supabase project. Nothing here writes to the database.
//
// Who may call it: only a caller that sends the shared key in the header  x-feed-key: <key>.
// The key lives in the function secret NIRVANA_FEED_KEY (set in the Supabase dashboard, and the same value in NIRVANA's
// own secrets). Until that secret is set the feed answers 503 and gives out nothing.
//
// GET  ?since=<ISO date>   items created or changed after that moment (default: the last 30 days), newest first, at most 500.
//
// Each item: { type, id, at, title, summary, status, person, email, link }
//   type: perk_request | challenge_signup | perk_offer | bug_report | flagged_profile | name_idea
//   link: where the team handles it in Site Management (the dashboard opens on the right tool).
import { createClient } from "jsr:@supabase/supabase-js@2";

const SITE = "https://www.whatatrip.com/home-dev"; // update when the site moves off Squarespace
const tool = (t: string) => `${SITE}#manage-${t}`;

Deno.serve(async (req: Request) => {
  const json = (body: unknown, status = 200) =>
    new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
  if (req.method !== "GET") return json({ ok: false, reason: "method" }, 405);

  const KEY = Deno.env.get("NIRVANA_FEED_KEY") ?? "";
  if (KEY.length < 24) return json({ ok: false, reason: "not_set_up" }, 503);
  const sent = req.headers.get("x-feed-key") ?? "";
  // constant-time comparison
  let diff = sent.length ^ KEY.length;
  for (let i = 0; i < KEY.length; i++) diff |= KEY.charCodeAt(i) ^ (sent.charCodeAt(i) || 0);
  if (diff !== 0) return json({ ok: false, reason: "unauthorized" }, 401);

  const u = new URL(req.url);
  const sinceRaw = u.searchParams.get("since");
  const since = sinceRaw && !isNaN(Date.parse(sinceRaw)) ? new Date(sinceRaw).toISOString() : new Date(Date.now() - 30 * 864e5).toISOString();

  const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
  const items: Record<string, unknown>[] = [];
  const names: Record<string, { name: string; email: string }> = {};
  const who = async (ids: (string | null)[]) => {
    const need = [...new Set(ids.filter((x): x is string => !!x && !names[x]))];
    if (!need.length) return;
    const { data } = await db.from("member_private").select("member_id,first_name,last_name,primary_email").in("member_id", need);
    (data ?? []).forEach((m) => { names[m.member_id] = { name: [m.first_name, m.last_name].filter(Boolean).join(" ") || "Member", email: m.primary_email ?? "" }; });
  };

  // Perk requests: a member asked for a perk or sent details.
  {
    const { data } = await db.from("perk_requests").select("id,member_id,perk_key,kind,interested,details,status,updated_at").gte("updated_at", since).order("updated_at", { ascending: false }).limit(200);
    await who((data ?? []).map((x) => x.member_id));
    (data ?? []).forEach((x) => items.push({
      type: "perk_request", id: `perk_request:${x.id}`, at: x.updated_at, status: x.status,
      title: `Perk request: ${x.perk_key}`, summary: x.interested ? "Interested" : Object.entries(x.details ?? {}).filter(([k]) => k !== "addr").map(([k, v]) => `${k}: ${v}`).join(", ").slice(0, 400),
      person: names[x.member_id]?.name ?? "Member", email: names[x.member_id]?.email ?? "", link: tool("preq"),
    }));
  }
  // Matching challenge sign-ups.
  {
    const { data } = await db.from("challenge_signups").select("id,created_at,name,email,amount,ratio,run_length,start_pref,pool_ok,credit_as,note,status").gte("created_at", since).order("created_at", { ascending: false }).limit(100);
    (data ?? []).forEach((x) => items.push({
      type: "challenge_signup", id: `challenge_signup:${x.id}`, at: x.created_at, status: x.status,
      title: `New matching challenge: $${Number(x.amount).toLocaleString("en-US")} at ${x.ratio}:1`,
      summary: [x.credit_as && `Credit as ${x.credit_as}`, x.run_length && `Run: ${x.run_length}`, x.start_pref && `Start: ${x.start_pref}`, x.pool_ok && "Open to combining", x.note].filter(Boolean).join(" · ").slice(0, 400),
      person: x.name, email: x.email, link: tool("chal"),
    }));
  }
  // Perk offers ("Donate a perk").
  {
    const { data } = await db.from("perk_offers").select("id,created_at,name,email,perk,availability,quantity,est_value,status").gte("created_at", since).order("created_at", { ascending: false }).limit(100);
    (data ?? []).forEach((x) => items.push({
      type: "perk_offer", id: `perk_offer:${x.id}`, at: x.created_at, status: x.status, title: "Perk offered",
      summary: [x.perk, x.availability && `Available: ${x.availability}`, x.quantity && `How many: ${x.quantity}`, x.est_value && `Value: ${x.est_value}`].filter(Boolean).join(" · ").slice(0, 400),
      person: x.name, email: x.email, link: tool("msgs"),
    }));
  }
  // Bug reports and ideas.
  {
    const { data } = await db.from("reports").select("id,created_at,updated_at,member_id,kind,message,page,code,status").gte("updated_at", since).order("updated_at", { ascending: false }).limit(200);
    await who((data ?? []).map((x) => x.member_id));
    (data ?? []).forEach((x) => items.push({
      type: "bug_report", id: `bug_report:${x.id}`, at: x.updated_at ?? x.created_at, status: x.status,
      title: `${x.kind === "idea" ? "Idea" : "Bug report"}${x.code ? ` (${x.code})` : ""}`, summary: [x.message, x.page && `Page: ${x.page}`].filter(Boolean).join(" · ").slice(0, 600),
      person: x.member_id ? names[x.member_id]?.name ?? "Member" : "Visitor", email: x.member_id ? names[x.member_id]?.email ?? "" : "", link: tool("bugs"),
    }));
  }
  // Profiles flagged for review.
  {
    const { data } = await db.from("profile_flags").select("id,created_at,member_id,reason,status").gte("created_at", since).order("created_at", { ascending: false }).limit(100);
    await who((data ?? []).map((x) => x.member_id));
    (data ?? []).forEach((x) => items.push({
      type: "flagged_profile", id: `flagged_profile:${x.id}`, at: x.created_at, status: x.status, title: "Profile flagged for review",
      summary: String(x.reason ?? "").slice(0, 400), person: names[x.member_id]?.name ?? "Member", email: "", link: tool("flags"),
    }));
  }
  // Credit-name ideas for the community credit.
  {
    const { data } = await db.from("credit_name_ideas").select("id,created_at,idea,member_id,status").gte("created_at", since).order("created_at", { ascending: false }).limit(200);
    await who((data ?? []).map((x) => x.member_id));
    (data ?? []).forEach((x) => items.push({
      type: "name_idea", id: `name_idea:${x.id}`, at: x.created_at, status: x.status, title: `Credit name idea: ${x.idea}`,
      summary: "", person: x.member_id ? names[x.member_id]?.name ?? "Member" : "", email: "", link: SITE,
    }));
  }

  items.sort((a, b) => String(b.at).localeCompare(String(a.at)));
  return json({ ok: true, since, count: Math.min(items.length, 500), items: items.slice(0, 500) });
});
