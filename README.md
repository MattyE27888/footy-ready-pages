# footy-ready-pages

The Footy Ready website, served by GitHub Pages at
<https://mattye27888.github.io/footy-ready-pages/>.

| File | What it is | Who needs it |
|---|---|---|
| `index.html` | The landing page | Social bios, the club poster's QR code, anyone sent the link |
| `how-it-works.html` | How the plan is built: the method in full | The objection the product has to beat |
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

What is queued instead is a **finite guide library**: six guides reworked from
`Marketing/instagram/carousels.md` (C1, C2, C3, C4, C8, C9), which are the entries with genuine
external search intent. Nine of the twelve carousels there were never rendered, so those words
have never been published anywhere indexable. C5, C6, C7, C11 and C12 are product explanation
rather than guides, and they went into `how-it-works.html` instead of becoming five thin pages.

**It ships complete and it is not a blog.** No feed, no dates on the cards, no "latest", nothing
that implies a cadence nobody has committed to. A finite set of six does not go stale. A blog with
three posts and a four-month gap does.

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

**Verify the site in Google Search Console and submit the sitemap** when the domain is settled.
That is what gets a new domain indexed in days rather than weeks, and it is the step that gets
skipped.

## Moving to a custom domain

`footyreadyapp.com.au` was free as of 16 September 2026. When it is registered:

1. Add a file called `CNAME` at the repo root containing `footyreadyapp.com.au` and nothing else.
   **Do not add it before the DNS exists**, or Pages stops serving the github.io address and starts
   serving nothing.
2. At the registrar, point the apex at GitHub's Pages addresses and add a `CNAME` record for `www`
   pointing at `mattye27888.github.io`.
3. In the repo's Settings, Pages, set the custom domain and tick Enforce HTTPS once the certificate
   is issued.
4. Update the absolute URLs in `index.html`: `og:url`, `og:image`, `canonical` and the four inside
   the JSON-LD block, plus `robots.txt` and `sitemap.xml`. Grep for `mattye27888.github.io` to find
   the lot.
5. Update the Support and Privacy URLs in App Store Connect, the Instagram and Facebook profile
   links, and rebuild the club poster so its QR code points at the new domain.

The old github.io address keeps redirecting, so nothing already printed or posted breaks.
