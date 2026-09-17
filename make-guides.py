#!/usr/bin/env python3
"""Build the guide hub and the six guides.

**Edit this file, never the HTML it writes.** Six guides that share a shell is six
copies of the same header, footer, nav and JSON-LD to keep in step by hand, which
is the same problem the inline CSS had before it became site.css.

    python3 make-guides.py

The rules the copy is written under, which the README states in full:

  * Each guide is as long as its material and no longer. The carousels in
    Marketing/instagram/carousels.md run about 150 words a slide; a guide that
    pads one into 800 is the thing the citations are meant to buy credibility
    against. A 500 word guide is finished if its material is finished.
  * Every number names its study, its population and its caveat, word for word
    from Marketing/instagram/stat-bank.md. A figure not in that bank does not
    go on a page.
  * Engine behaviour is labelled "How Footy Ready plans it" and never given an
    academic source, and is checked against the shipping source rather than
    against SPEC.md.
  * No club, league or governing-body names. Code-neutral by default: the four
    codes are one audience, and six guides published at once cannot "rotate"
    examples the way a month of posts can.
"""

import html
import os

BASE = "https://mattye27888.github.io/footy-ready-pages"
APP = "https://apps.apple.com/au/app/footy-ready-training-plan/id6807821197"
PUBLISHED = "2026-09-17"

# --------------------------------------------------------------------------- #
# Shell
# --------------------------------------------------------------------------- #

NAV = """      <nav>
        <a href="guides.html">Guides</a>
        <a href="how-it-works.html">How it works</a>
        <a href="{coaches}">Coaches</a>
        <a href="support.html">Support</a>
      </nav>"""

FOOTER = """<footer>
  <div class="wrap">
    <p class="links">
      <a href="./">Home</a>
      <a href="guides.html">Guides</a>
      <a href="how-it-works.html">How it works</a>
      <a href="support.html">Support</a>
      <a href="privacy.html">Privacy</a>
      <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Terms of Use</a>
      <a href="mailto:mattsappdevelopment@gmail.com">Email</a>
    </p>
    <p>Footy Ready gives general fitness guidance, not medical advice, and is not physiotherapy or rehabilitation. See a health professional about anything more than mild soreness.</p>
    <p>Footy Ready is an independent training app for amateur Aussie rules, rugby league, rugby union and soccer players. It is not affiliated with, endorsed by or connected to any league or governing body.</p>
    <p>&copy; 2026 Matthew Edwards</p>
  </div>
</footer>"""


def page(slug, title, description, body, jsonld=""):
    ld = f'\n<script type="application/ld+json">\n{jsonld}\n</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{html.escape(description, quote=True)}">
<link rel="canonical" href="{BASE}/{slug}">
<meta name="apple-itunes-app" content="app-id=6807821197">
<link rel="icon" href="img/favicon.png">
<link rel="apple-touch-icon" href="img/icon.png">
<link rel="stylesheet" href="site.css">{ld}
</head>
<body>

<header class="olive">
  <div class="wrap">
    <div class="bar">
      <a class="brand" href="./">
        <img src="img/icon.png" alt="">
        <span>Footy Ready</span>
      </a>
{NAV.format(coaches="./#coaches")}
    </div>
  </div>
</header>

<section class="bone doc">
  <div class="wrap">
{body}
  </div>
</section>

{FOOTER}

</body>
</html>
"""


def render(blocks):
    out = []
    for kind, value in blocks:
        if kind == "h2":
            anchor, text = value
            out.append(f'    <h2 id="{anchor}">{text}</h2>')
        elif kind == "p":
            out.append(f"    <p>{value}</p>")
        elif kind == "lede":
            out.append(f'    <p class="lede">{value}</p>')
        elif kind == "pull":
            out.append(f'    <p class="pull">{value}</p>')
        elif kind == "cite":
            out.append(f'    <p class="cite">{value}</p>')
        elif kind == "plan":
            out.append('    <div class="plan">')
            out.append('      <span class="tag">How Footy Ready plans it</span>')
            for para in value:
                out.append(f"      <p>{para}</p>")
            out.append("    </div>")
        elif kind == "ul":
            out.append('    <ul>')
            for item in value:
                out.append(f"      <li>{item}</li>")
            out.append("    </ul>")
        else:
            raise ValueError(kind)
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# The guides. Reworked from Marketing/instagram/carousels.md, which holds the
# words these were cut down from; the carousel each one came from is noted so
# the two can be kept honest against each other.
# --------------------------------------------------------------------------- #

GUIDES = []

# --- C1 -------------------------------------------------------------------- #
GUIDES.append(dict(
    slug="where-a-pre-season-starts.html",
    title="Where a Pre-Season Actually Starts",
    heading="Where a pre-season actually starts",
    ct="guide-start",
    blurb="Easy running first and sprints later, two lifts a week from week one, and why the first fortnight back is where the soft-tissue injuries live.",
    description="How to start a pre-season: aerobic base running before intervals, two lifting sessions a week from the start, and the order to add work in.",
    blocks=[
        ("lede", "The first block of a pre-season is the least exciting part of the training year, and it is the part everything later sits on. Here is the order that works, and the order most people actually use."),

        ("h2", ("base", "It doesn't start with intervals")),
        ("p", "The first block is aerobic. Easy running, most weeks, at a pace you could hold a conversation at. That's it. It is dull to do and duller to read about, which is exactly why it gets skipped."),
        ("p", "Intervals and repeat sprints work. They work best on legs that already have a base underneath them, and they are what people reach for first because they feel like training. Easy running does not feel like training until about week five, when the hard sessions you add start going better than they used to."),
        ("pull", "Boring first. Sharp later."),

        ("h2", ("lift", "Lift twice a week, from the first week")),
        ("p", "Two lifting sessions a week, every week, beats four sessions at the start and none by the time the season arrives. The consistency is the point, not the session design. Two thirty-minute sessions you actually do outperform an ambitious four-day split you abandon."),
        ("cite", "The evidence for strength work is the strongest in this area. Across 25 randomised trials and 26,610 participants, strength training programs cut sports injuries to under a third of the rate in the control groups. Stretching programs, measured the same way in the same review, changed nothing at all. Lauersen JB, Bertelsen DM, Andersen LB. The effectiveness of exercise interventions to prevent sports injuries. <em>Br J Sports Med.</em> 2014;48(11):871-877. <a href=\"https://pubmed.ncbi.nlm.nih.gov/24100287/\">PubMed 24100287</a>. The authors say plainly that the overall effect estimate was heterogeneous, and the figure is \"to under a third\", not \"by a third\", which is a different and much-repeated claim."),

        ("h2", ("turn-up", "Turning up beats going hard")),
        ("p", "The most useful finding in pre-season research is not about how to train. It is about how often you finish what you planned."),
        ("cite", "In a professional rugby league squad tracked across one 17-week pre-season, ten extra completed sessions went with 17 percent lower odds of injury the following week, controlling for that week's training load. Windt J, Gabbett TJ, Ferris D, Khan KM. Training load-injury paradox. <em>Br J Sports Med.</em> 2017;51(8):645-650. <a href=\"https://pubmed.ncbi.nlm.nih.gov/27075963/\">PubMed 27075963</a>. Thirty elite players, so it describes a full-time squad rather than somebody fitting sessions around work. The direction is worth having anyway."),
        ("p", "Not ten harder sessions. Ten more of them, actually completed. Of everything in a pre-season, that is the variable most under your control, and it is the one that responds to building a week you can realistically finish."),

        ("h2", ("order", "The order that works")),
        ("ul", [
            "<strong>Weeks 1 to 4.</strong> Easy running and two lifts. Nothing hard, nothing clever.",
            "<strong>Weeks 5 to 8.</strong> Add one harder run a week. Keep the easy running easy so the hard day can be hard.",
            "<strong>Weeks 9 onward.</strong> Sprints, changes of direction, and the total volume starts coming down as the quality goes up.",
        ]),
        ("p", "Add one thing at a time, so that when something goes well or goes wrong you know which change did it. Two new stressors in the same week tell you nothing."),

        ("h2", ("wrong", "Where most people go wrong")),
        ("p", "They start at week 9. Sprints and hard running in the first week back feel like progress in a way that easy running never does, and that is why the first fortnight of a pre-season is where the soft-tissue injuries live."),
        ("pull", "There is no version of this where you skip the base and keep it."),
        ("p", "If the first month feels slow, that is not a sign you have got it wrong. It is very nearly the only sign you have got it right."),

        ("plan", [
            "The off-season build phase runs exactly this order: aerobic base running and hypertrophy-biased lifting first, hard running introduced as the phase goes on, and the sharpening left until the phase after it. You don't choose the order, and you can't accidentally start at week 9.",
            'How the phases are worked out, and what each one is for, is on <a href="how-it-works.html#season">how the plan is built</a>.',
        ]),
    ],
))

# --- C2 -------------------------------------------------------------------- #
GUIDES.append(dict(
    slug="coming-back-after-the-off-season.html",
    title="Coming Back After the Off-Season",
    heading="The week after the quiet month",
    ct="guide-comeback",
    blurb="The jump from a quiet month to a full week is the risky part, not the fitness you lost. What the load research says, including the half of it that usually gets left off.",
    description="Coming back after the off-season: why the jump from a quiet month to a full training week is the risk, and how to ramp back in without it.",
    blocks=[
        ("lede", "The season ends, you take a proper break, and then club training resumes and you go from almost nothing to four hard sessions in a week because everybody else is. That week is the one to be careful with, and not for the reason most people assume."),

        ("h2", ("jump", "The jump is the problem, not the fitness you lost")),
        ("p", "It is tempting to read the first hard week back as punishment for the month off. It isn't. The issue is the size of the step between this week and the last month, rather than the absolute amount of work in it."),
        ("cite", "In elite rugby league players tracked over two seasons, those whose week reached about 1.6 times their rolling four-week average were several times more likely to be injured in the next match. Hulin BT, Gabbett TJ, Caputi P, Lawson DW, Sampson JA. Low chronic workload and the acute:chronic workload ratio are more predictive of injury than between-match recovery time. <em>Br J Sports Med.</em> 2016;50(16):1008-1012. <a href=\"https://pubmed.ncbi.nlm.nih.gov/26851288/\">PubMed 26851288</a>. Read this one directionally and no further: it is 28 players, the confidence intervals are enormous, and the acute-to-chronic ratio has since been criticised on statistical grounds. It is not a number to go and calculate on yourself."),

        ("h2", ("base", "A bigger base protects you")),
        ("p", "Here is the half of that finding that usually gets left off. In the same study, players carrying a high steady workload were injured less often, not more. The conclusion is not \"train less\". It is that a month of steady work is what lets you absorb a heavy week when the fixture list hands you one."),
        ("pull", "Fitness is the buffer, not the risk."),

        ("h2", ("what", "So what do you actually do")),
        ("ul", [
            "<strong>Come back before club training does</strong>, by about a fortnight, so the first hard week is not also your first week.",
            "<strong>Add roughly one session a week, not three.</strong> If you finished the break on nothing, two sessions is a full week.",
            "<strong>Keep the easy running easy.</strong> Most people ramp back by making every session moderately hard, which raises the whole week at once and leaves nowhere to go.",
        ]),
        ("p", "None of that is dramatic, and none of it will feel like enough at the time. Ramping in properly costs you a fortnight of feeling underdone and buys you the first month of the season."),

        ("plan", [
            "Weekly volume has a floor and a ceiling worked out from your answers, and the plan climbs toward the ceiling across a phase rather than starting at it. A deload comes around on a cadence set by your own recovery capacity, and it comes around sooner if your check-ins keep coming back below par.",
        ]),
    ],
))

# --- C3 -------------------------------------------------------------------- #
GUIDES.append(dict(
    slug="pre-season-training-without-a-gym.html",
    title="Pre-Season Training Without a Gym",
    heading="A pre-season with no gym",
    ct="guide-nogym",
    blurb="A patch of grass, something to hang off, and maybe a pair of dumbbells covers every movement a footy pre-season asks for. What to swap, and where bodyweight honestly runs out.",
    description="How to run a football pre-season without a gym: the six movement patterns, the swaps that hold up, and how to keep progressing without plates.",
    blocks=[
        ("lede", "A full gym buys you convenience and load. It does not buy you results you cannot get otherwise, and for a pre-season in particular the gap is smaller than the marketing around gyms suggests."),

        ("h2", ("need", "What you actually need")),
        ("p", "A patch of grass, something solid to hang off, and either a pair of dumbbells or nothing at all. That covers every movement a football pre-season asks for."),
        ("pull", "The barbell is a nice-to-have, not the program."),

        ("h2", ("patterns", "The six patterns")),
        ("p", "Strip the exercise names away and a lifting program is six jobs. Squat, hinge, push, pull, one leg at a time, and trunk. Every one of them has a version that needs no gym."),
        ("p", "That is all an exercise substitution is: the same job done with a different tool. It is not a downgrade, and it is not a compromise you are meant to feel bad about."),

        ("h2", ("swaps", "Swaps that hold up")),
        ("ul", [
            "<strong>Back squat</strong> becomes a split squat, loaded with a backpack if you have one.",
            "<strong>Deadlift</strong> becomes a single-leg hinge, done slowly, where the balance demand does the work the bar used to.",
            "<strong>Bench press</strong> becomes push-ups with your feet up on something.",
            "<strong>Chin-up</strong> stays a chin-up. It was never a gym exercise.",
        ]),

        ("h2", ("progress", "Progressing without plates")),
        ("p", "The real question with no gym is not what to do, it is how to make it harder next month. Being harder to load is not the problem it sounds like, because it forces the other levers: more reps, slower tempo, a longer range, a worse angle, or one leg instead of two."),
        ("p", "Where it does honestly run out is heavy lower-body strength. There is a point at which split squats with a backpack stop being a strength stimulus and become a conditioning one, and no amount of programming hides that. If you get there, you have had a very good year, and a pair of adjustable dumbbells is the cheapest fix there is."),

        ("plan", [
            "There are four equipment tiers, from a full gym down to bodyweight and a park, and 120 exercises in the library that substitute across them. You pick your tier once during the assessment and the plan is built inside it, so the running and bodyweight work carries the session rather than quietly assuming a rack you haven't got.",
            "Any single exercise can also be swapped on the day, and the replacements are filtered through the same eligibility rules as the original, so a swap can never hand you something your injuries or your age rule out.",
        ]),
    ],
))

# --- C4 -------------------------------------------------------------------- #
GUIDES.append(dict(
    slug="what-a-pre-season-week-looks-like.html",
    title="What a Pre-Season Week Looks Like",
    heading="What a pre-season week looks like",
    ct="guide-week",
    blurb="Two lifts, two runs and a rest day that means it. How to space the hard days, why club nights count, and what to cut when the week does not fit.",
    description="What a football pre-season training week looks like: two lifts, two runs, one real rest day, and how to fit it around club training nights.",
    blocks=[
        ("lede", "Most pre-season plans fail on arithmetic rather than on principle. The sessions are fine; there are just more of them than the week holds. Here is a week that fits."),

        ("h2", ("shape", "The shape of it")),
        ("ul", [
            "<strong>Two lifts</strong>, thirty to sixty minutes each.",
            "<strong>Two runs</strong>, one easy and one harder.",
            "<strong>One day that is genuinely off.</strong> Not active recovery. Off.",
        ]),
        ("pull", "Four sessions you finish beats six you plan."),

        ("h2", ("spacing", "Put the hard days apart")),
        ("p", "A hard run the day after a heavy lift is two hard days in a row wearing different clothes. Your legs do not keep separate accounts for which session the fatigue came from."),
        ("p", "Alternate them instead. Lift, easy run, lift, hard run, rest, and the week suddenly has room in it. The ordering does more for how the hard sessions go than the content of the hard sessions does."),
        ("pull", "Recovery is the space between sessions, not a session."),

        ("h2", ("club", "Club nights are training")),
        ("p", "Once club pre-season resumes, a club night is a hard session whether or not it appears on your own plan. Two club nights and a match is most of a week already, and a plan that adds four sessions on top of it is not a plan, it is a wish."),
        ("p", "Count what the club takes before you add anything. This is the single most common way a good individual program turns into an injury: it was written for the week you had in November and never revised for the week you have in March."),

        ("h2", ("time", "Thirty minutes is a session")),
        ("p", "Not a compromise, not a maintenance dose. A session. Most of what a football pre-season needs fits into half an hour, provided the half hour is not spent on the parts that do not matter."),
        ("plan", [
            "The assessment asks how long you have, and the answer is one of four: thirty minutes, forty-five, sixty, or seventy-five plus. Sessions are built to the length you picked rather than trimmed down from a longer one, so a thirty-minute session is a complete session and not the first half of an hour.",
        ]),

        ("h2", ("cut", "The run that gets cut first")),
        ("p", "When the week does not fit, something has to go, and it should not be the thing you decide on the night. An easy run is last in every sense: it only earns a spot once the match, the club nights and both lifts have had theirs."),
        ("plan", [
            "In-season, the easy run only appears if at least fifteen minutes of the week's running budget survives your match and your club training. A player with two club nights usually has neither the day nor the minutes, so their week is the fixture, the club nights and two short lifts, and the plan says so rather than stacking a run on top of it.",
            'The in-season week is anchored to match day rather than to Monday. <a href="how-it-works.html#season">How the plan is built</a> sets out where each day lands.',
        ]),
    ],
))

# --- C8 -------------------------------------------------------------------- #
GUIDES.append(dict(
    slug="counting-back-from-round-1.html",
    title="Counting Backwards From Round 1",
    heading="Counting backwards from round 1",
    ct="guide-countback",
    blurb="Every decision in a pre-season is arithmetic from one date. The six phases, what changes between them, and why community footy gets hurt most at the start of a season.",
    description="How to plan a pre-season backwards from round 1: the six training phases, what changes in each, and why the start of the season is when injuries cluster.",
    blocks=[
        ("lede", "Every decision in a pre-season is downstream of one date: when you next play a game that counts. How much running, how heavy, when to sharpen, when to back off. All of it is arithmetic from round 1."),
        ("pull", "Without the date, a plan is just a list of sessions."),

        ("h2", ("phases", "The six phases")),
        ("ul", [
            "<strong>Post-season reset.</strong> Two to three weeks of nothing structured.",
            "<strong>Off-season build.</strong> Aerobic base and hypertrophy-biased lifting.",
            "<strong>Pre-season 1.</strong> Strength and power, running volume climbing.",
            "<strong>Pre-season 2.</strong> Speed and repeat efforts, volume coming down as club load rises.",
            "<strong>In-season.</strong> Maintenance, anchored to match day.",
            "<strong>Finals taper.</strong> If you get there.",
        ]),

        ("h2", ("changes", "What changes in each")),
        ("p", "Off-season builds the engine. Pre-season 1 builds strength and running volume on top of it. Pre-season 2 turns that into speed while the total volume comes down, because club training is rising at the same time and the two have to add up to something survivable."),
        ("p", "The striking part, if you lay the phases side by side, is how little the exercise list changes. A squat appears in all of them. What changes every phase is the reason you are doing it, which shows up as the sets, the rep range and how close to your limit each set lands."),
        ("pull", "Same squat, different job."),

        ("h2", ("deadline", "Round 1 is a deadline")),
        ("p", "There is a reason to treat it as one rather than as a start line."),
        ("cite", "Across five amateur Australian football clubs over a season, injuries came to 27 per 1,000 player hours, they were most commonly sustained at the start of the season, and hamstring strains were the most common injury of the lot. Gabbe B, Finch C, Wajswelner H, Bennell K. Australian football: injury profile at the community level. <em>J Sci Med Sport.</em> 2002;5(2):149-160. <a href=\"https://pubmed.ncbi.nlm.nih.gov/12188087/\">PubMed 12188087</a>. This is 1999 data from one code in one state, and men's community football at that, so it is old and narrow. It is also the best published description of exactly this population, which is why it is here rather than a tidier study of professionals."),
        ("p", "You do not get fit during the season. You arrive fit, or you spend the first month catching up while everybody else is already playing, which is both the least enjoyable month of the year and the one the injury data points at."),
        ("pull", "The pre-season is the part of the season nobody sees."),

        ("plan", [
            "You enter your round 1 date during the assessment and the six phases are computed backwards from it and forwards through finals. Move the date and the whole structure moves with it. Every phase boundary is a default you can change.",
            'The phase table, and what each one actually programs, is on <a href="how-it-works.html#season">how the plan is built</a>.',
        ]),
    ],
))

# --- C9 -------------------------------------------------------------------- #
GUIDES.append(dict(
    slug="the-weeks-where-doing-nothing-is-the-plan.html",
    title="The Weeks Where Doing Nothing Is the Plan",
    heading="The weeks where doing nothing is the plan",
    ct="guide-reset",
    blurb="After the last game, the right amount of structured training is none. Why a planned two or three weeks off is not lost time, and how it differs from stopping.",
    description="The post-season break: why two to three weeks of no structured training after your last game is the plan, and how a planned break differs from stopping.",
    blocks=[
        ("lede", "After your last game, the correct amount of structured training is none. Not light training. None. Walk, swim, play something else, or do nothing at all, for two to three weeks."),

        ("h2", ("not-lost", "Why it isn't lost time")),
        ("p", "The fear is that a few weeks off undoes a year. It doesn't, and the two halves of your fitness behave quite differently across a short break."),
        ("cite", "Strength holds up well across a short break. Endurance fades faster, and recently acquired gains go first, while long-standing fitness stays above untrained levels. Mujika I, Padilla S. Detraining: loss of training-induced physiological and performance adaptations, Parts I and II. <em>Sports Med.</em> 2000;30(2):79-87 and 30(3):145-154. <a href=\"https://pubmed.ncbi.nlm.nih.gov/10966148/\">PubMed 10966148</a>. There is a widely quoted percentage for how much fitness is lost in how many weeks. It is not quoted here, because it does not appear in either abstract, and the figures in circulation are other people's paraphrases."),
        ("p", "Running fitness fading faster is not an argument against the break. It comes back faster too, and rebuilding it is precisely what the off-season block exists to do."),
        ("p", "What does not recover on its own is the accumulated wear of a full season, and the only thing that addresses it is time you do not spend training."),

        ("h2", ("not-stopping", "Rest is not the same as stopping")),
        ("p", "A break is two or three weeks, planned, at a known point in the year, with a date it ends on. Stopping is what happens in the middle of a pre-season when you started at somebody else's pace and ran out."),
        ("pull", "Take the break on purpose and you won't need one later."),

        ("h2", ("then", "Then it starts")),
        ("p", "When the reset ends, the off-season block begins with easy running and two lifts a week. Not because it is a gentle way back in, but because it is the base that everything after it is built on."),

        ("plan", [
            "Post-season reset is a phase like any other, with its own dates, and it is the only phase in the app that tells you not to train hard. It ends when the calendar says it ends rather than when you feel ready, which is the point of putting it on a calendar.",
        ]),
    ],
))


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #

def guide_jsonld(g):
    return f"""{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{g['heading']}",
  "description": "{html.escape(g['description'], quote=True)}",
  "inLanguage": "en-AU",
  "datePublished": "{PUBLISHED}",
  "mainEntityOfPage": "{BASE}/{g['slug']}",
  "isPartOf": {{ "@id": "{BASE}/#site" }},
  "author": {{ "@id": "{BASE}/#org" }},
  "publisher": {{ "@id": "{BASE}/#org" }}
}}"""


def build_guide(g):
    body = [f"    <h1>{g['heading']}</h1>"]
    body.append(render(g["blocks"]))
    body.append(f"""
    <div class="end">
      <h2>Try it on your own season</h2>
      <p>Footy Ready builds this into a plan around your dates, your body and the gear you actually have. The assessment, your whole season across all six phases, and one real session generated from your own answers are free.</p>
      <p><a class="cta" href="{APP}?ct={g['ct']}">Get it on the App Store</a></p>
      <p class="note">iPhone only. No account and no sign-in.</p>
      <p class="backlink"><a href="guides.html">All six guides</a></p>
    </div>""")
    return page(g["slug"], f"{g['title']}: Footy Ready", g["description"],
                "\n".join(body), guide_jsonld(g))


def build_hub():
    cards = "\n".join(
        f'      <a href="{g["slug"]}">\n'
        f'        <h3>{g["heading"]}</h3>\n'
        f'        <p>{g["blurb"]}</p>\n'
        f'      </a>'
        for g in GUIDES
    )
    body = f"""    <h1>Guides</h1>
    <p class="meta">Six of them, and that is all of them</p>

    <p class="lede">Six guides on building a pre-season, written from the same material the app is built on. Every number names its study and the people it was measured on, and where the evidence is thin the guide says so rather than rounding it up.</p>

    <p>This is a finite set rather than a blog. It is complete, nothing here is waiting on a posting schedule, and none of it carries a date, because a date on a guide about how to train implies a freshness that the underlying material does not have and does not need.</p>

    <div class="cards">
{cards}
    </div>

    <h2 id="codes">One pre-season, four codes</h2>
    <p>These are written for amateur Aussie rules, rugby league, rugby union and soccer players without distinction, because the off-season problem is the same in all four: the strength, the running and the soft-tissue work that every football code shares.</p>
    <p>Where a study measured one code, the guide says which one, because they are not interchangeable and a finding from a professional rugby league squad is not automatically true of amateur soccer. What none of this covers is skills, kicking, or contact and tackle conditioning. That is your coach's job and the app does not pretend otherwise.</p>

    <div class="end">
      <h2>Build your own season</h2>
      <p>Round 1 is a date, not a surprise. Build your plan in about five minutes and play your first session today.</p>
      <p><a class="cta" href="{APP}?ct=guides-hub">Get it on the App Store</a></p>
      <p class="note">Or read <a href="how-it-works.html">how the plan is built</a>, which is the method in full.</p>
    </div>"""
    jsonld = f"""{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Footy Ready guides",
  "description": "Six guides on building a football pre-season, each citing its sources and the population they were measured on.",
  "inLanguage": "en-AU",
  "isPartOf": {{ "@id": "{BASE}/#site" }},
  "publisher": {{ "@id": "{BASE}/#org" }},
  "hasPart": [
{chr(10).join(f'    {{ "@type": "Article", "headline": "{g["heading"]}", "url": "{BASE}/{g["slug"]}" }}' + ("," if i < len(GUIDES) - 1 else "") for i, g in enumerate(GUIDES))}
  ]
}}"""
    return page("guides.html", "Guides: Footy Ready",
                "Six guides on building a football pre-season: where to start, coming back after the off-season, training without a gym, what a week looks like, counting back from round 1, and the post-season break.",
                body, jsonld)


def build_sitemap():
    urls = [("", "1.0"), ("guides.html", "0.8"), ("how-it-works.html", "0.8")]
    urls += [(g["slug"], "0.7") for g in GUIDES]
    urls += [("support.html", "0.5"), ("privacy.html", "0.3")]
    rows = "\n".join(
        f"  <url>\n    <loc>{BASE}/{slug}</loc>\n"
        f"    <lastmod>{PUBLISHED}</lastmod>\n    <priority>{pri}</priority>\n  </url>"
        for slug, pri in urls
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{rows}\n</urlset>\n")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    written = []
    for g in GUIDES:
        with open(os.path.join(here, g["slug"]), "w", encoding="utf-8") as fh:
            fh.write(build_guide(g))
        written.append(g["slug"])
    with open(os.path.join(here, "guides.html"), "w", encoding="utf-8") as fh:
        fh.write(build_hub())
    written.append("guides.html")
    with open(os.path.join(here, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(build_sitemap())
    written.append("sitemap.xml")
    for name in written:
        print("wrote", name)
