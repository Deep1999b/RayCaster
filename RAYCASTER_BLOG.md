# Building a Raycaster in Python: A Small Engine That Carried a Big Fight

Some projects are impressive because they are huge. Others matter because of what it took to finish them.

This raycaster belongs to the second kind.

On the surface, it is a compact Python project built with `pygame` and `numpy`. Underneath, it is a piece of work that asks for patience: angles that refuse to behave, walls that distort if the math is even slightly wrong, collision that feels broken until it suddenly feels natural, and rendering code that gives you almost nothing for free. A project like this is not just about making something look 3D. It is about staying with a problem long enough to understand it.

![Raycaster Screenshot](./Screenshot%20(22).png)

## What this project is

This is a classic grid-based raycaster inspired by the rendering ideas behind early first-person games. Instead of true 3D geometry, the world is stored as a 2D tile map. Every frame, the engine casts rays outward from the player, finds where those rays hit walls, and turns those hit distances into vertical wall slices on the screen.

That means the illusion of depth comes from careful math, not a heavyweight 3D engine.

In this project, the world is defined on a `30 x 20` map with a tile size of `32` pixels. The game renders to an internal surface and then scales that view to fullscreen, which is a smart choice because it keeps the raycasting math tied to a fixed resolution while still presenting cleanly on larger displays.

## The architecture in plain English

The project is split into simple modules, and that is one of its strengths.

- `main.py` runs the game loop, creates the world, updates the player, casts rays, renders the scene, and presents the final frame.
- `Settings.py` defines the core rendering constants like field of view, render dimensions, wall strip width, and texture size.
- `player.py` handles movement, strafing, mouse-look rotation, and wall collision.
- `Ray.py` performs the actual ray casting by checking horizontal and vertical grid intersections and keeping the nearest wall hit.
- `RayCaster.py` turns those ray hits into textured wall columns and writes them into a frame buffer.
- `Map.py`, `Grid.py`, and `MiniMap.py` provide the world layout, collision lookup, and top-down debug view.
- `Textures.py` loads wall textures from the asset folder and converts them into a format that can be sampled quickly during rendering.

The result is a project that stays readable even while doing something that feels visually advanced.

## How the raycasting works

The heart of the engine is the process in `Ray.py` and `RayCaster.py`.

For each frame:

1. The player angle is used as the center of the camera.
2. A set of rays is cast across the field of view.
3. Each ray checks horizontal and vertical grid intersections separately.
4. The engine keeps the closest valid wall hit.
5. That distance is corrected to remove the fisheye effect.
6. The corrected distance is converted into the height of a wall slice.
7. A matching column from the wall texture is sampled and drawn.

This is one of those ideas that sounds manageable when written as a list, but becomes difficult the moment you implement it. Every step has edge cases. Rays near flat angles can break because of tangent values. Horizontal and vertical checks need slightly different offsets. Texture coordinates need to match the exact side of the wall that was hit. And if the distance correction is wrong, the entire illusion collapses.

That is why this project deserves respect. It solves problems that are conceptually simple and practically stubborn.

## Technical details that stand out

There are a few choices here that make the project more than just a first draft.

### 1. Fisheye correction is handled properly

The wall distance is corrected with the cosine of the difference between the ray angle and the player angle. That matters because raw ray distance alone makes the edges of the screen stretch unnaturally. Fixing that is one of the big steps between "rays are working" and "this actually feels like a 3D scene."

### 2. The renderer uses a frame buffer

Instead of drawing each pixel one by one through slow high-level calls, the project stores pixel data in a `numpy` frame buffer. It then reshapes that data and blits the final result to a `pygame` surface. That is a meaningful performance-minded decision and shows a shift from "make it work" toward "make it work well."

### 3. Texture sampling is implemented directly

The textures are loaded, converted into arrays, and sampled by column depending on where the ray hit the wall. That is the part that transforms flat-colored columns into surfaces that feel tangible. Once textures appear correctly in a raycaster, the project stops looking like a prototype and starts looking like an engine.

### 4. Movement has practical polish

The player supports forward movement, backward movement, strafing, mouse-based rotation, and diagonal speed normalization. Collision is resolved independently on each axis, which allows wall-sliding instead of harsh full stops. That one detail makes movement feel far better than a naive collision system.

### 5. The minimap keeps the math visible

The minimap is not just a feature. It is a development tool. In projects like this, a minimap helps you see the relationship between the player, the map, and the rendered result. When you are debugging spatial math, visibility is survival.

## Why this kind of project is hard

What makes a raycaster difficult is not just the formulas. It is the emotional rhythm of building one.

You make a change and the screen goes black.

You fix that and the walls bend.

You fix that and collision starts failing at corners.

You fix that and the textures crawl or stretch.

You fix that and suddenly something clicks. The world holds together for a second. Then for a minute. Then for a full run.

That cycle is exhausting, especially when the codebase is small enough that every bug feels personal. There is nowhere to hide in a project like this. If something is broken, it is usually because your understanding is being tested in real time.

And that is exactly why finishing a project like this means something.

## What this project says about the developer

This raycaster is not interesting only because it renders walls in perspective. It is interesting because it shows discipline.

It shows someone willing to work through foundational graphics concepts instead of skipping to a ready-made engine. It shows curiosity strong enough to wrestle with trigonometry, coordinate systems, texture mapping, input handling, and performance tradeoffs in a single project. It shows patience, because none of this looks impressive on day one. Most of the work happens in the awkward middle, where the result is unstable and the effort is invisible.

There is also something quietly honest about this build. It does not pretend to be bigger than it is. It is a focused project with clear goals, and that makes it easier to appreciate. You can see the systems. You can trace the logic. You can tell where the hard-earned understanding lives.

## What could come next

Even in its current form, the project already proves the core engine works. From here, there are several strong directions it could grow:

- sprite rendering for enemies, objects, or pickups
- richer maps with interactive spaces and better level composition
- depth-based sprite sorting and occlusion
- doors, switches, or animated wall states
- lighting, fog, or distance-based shading
- floor and ceiling texturing
- a HUD, weapon view, or retro game presentation layer

But the important part is this: the hard part has already happened. The leap from "I want to understand raycasting" to "I built one" is much bigger than the leap from here to extra features.

## Final thoughts

This is a small engine, but not a small achievement.

A raycaster teaches you that impressive results are often built from repetitive, frustrating, highly technical steps that nobody applauds while you are doing them. You debug invisible lines. You question your math. You stare at results that are almost right and somehow more annoying than being completely wrong.

And then, eventually, a world appears.

That is what makes this project worth writing about. Not just because it works, but because it represents the kind of persistence that real learning demands. The code renders a 3D illusion. The process behind it proves something more important: you stayed with a difficult problem long enough to make it real.
