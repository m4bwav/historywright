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
