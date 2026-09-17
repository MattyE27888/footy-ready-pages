# footy-ready-pages

The Footy Ready website, served by GitHub Pages at
<https://mattye27888.github.io/footy-ready-pages/>.

| File | What it is | Who needs it |
|---|---|---|
| `index.html` | The landing page | Social bios, the club poster's QR code, anyone sent the link |
| `how-it-works.html` | How the plan is built: the method in full | The objection the product has to beat |
| `guides.html` | The guide hub | Anyone arriving from search |
| six guide pages | Generated, listed in `make-guides.py` | Search, and the hub |
| `make-guides.py` | **The source of truth for the hub and all six guides** | Edit this, never the HTML |
| `support.html` | The support FAQ | **App Store Connect's Support URL field** |
| `privacy.html` | The privacy policy | **App Store Connect's Privacy Policy URL field** |
| `site.css` | Every page's styles, shared | All of them |
| `club-poster.pdf` | A copy of `Marketing/clubs/footy-ready-club-noticeboard.pdf` | Linked from the coaches section |

`support.html` and `privacy.html` were plain system-font pages with blue links and no header or
footer until 17 September 2026, which made the two pages Apple's own metadata points at look like
a different product. They now carry the same shell as the landing page. **The prose was not
touched**, checked by diffing the rendered word stream against the previous commit: the only
changes are the page furniture, the heading that used to repeat the wordmark now sitting in the
header instead, and one stale line dropped from the support page ("Off-season training built
around footy, not a gym plan", which predates the four-code, all-phases positioning).

`index.html` used to be the support page. It became the landing page on 16 September 2026, and
the support copy moved to `support.html` unchanged apart from two corrections: the restore control
is called **Restore Subscription**, not "Restore Purchases" (walked on a running build, recorded in
`AppStoreAssets/listing.md`), and three em dashes came out.

**The Support URL in App Store Connect points at the root, and it cannot be changed until the
next version.** It is not an App Information field. `supportUrl` lives on
`appStoreVersionLocalizations`, the same object as What's New, so it is locked while the version
is `READY_FOR_SALE` and only unlocks on a version in an editable state. `Scripts/asc.py` shows
this: it refuses to patch that object unless it finds an editable version. Promotional text is
the only listing field that can be changed in place.

So do not plan a metadata-only trip to App Store Connect for this. **Repoint it at
`support.html` as part of the next version you ship**, where it costs nothing.

In the meantime the root has to do the support work, and it does: a Support link in the header
nav, a Support link in the footer, and `mattsappdevelopment@gmail.com` on the page twice. Anyone
Apple sends there reaches the FAQ in one tap. Guideline 1.5 is checked at submission, which is
the same moment the field unlocks, so the two never conflict.

## `how-it-works.html`, and the rule it is written under

The landing page's feature grid *asserts* six things. This page proves one of them, which is the
objection the product actually has to beat: is this a generated PDF with a check-in bolted on.
Its search intent is modest and its job is conversion, so it is linked from the header nav, the
footer and the first support answer, and it is not the page anybody is meant to land on cold.

Two rules govern what it may say, and both exist because a website is a fourth place for a fact
to go stale.

**Publish the invariants, not the tuning values.** SPEC 5.1 to 5.3 are full of integers that are
explicitly expected to move during beta: the readiness band boundaries, the reps-in-reserve bands
per rep-range purpose, the 25 percent amber reduction. None of them are on this page. What is on
it is the structure (three states, two floor rules, a total that is never displayed) and the
invariants the test suite asserts, which will not move: no set to failure, an amber session never
larger than the green one, a red session with no hard running and no hard lifting sets, an
adjustment that may ease an effort target and never tighten one, an unanswered check-in that never
defaults to green. Those are safe to print because a build that breaks one does not ship.

**Check every claim against the shipping source, not against `SPEC.md`.** The spec describes
intent and the source is what runs, which is the same rule
`Marketing/instagram/stat-bank.md` section C already imposes on engine numbers. Writing this page
caught one: SPEC 5.5's absence and welcome-back flow (re-ask at 14 days, re-onboard at three
months, capacity stepped down per month away) does not exist in the app. A draft paragraph
describing it was cut and replaced with the pinning behaviour, which does ship
(`WeeklyPlanner.anchoredPlacements`, with a UI test). Verified the same way: the six phase names
against `SeasonPhase.swift`, the never-to-failure rule against
`SessionAcceptanceInvariantTests.swift:274`, the swap list's eligibility gate against
`ExerciseSwap.swift:19`.

The three citations carry their own caveats in the body text, which is deliberate. The Gabbe
hamstring figure is printed with its confidence interval running from 1.1 to 14.0, and the page
closes on Whittaker et al. 2025 finding no association between strength measures and injury in
female athletes. Both come from `stat-bank.md`, which holds the caveat wording. A marketing page
that prints the weakness of its own evidence is the thing that separates this from generated
content, and it is not to be tidied away.

## What this site will not have

Decided 17 September 2026, when the question was "make the website bigger and more substantive".
Bigger only helps if each page has its own reason to exist, so these were considered and rejected:

- **Four per-code landing pages.** The obvious search play and four near-identical pages. Brand kit
  section 1 holds that the four codes are one audience, and templated variants are the exact pile
  of thin pages this is meant to avoid.
- **A public exercise library.** 120 exercises in `Content/exercises.json` would look substantive
  and would be 120 thin pages. It is also the product.
- **A blog, a changelog, a news section or testimonials.** No author time behind them, and no real
  reviews to cite. Invented review markup is a manual-action offence.
- **A pricing page.** Same reason as everywhere else here: the App Store renders the price.

What was built instead is a **finite guide library**, shipped 17 September 2026: six guides
reworked from `Marketing/instagram/carousels.md` (C1, C2, C3, C4, C8, C9), which are the entries
with genuine external search intent. Nine of the twelve carousels there were never rendered, so
those words had never been published anywhere indexable. C5, C6, C7, C11 and C12 are product
explanation rather than guides, and they went into `how-it-works.html` instead of becoming five
thin pages. C10 became the "one pre-season, four codes" section on the hub.

**It ships complete and it is not a blog.** No feed, no dates on the cards, no "latest", nothing
that implies a cadence nobody has committed to. A finite set of six does not go stale. A blog with
three posts and a four-month gap does. (`datePublished` is in each guide's `Article` JSON-LD,
because that field is honest and machine-facing. Nothing on the page shows a date.)

## `make-guides.py`

**Edit the script, never the HTML it writes.** Six guides sharing a shell means six copies of the
same header, nav, footer and JSON-LD to keep in step by hand, which is the problem the inline CSS
had before it became `site.css`. The copy lives in the `GUIDES` list; `python3 make-guides.py`
rewrites the seven pages and `sitemap.xml`.

Three rules bind the copy, and the script's own docstring repeats them:

- **Each guide is as long as its material and no longer.** A carousel slide is about 150 words;
  expanding one into 800 is exactly how padded machine-written prose happens, and padding undoes
  the credibility the citations buy. The six currently run 441 to 748 words and that spread is
  correct, not an inconsistency to even out.
- **Every number names its study, its population and its caveat**, taken from `stat-bank.md` rather
  than paraphrased. A figure not in that bank does not go on a page. The guides print the awkward
  parts on purpose: that the acute-to-chronic workload ratio has been criticised on statistical
  grounds, that the Gabbe community-football data is from 1999, and that the widely quoted
  detraining percentage is omitted because it is not in either abstract.
- **Code-neutral by default.** The brand kit lets social rotate code examples across a month. Six
  guides published in one go cannot rotate, so they name a code only when a cited study measured
  one, and say so when they do.

**Check every PubMed ID before publishing.** A draft of the first guide carried a plausible but
wrong ID for Windt et al., written from memory instead of read off the bank; the bank says
27075963. All eight IDs on the site were then checked against the eutils summary endpoint, author,
journal and year. `stat-bank.md`'s header has the command.

## Where the design comes from

Nothing here is invented. Colour and type are `Marketing/BRAND-KIT.md` sections 2 and 3, which come
in turn from the app's own `Theme.swift`, and the page copy is cut down from
`AppStoreAssets/listing.md`'s approved description. Change the app first, the kit second and this
page third.

- One accent per section. Olive grounds carry chartreuse, bone grounds carry field green, and the
  two greens never appear together.
- No gradients, no drop shadows.
- Australian English, no em dashes, no medical claims, no first person.
- No club, league or governing-body names. The ban was lifted for **social** content on
  9 September 2026 and this page is not social: it is the site Apple's own metadata points at.
- No prices. The App Store renders the current price and trial itself, and a number typed here
  would be a fourth place for it to go stale.

## Assets

```
python3 make-assets.py   # rebuilds every image in img/ from the App Store assets
```

The device shots in `img/` are cropped out of `AppStoreAssets/screenshots/6.5/`, keeping their
olive ground so they sit flush on the olive sections and read as a deliberate olive panel on the
bone ones. The fonts in `fonts/` are the same Inter and Inter Tight variable files the tile
compositor uses, subsetted to latin and converted to woff2 (about 75 KB for the pair). They are
self-hosted rather than loaded from Google, because a page whose selling point is "no analytics and
no server" should not hand every visitor's IP to a third party on load.

## The App Store link

The landing page's two buttons carry `?ct=website` and `how-it-works.html` carries
`?ct=website-method`, the App Analytics campaign tokens, so traffic from here is separable from
App Store search in Analytics, Acquisition, Campaigns, and the two pages are separable from each
other. **Give each new page its own token** on the same pattern, or it converts invisibly. Any link posted elsewhere can
carry its own token the same way (`?ct=tiktok`, `?ct=instagram`) with no website involved.

## Search

The page carries `Organization`, `WebSite` and `SoftwareApplication` JSON-LD in one `@graph`, a
canonical URL, a sitemap and `robots.txt`. The point of the structured data is not rich results,
it is telling Google that the site, the App Store listing and the Instagram account are one entity,
so that somebody who reads the poster and then searches "footy ready app" lands here.

`sameAs` currently lists the App Store listing and Instagram only, because those are the two
handles confirmed live. **Add TikTok, Facebook and YouTube to it once their URLs are certain.** A
wrong URL in `sameAs` works against the entity matching it is there to help, so a guess is worse
than an omission. No `aggregateRating` is claimed, and none should be until there are real ratings
to cite; invented review markup is a manual-action offence.

`<meta name="apple-itunes-app">` puts Safari's native install banner at the top of the page on an
iPhone, which is where the conversions are.

**The site is verified in Google Search Console and `sitemap.xml` is submitted**, done
17 September 2026 as a Domain property. See "Search Console" below.

## The custom domain

Three domains were registered at VentraIP on 17 September 2026: **`footyreadyapp.com.au`**,
`footyreadyapp.com` and `footyreadyapp.site`.

**`footyreadyapp.com.au` is canonical.** GitHub Pages serves one custom domain per repository,
because the `CNAME` file holds exactly one name, so the other two redirect to it and are not
served from here. The `.com.au` was chosen because the audience is Australian amateur footballers,
"footy" is an Australianism, and the App Store listing is on the AU storefront. It is reversible:
the `.com` is held, so if the app ever goes beyond Australia the canonical can move to it.

Every absolute URL in the repo was swapped from `mattye27888.github.io/footy-ready-pages` on
17 September 2026, which is 68 occurrences across 15 files, and the path segment went with it
because the new domain serves from its root. **`make-guides.py`'s `BASE` is the source of truth
for the eleven canonical tags, the JSON-LD and `sitemap.xml`**; change it there and re-run, never
in the generated HTML. `robots.txt` and the four hand-written pages carry their own copy.

The old `mattye27888.github.io` address keeps redirecting once the custom domain is set, so the
club poster and anything already posted still work.

### DNS, which is Matthew's to enter

At VentraIP, for `footyreadyapp.com.au`:

| Type | Host | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `mattye27888.github.io.` |

Those four apex addresses were read off GitHub's own documentation on 17 September 2026, not from
memory. AAAA records on `2606:50c0:800{0,1,2,3}::153` are optional and can be added later.

For `footyreadyapp.com` and `footyreadyapp.site`, use VentraIP's free web forwarding to
`https://footyreadyapp.com.au`, set to a permanent (301) redirect. **Check that the forwarder
serves HTTPS.** Registrar URL forwarding is often HTTP-only, which means `https://footyreadyapp.com`
would fail with a certificate warning rather than redirect. If VentraIP's does not do HTTPS, put
the `.com` behind Cloudflare's free tier and use a redirect rule there instead.

### Done, 17 September 2026

The move is complete and verified. Every entry point lands on `https://footyreadyapp.com.au`:
the apex, `www`, both other domains, and the old `mattye27888.github.io` address, which keeps
redirecting so the club poster and anything already posted still work.

Certificates: `footyreadyapp.com.au` is Let's Encrypt via GitHub Pages, and the two forwarded
domains carry their own ZeroSSL certificates issued by VentraIP. **Enforce HTTPS is ticked** in
Settings, Pages, so `http://` is 301'd rather than served, which is what was showing "Not Secure"
in the address bar before it was turned on. Serving plain HTTP was the default until that box was
ticked, so it is worth checking after any future domain change.

Two things about the forwarded domains, learned here rather than assumed:

- **VentraIP's forwarding does serve HTTPS.** The concern recorded above was that registrar URL
  forwarding is often HTTP-only. It is not, in this case.
- **The certificates are not issued at the same time.** `.site` had one within a couple of minutes
  and `.com` took closer to fifteen, which looked like a configuration difference and was not one.
  A forwarded domain failing TLS handshake shortly after setup is worth waiting out before
  changing anything.

Each forwarder is a 301 with **Wildcard redirect** and **Retain source path** on, so
`footyreadyapp.com/guides.html` reaches the matching page rather than the homepage, and
`www.footyreadyapp.com` redirects as well as the bare domain.

### Still to do

1. **Privacy Policy URL** in App Store Connect, to `https://footyreadyapp.com.au/privacy.html`.
2. **Support URL** with the next version, to `https://footyreadyapp.com.au/support.html`. It is a
   version-level field and cannot be changed while a version is live.
3. Instagram and Facebook profile links.
4. Rebuild the club poster so its QR code points at the site rather than at the App Store.
5. Add TikTok, Facebook and YouTube to `sameAs` in `index.html`'s JSON-LD once those URLs are
   certain. A wrong URL there works against the entity matching it exists to help.

### Search Console. Done 17 September 2026

Verified as a **Domain property**, which covers the apex, `www`, http and https in one. A
URL-prefix property would have needed a second property for `www`. Verification is a
`google-site-verification` TXT record on the apex at VentraIP: in their DNS editor the Hostname
field appends `.footyreadyapp.com.au` on its own, so the root record is entered with **Hostname
left blank**, not `@`. `sitemap.xml` was submitted as a **full URL**, because a Domain property
has no prefix to append a relative path to. It read Success and eleven discovered pages the same
day. **Leave the TXT record in place**; Google re-checks it and un-verifies the property if it
goes.

**The first VERIFY press failed on a record that was already correct, and the fix was to wait.**
Creating the property makes Google look for the token before it exists, and that empty answer is
cached for the zone's negative TTL, the last field of the SOA, which is 3600 here. The failure
reads as a wrong or truncated value, so the instinct is to change the DNS, and every such change
is wasted: it cannot flush Google's cache. Ignore the error dialog's own suggestion to add a
different TXT record, which only leaves a second dead token in the zone. Confirm the record once
against the nameservers rather than a local resolver, `dig +short @ns1.nameserver.net.au
footyreadyapp.com.au TXT`, then change nothing and press VERIFY again later.

Two things that mislead while waiting. The dialog's value field **truncates the token visually**,
so use its COPY button rather than reading it off the screen; a real Google token is 43 characters
after the `=`. And **sampling `8.8.8.8` does not predict the verifier**: it is anycast, different
instances expire the cached answer at different times, and verification succeeded at a moment when
that resolver was returning the record on only 5 of 12 queries.

### The original checklist, kept for the next domain change

### Then, in order

1. Wait for the DNS to resolve. `dig +short footyreadyapp.com.au` should return the four addresses.
2. **Only then push the `CNAME` file.** Pushing it before the DNS exists stops Pages serving the
   github.io address and starts it serving nothing. The file is committed but held back for
   exactly this reason.
3. Repo Settings, Pages, set the custom domain, then tick Enforce HTTPS once the certificate is
   issued. It can take a few minutes.
4. Update the **Privacy Policy URL** in App Store Connect. The Support URL is a version-level
   field and cannot be changed while the version is live; repoint it at `support.html` as part of
   the next version.
5. Update the Instagram and Facebook profile links.
6. Rebuild the club poster so its QR code points at the new domain rather than at the App Store.
7. Verify the site in Google Search Console and submit `sitemap.xml`, which now lists eleven URLs.
   This is the step that gets skipped and it is what gets a new domain indexed in days rather than
   weeks. Expect the first VERIFY press to fail on a correct record and read "Search Console"
   above before touching the DNS.
