// What a Trip: email a reminder to someone who left the checkout part-way and asked for one.
// Called from the checkout's "Maybe next time?" card. Deployed to the "What a Trip" Supabase project.
//
// Anyone can ask (they are not logged in), so this function does its own limits:
//   - one reminder per email address per 24 hours,
//   - at most 20 an hour and 150 a day in total,
//   - the wording is fixed; nothing the visitor types appears in the email except the gift amount.
// Requests are kept in public.checkout_reminders, which only this function can read or write (service key).
// The email goes out through Resend. The key lives in the function secret RESEND_API_KEY and is never in the page.
import { createClient } from "jsr:@supabase/supabase-js@2";

const SITE = "https://www.whatatrip.com";
const PAGES = ["/home-dev", "/home-test", "/donate", "/"]; // where the "finish your gift" link may point. Update when the site moves.
const FROM = "WHAT A TRIP: The Rick Doblin Story <members@whatatrip.com>";
const REPLY_TO = "support@whatatrip.com";
const ORIGINS = ["https://whatatrip.com", "https://www.whatatrip.com"];
// While testing (Nirvan, Nov 23), reminders go only to the team: any @interconnected.is or @whatatrip.com address,
// and nirvan.mullick@gmail.com. Every other address is refused here, whatever the page sends.
const TEAM_ONLY = true;
const teamOk = (e: string) => /@(interconnected\.is|whatatrip\.com)$/.test(e) || e === "nirvan.mullick@gmail.com";
const money = (n: number) => "$" + n.toLocaleString("en-US", { maximumFractionDigits: 2 });

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
  if (req.method !== "POST") return json({ ok: false, reason: "method" }, 405);
  if (origin && !ORIGINS.includes(origin)) return json({ ok: false, reason: "origin" }, 403);

  let body: { email?: string; amount?: number; monthly?: boolean; page?: string };
  try { body = await req.json(); } catch { return json({ ok: false, reason: "bad_request" }, 400); }
  const email = String(body.email ?? "").trim().toLowerCase();
  const amount = Math.round(Number(body.amount) * 100) / 100;
  const monthly = body.monthly === true;
  const page = PAGES.includes(String(body.page ?? "")) ? String(body.page) : "/";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 254) return json({ ok: false, reason: "bad_email" }, 400);
  if (!(amount >= 5 && amount <= 10000000)) return json({ ok: false, reason: "bad_amount" }, 400);
  if (TEAM_ONLY && !teamOk(email)) return json({ ok: false, reason: "team_only" });

  const url = Deno.env.get("SUPABASE_URL"), skey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (!url || !skey) return json({ ok: false, reason: "not_set_up" });
  const db = createClient(url, skey, { auth: { persistSession: false, autoRefreshToken: false } });

  const dayAgo = new Date(Date.now() - 864e5).toISOString(), hourAgo = new Date(Date.now() - 36e5).toISOString();
  const same = await db.from("checkout_reminders").select("id", { count: "exact", head: true }).eq("email", email).not("sent_at", "is", null).gte("created_at", dayAgo);
  if (same.error) { console.error("lookup failed", same.error.message); return json({ ok: false, reason: "send_failed" }); }
  if ((same.count ?? 0) > 0) return json({ ok: true, already: true });
  const hr = await db.from("checkout_reminders").select("id", { count: "exact", head: true }).gte("created_at", hourAgo);
  const dy = await db.from("checkout_reminders").select("id", { count: "exact", head: true }).gte("created_at", dayAgo);
  if ((hr.count ?? 0) >= 20 || (dy.count ?? 0) >= 150) return json({ ok: false, reason: "busy" });

  const key = Deno.env.get("RESEND_API_KEY");
  if (!key) return json({ ok: false, reason: "not_set_up" });

  const ins = await db.from("checkout_reminders").insert({ email, amount, monthly, page }).select("id").single();
  if (ins.error || !ins.data) { console.error("insert failed", ins.error?.message); return json({ ok: false, reason: "send_failed" }); }

  const link = `${SITE}${page === "/" ? "/" : page}?finish=${encodeURIComponent(String(amount))}${monthly ? "&monthly=1" : ""}`;
  const gift = money(amount) + (monthly ? " monthly gift" : " gift");
  const subject = "Your reminder: finish your gift to What a Trip";
  const text =
`You asked us for a reminder to finish your ${gift} to WHAT A TRIP: The Rick Doblin Story.

Pick up where you left off:
${link}

Your gift is tax-deductible through Creative Visions Foundation, our nonprofit fiscal sponsor. Nothing has been charged.

If you didn't ask for this, you can ignore it. We won't email you about it again.

WHAT A TRIP: The Rick Doblin Story
whatatrip.com`;
  const html =
`<div style="font-family:Helvetica,Arial,sans-serif;font-size:16px;line-height:1.5;color:#1b1526;max-width:520px;margin:0 auto;padding:24px 20px">
<p style="font-size:13px;font-weight:bold;letter-spacing:.08em;color:#6152a0;margin:0 0 14px">WHAT A TRIP: THE RICK DOBLIN STORY</p>
<p style="font-size:20px;font-weight:bold;margin:0 0 12px">Here’s the reminder you asked for.</p>
<p style="margin:0 0 18px">You were part-way through a <b>${gift}</b> to the film. You can pick up where you left off whenever you’re ready.</p>
<p style="margin:0 0 22px"><a href="${link}" style="display:inline-block;background:#6152a0;color:#ffffff;text-decoration:none;font-weight:bold;padding:12px 22px;border-radius:8px">Finish my gift</a></p>
<p style="margin:0 0 18px;color:#5b6478;font-size:14px">Your gift is tax-deductible through Creative Visions Foundation, our nonprofit fiscal sponsor. Nothing has been charged.</p>
<p style="margin:0;color:#5b6478;font-size:14px">If you didn’t ask for this, you can ignore it. We won’t email you about it again.</p>
</div>`;

  let failed = "";
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({ from: FROM, to: [email], reply_to: REPLY_TO, subject, html, text }),
    });
    if (!r.ok) failed = `resend ${r.status} ${(await r.text()).slice(0, 200)}`;
  } catch (e) { failed = String(e).slice(0, 200); }

  if (failed) {
    console.error("send failed", failed);
    await db.from("checkout_reminders").update({ send_error: failed }).eq("id", ins.data.id);
    return json({ ok: false, reason: "send_failed" });
  }
  await db.from("checkout_reminders").update({ sent_at: new Date().toISOString() }).eq("id", ins.data.id);
  return json({ ok: true });
});
