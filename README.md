# footy-ready-pages

The Footy Ready website, served by GitHub Pages at
<https://mattye27888.github.io/footy-ready-pages/>.

| File | What it is | Who needs it |
|---|---|---|
| `index.html` | The landing page | Social bios, the club poster's QR code, anyone sent the link |
| `support.html` | The support FAQ | **App Store Connect's Support URL field** |
| `privacy.html` | The privacy policy | **App Store Connect's Privacy Policy URL field** |
| `club-poster.pdf` | A copy of `Marketing/clubs/footy-ready-club-noticeboard.pdf` | Linked from the coaches section |

`index.html` used to be the support page. It became the landing page on 16 September 2026, and
the support copy moved to `support.html` unchanged apart from two corrections: the restore control
is called **Restore Subscription**, not "Restore Purchases" (walked on a running build, recorded in
`AppStoreAssets/listing.md`), and three em dashes came out.

**The Support URL in App Store Connect has to be repointed at `support.html`.** Apple's guideline
1.5 wants a support page at that URL, and the root is now marketing. It is a metadata-only field,
so it needs no new build, but until it changes the listing sends people to the wrong page.

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

Both buttons carry `?ct=website`, the App Analytics campaign token, so traffic from here is
separable from App Store search in Analytics, Acquisition, Campaigns. Any link posted elsewhere can
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
