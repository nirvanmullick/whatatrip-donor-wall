// What a Trip: give a teammate a role AND email them about it.
// Called from Team tools > Team & roles on whatatrip.com. Deployed to the "What a Trip" Supabase project.
//
// Who may do this is decided by the database function invite_staff(), which runs as the signed-in caller:
// Owner may give Admin, Manager or Editor; an Admin may give Manager or Editor. This function only adds the email.
// The email goes out through Resend. The key lives in the function secret RESEND_API_KEY and is never in the page.
import { createClient } from "jsr:@supabase/supabase-js@2";

const SITE = "https://whatatrip.com/home-test?welcome=team"; // opens the welcome + log-in screen. Change the page when the new home page goes live
const FROM = "WHAT A TRIP: The Rick Doblin Story <members@whatatrip.com>";
const REPLY_TO = "support@whatatrip.com";
const ORIGINS = ["https://whatatrip.com", "https://www.whatatrip.com"];
const ROLES: Record<string, [string, string]> = {
  admin: ["an Admin", "You can run the site day to day: members, updates, perks, reports, and giving teammates a Manager or Editor role."],
  manager: ["a Manager", "You can find members, see gifts and reports, and post updates."],
  editor: ["an Editor", "You can post updates and edit the site's public text."],
};
const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

Deno.serve(async (req: Request) => {
  const origin = req.headers.get("origin") ?? "";
  const cors = {
    "Access-Control-Allow-Origin": ORIGINS.includes(origin) ? origin : ORIGINS[0],
    "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Vary": "Origin",
  };
  const json = (body: unknown, status = 200) =>
    new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "method" }, 405);

  const auth = req.headers.get("Authorization") ?? "";
  if (!auth.startsWith("Bearer ")) return json({ error: "not_signed_in" }, 401);
  const sb = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_ANON_KEY") ?? "sb_publishable_1qMBjg1BSnygZLkKbmqT6w_ZIAdt5oY",
    { global: { headers: { Authorization: auth } }, auth: { persistSession: false, autoRefreshToken: false } },
  );
  const { data: u } = await sb.auth.getUser(auth.slice(7));
  if (!u?.user) return json({ error: "not_signed_in" }, 401);

  let body: { email?: string; role?: string };
  try { body = await req.json(); } catch { return json({ error: "bad_request" }, 400); }
  const email = String(body.email ?? "").trim().toLowerCase();
  const role = String(body.role ?? "");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 254 || !ROLES[role]) return json({ error: "bad_request" }, 400);

  // The permission check and the role change both happen here, as the caller.
  const { data: result, error } = await sb.rpc("invite_staff", { invite_email: email, invite_role: role });
  if (error) return json({ error: "not_allowed" }, 403);

  // Who is inviting, for the wording.
  let inviter = "The What a Trip team";
  const { data: m } = await sb.from("members").select("id").eq("auth_user_id", u.user.id).maybeSingle();
  if (m?.id) {
    const { data: p } = await sb.from("member_private").select("first_name,last_name").eq("member_id", m.id).maybeSingle();
    const n = [p?.first_name, p?.last_name].filter(Boolean).join(" ").trim();
    if (n) inviter = n.slice(0, 80);
  }

  const key = Deno.env.get("RESEND_API_KEY");
  if (!key) return json({ result, emailed: false, reason: "not_set_up" });

  const [aRole, can] = ROLES[role];
  const subject = `${inviter} added you to the What a Trip team`;
  const text =
`${inviter} added you to the What a Trip team as ${aRole}.

${can}

To get started, log in with this email address (${email}):
${SITE}

That link opens a welcome page. Type this address there and choose "Email me a log-in link". You can set a password once you are in. Your team tools will be in the menu on your dashboard.

Questions? Just reply to this email.

WHAT A TRIP: The Rick Doblin Story
whatatrip.com`;
  const html =
`<div style="font-family:Helvetica,Arial,sans-serif;font-size:16px;line-height:1.5;color:#1b1526;max-width:520px;margin:0 auto;padding:24px 20px">
<p style="font-size:13px;font-weight:bold;letter-spacing:.08em;color:#6152a0;margin:0 0 14px">WHAT A TRIP: THE RICK DOBLIN STORY</p>
<p style="font-size:20px;font-weight:bold;margin:0 0 12px">${esc(inviter)} added you to the team as ${esc(aRole)}.</p>
<p style="margin:0 0 18px">${esc(can)}</p>
<p style="margin:0 0 18px">To get started, log in with this email address (<b>${esc(email)}</b>).</p>
<p style="margin:0 0 22px"><a href="${SITE}" style="display:inline-block;background:#6152a0;color:#ffffff;text-decoration:none;font-weight:bold;padding:12px 22px;border-radius:8px">Log in to What a Trip</a></p>
<p style="margin:0 0 18px;color:#5b6478;font-size:14px">The button opens a welcome page. Type this address there and choose “Email me a log-in link”. You can set a password once you are in. Your team tools will be in the menu on your dashboard.</p>
<p style="margin:0;color:#5b6478;font-size:14px">Questions? Just reply to this email.</p>
</div>`;

  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({ from: FROM, to: [email], reply_to: REPLY_TO, subject, html, text }),
    });
    if (!r.ok) {
      console.error("resend failed", r.status, (await r.text()).slice(0, 300));
      return json({ result, emailed: false, reason: "send_failed" });
    }
  } catch (e) {
    console.error("resend error", String(e).slice(0, 300));
    return json({ result, emailed: false, reason: "send_failed" });
  }
  return json({ result, emailed: true });
});
