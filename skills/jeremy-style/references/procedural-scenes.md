# Procedural adaptation and dimensional honesty

This is a build specification, not tested renderer code. The analysis task did not render a new scene or install a 3D package. Verify the chosen project's actual dependencies and a small encoded test before claiming production readiness.

## Existing solution preflight

Inspect the existing local Remotion project and local 3D guide, if one exists. Reuse an adequate verified renderer rather than building another engine. In a Remotion implementation a compatible Three.js/React Three Fiber integration may supply real geometry, lights and camera, but do not assume @remotion/three, three or @react-three/fiber is installed merely because the 2D Remotion skill exists. Pin compatible versions only with authorized project-local dependency changes; read scripts/license and lockfile first. Do not change shared runtime configuration. A separately verified local 3D renderer can generate original plates for a Remotion/NLE assembly; preserve the underlying scene source and label plate editability honestly.

## Select the representation by scene need

- 2D: flat text, graph, arrows, choice card, UI, schematic figure. No perspective camera/light simulation is needed.
- 2.5D: flat billboards/cutouts at separated depths, layered school/stage backdrop, simulated zoom/parallax. Label it a low-cost adaptation; do not claim a head turning in perspective or a spatial reverse angle from a single PNG.
- Real 3D: spherical/rounded geometry, rigged limbs and faces placed in scene coordinates, perspective camera, physically consistent occlusion and lighting. Use for walk-throughs, turns, over-shoulder exchange, high corridor views and set/venue scale changes.
- Hybrid: use real 3D for the protagonist/foreground/near props; flat/instanced stylized extras for distant crowds; screen-space diagrams and text over the result. The reference shows graphic crowd/diagram treatments alongside volumetric heroes. Do not assume every background extra is a fully rigged 3D character.

Observable evidence strongly supports a 3D-rendered visual appearance; it does not establish the source author's exact software, mesh topology, physical lens or whether any shot was subsequently composited.

## Build sequence with gates

1. Block a neutral hero in a gray studio. Normalize total height H=1. Use a sphere head diameter approximately 0.35–0.42H; a rounded box/capsule hoodie torso approximately 0.25–0.30H high; narrow neck, capsule upper/lower limbs and sphere/mitten hands. Add simple shoes. These are proposed ratios. **Gate:** front/side/three-quarter views read as the same character without clipping.
2. Create face controls independent from head rotation: gaze direction, eyelid openness, brow angle/height, mouth curve/opening and optional blush. Place dark face decals/curves slightly above the head surface without z-fighting or floating far off it. **Gate:** neutral, confident, surprised, worried and thinking expressions remain readable at actual delivery size. No unintended white teeth in this user's talking derivative.
3. Establish pose controls for shoulder/elbow/wrist and hip/knee/ankle, or an equivalent simple hierarchy. Ground feet with leg length constraints; attach carried props to hands, not the camera. Cache fixed pose keys for explain, point, think, react and rest. **Gate:** poses are genuinely different, contact points stay attached and silhouette is clear.
4. Block a reusable set with a floor, back wall, a few large props and one practical light source. A classroom needs desks/benches, perspective windows and a few identifying wall shapes, not a fully decorated school. A bedroom needs bed, side table and doorway. A corridor needs repeating lockers, ceiling fixtures and an end wall. **Gate:** the location and geography read without tiny labels.
5. Add motivated lights and materials, then test a face closeup and a wide shot. Keep overlay type outside depth-of-field. Avoid relying on bloom to hide low contrast. **Gate:** expression, footing and primary prop remain readable before post effects.
6. Add the information layer. Anchor a line endpoint to a character/chest/prop in world space; project to screen for a screen-space counter or keep line geometry in world coordinates as the shot demands. Specify what the line means and where it begins/ends; do not use a decorative beam with no story function. **Gate:** overlays track their intended subjects through camera movement without penetrating unrelated geometry.
7. Block camera cuts from an establishing view to an action two-shot and a reaction closeup. Confirm eye lines and screen direction. Only then add a slow push or reveal if motivated. **Gate:** the viewer can identify who looks at whom and what changed.
8. Add secondary cast/crowd and finishing last. Reuse geometry/materials, instance repeated seats/extras, use coarse detail at distance and keep expensive shadows/DOF/bloom limited. **Gate:** render time/memory are measured on a short sample and no hero is lost in crowd noise.

## Scene families to reuse

**Social encounter:** a medium two-shot at a desk/rail; one speaks/gestures, the other reacts. Keep the foreground head/shoulder as an optional spatial cue, not a permanent obstruction. Pink line or small count appears only when the story activates that mechanic. Cut to expression to show the consequence.

**Private consequence:** isolate the protagonist in a bedroom/quiet corner. Put the hands in thinking/resting poses, use modest motion and negative space. Lower visual density to let an emotional line land. Do not force the upbeat gym palette onto a quiet night shot.

**Explanatory board:** dark purple field with subtle grid/vignette; gold heading; two simplified figures, one diagram or a ranked comparison. Keep the graphic's meaning and units explicit. Use a short return transition to the story so the diagram answers a question rather than becoming a separate slideshow.

**Scale reveal:** establish one person, then cut/pull back to repeated seats/people or a venue overview. Use instancing or flat distant extras where appropriate. Keep near characters volumetric if the camera passes them. Never imply an illustrative crowd count is a measured fact.

**Resolution and end card:** reduce complexity to one emotional exchange, reuse the line motif, then finish on a legible question/choice layout. Engagement elements are optional to the user's brief, not mandatory source branding.

## Deterministic rendering contract

Drive pose curves, camera paths, shader time, line pulse and particle positions from the renderer's frame/fps clock; seed procedural randomness and record seed. Avoid requestAnimationFrame/wall-clock animation or time-dependent random choices in exported sequences. Evaluate transforms for arbitrary requested frames, because a frame renderer can seek non-sequentially. Keep camera targets and focal distance explicit. Clamp eased controls to valid ranges; use quaternion rotation interpolation or tested rig controls to avoid flips. Do not claim a particular spring/easing duplicates the original from quarter-second samples.

For a Remotion composition keep narration outside individual visual sequences to avoid restarts. Measure audio and calculate total frame coverage from that measurement; the reference's 60fps is an observation, not a universal requirement. Test project-supported 30 or 60fps as appropriate. Keep all original 3D/model/material and shot timing sources with the final plate; a flattened MP4 alone is not an editable scene.
