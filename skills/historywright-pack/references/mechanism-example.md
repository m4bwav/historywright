# Example: the Mechanism section of an anachronism checklist

Back to [SKILL.md](../SKILL.md) (Step 4) and [contract.md](contract.md). This is the Mechanism section of a real
pack, a small water-powered sash sawmill of 1790-1840, built on 2026-10-23. It shows the shape: one numbered
item per link of the drive chain, from the power source to the tool, each saying what the part is, where it must
sit and what it drives, with sizes and citations; then the things a picture or model must never show. The pack's
`manifest.json` has `historywright.mechanism: true`, so `hw.py validate-pack` requires this section to have items.

Source key for the excerpt: [s1] Oliver Evans, *The Young Mill-wright & Miller's Guide* (1795), saw-mill article
and Plates XI-XIV; [s2] HABS PA-116, Up-and-Down Sawmill, Chester Springs, data pages; [s5] HABS NH-45, James Saw
Mill, measured drawings; [s7] HABS NH-31, Nichols Saw Mill, measured drawings; [s9] M. Powis Bale, *Woodworking
Machinery* (1880); [s10] and [s11] two mills converted to circular saws in the 1870s and 1880s.

```markdown
## Mechanism: what drives what, and where it must sit

The drive chain, from the water to the blade. Every link must be visible or plainly implied, and connected.

1. **Millpond, then headrace.** A timber flume or forebay leads from the pond above the dam to the wheel, with a
   gate at its head, lifted by a lever from the saw floor. Nichols: 4 ft 6 in (1.37 m) wide flume (sheets 12-13) [s7].
2. **Wheel, in the water at the foot of the flume.** It sits under the saw floor, directly below the saw gate
   (Nichols sheet 2; James sheet 5) [s5] [s7], or in a lean-to beside the foundation when it is a larger undershot
   wheel [s2]. Spent water leaves by the stream bed under the mill [s7].
3. **Horizontal wheel shaft, with the crank on its end.** On a flutter wheel the crank is on the wheel shaft
   itself [s1]; crank throw 12 in, so the saw stroke is 24 in [s1]. **No gears in a flutter-wheel mill.**
   - Geared variant (rarer, "expensive and but little used"): a large wheel turns a spur cog wheel that drives a
     wallower on a second shaft carrying the crank, about 9:1 [s1]. The gears sit inside the mill on framed timbers.
4. **Pitman (connecting rod).** A long vertical squared timber from the crank wrist straight up through a slot in
   the saw floor to the bottom rail of the saw gate [s1] [s5].
5. **Saw gate (sash).** A rectangular timber frame about 6 ft (1.83 m) wide with the blade strained vertically in
   the middle, sliding up and down between two vertical fender posts 12 ft (3.66 m) tall [s1].
6. **Carriage feed.** A lever on the gate works a hand-pole whose iron hand turns a 5 ft (1.52 m) rag wheel by
   ratchet; its shaft drives cogs under the 29-32 ft carriage, which creeps forward on ways the length of the mill [s1].
7. **Return.** A separate small tub wheel on a vertical shaft runs the carriage back [s1] [s7].

## Prohibitions a picture or model must obey

- **No circular blade before about 1840 in a small country mill.** Circular saws were dockyard and workshop machines
  [s9]; country mills converted in the 1870s-1880s [s10] [s11].
- **No blade on the roof, on an outdoor bench, or outside the building.** The sash stands vertical inside the saw
  floor, between its fender posts, over the slot through which the pitman rises [s1] [s7].
- **No wheel without a shaft into the building**, and no wheel on the dry side: it sits in the flume or tail water [s1] [s5] [s7].
- **No free-floating gears.** Every cog wheel sits on a shaft in bearings on framed timbers and meshes with another [s1].
- **The wheel is not huge and slow in a direct-crank mill.** One stroke per turn means about 100-120 turns a minute:
  a small flutter wheel about 0.8-0.9 m across, not a 5 m wheel [s1].
```

Why it matters: the prohibitions name the mistakes pictures of machines make (a blade outside the building, a
wheel with no shaft into it, gears floating in the air). The answer can hold every fact and still not say where
each part sits; this section is what a generated picture or a model is checked against (LEARNINGS L-010).

## The water path

The same pack was later extended for a wide picture of the mill in its landscape, where the drive chain inside
the mill says nothing about where the water comes from and goes. Image models' commonest error there was water
pouring out of the wheel's hub. `pack init --mechanism` now writes a "Water path (water-powered machines)"
subsection with one placeholder per item; this is the pack's filled version for its large undershot wheel, cut
down. Source key: [s1] Evans 1795 as above (its articles on undershot mills, canals and dams); [s2] HABS
PA-116 as above; [s8] HABS CT-63, Buttery Mill, Silvermine, written data; [s14] William Fairbairn, *Treatise on
Mills and Millwork*, Part I (London, 1864), chapters I (weirs), III (water-wheels) and IV (the undershot wheel).

```markdown
### Water path (water-powered machines)

1. **Source.** A dam or weir across the river, "a sufficient distance" above the mill, with a tumbling space to
   pass floods [s1]; a sluice gate in one wing wall of the weir draws off surplus water [s14]. Chester Springs
   took its water from an adjacent stone dam [s2].
2. **Head race.** A dug canal from the pond to the mill, which is "set well into the bank"; surplus runs back to
   the river over a waste left in the canal's bank [s1]. Evans's worked example: about 3 ft deep and nearly
   10 ft wide for a 15 ft wheel on 5 ft of head [s1].
3. **Gate.** A sluice (the shuttle) at the end of the forebay, drawn "as near the float-boards as possible" [s1].
4. **Where the water meets the wheel (undershot).** The forebay slants down under the wheel so the gate opens
   near the floats [s1]; the water is applied near the bottom of the wheel, rushing out under the shuttle
   against the floats [s14].
5. **Turning direction.** The bottom floats move downstream with the water, the top upstream; the tail race lies
   in the same direction as the wheel's revolution [s14].
6. **Tail race.** Sunk about 1 ft [s1], or two to two and a half feet [s14], below the bottom of the wheel, and
   carried back to the river below the mill [s14].

Never show:

- **No water from the hub, axle or shaft.** Water reaches an undershot wheel at the bottom of its rim [s1] [s14].
- **No trough ending above the wheel**, no flume on trestles: that feeds an overshot wheel, as at Buttery Mill [s8];
  an undershot wheel takes its water at the bottom, from a race at ground level [s14].
- **The wheel sits in its race**, lowest floats in the water between the race walls, its shaft running into
  the mill wall [s1] [s2] [s14].
```

How it was found: both books are Internet Archive OCR text. Evans's 1795 printing uses the long s, which the OCR
reads as "f", so "shot" is "fhot" and "sufficient distance" is "fufficient diftance"; `hw.py fetch <url> --find
shot` tries those spellings itself. Fairbairn (1864) writes 70 years later in England, but his chapter on the
undershot wheel's "old forms" describes the wooden wheels of the period, and he and Evans agree.
