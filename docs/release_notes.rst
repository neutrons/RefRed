.. _release_notes:

Release Notes
=============

<Next Release>
--------------
(date of release)

**Of interest to the User**:

- MR #XYZ: one-liner description

**Of interest to the Developer:**

- MR #XYZ: one-liner description

5.1.0
-----
2024-07-16

**Of interest to the User**:

- MR #XYZ: one-liner description

**Of interest to the Developer:**

- MR #XYZ: one-liner description

5.0.0
-----
2023-04-01

RefRed v5 now uses a new reduction package <https://github.com/neutrons/LiquidsReflectometer>.
Apart from being an event-based implementation of the same reduction process,
the main difference with previous version is the addition of a gravity correction
and the use of an effective sample-to-detector distance that takes into account
the average emission time of neutrons in the moderator.

Other changes to version 5 include:

- The normalization option (which is a global option in the current UI) was ignored. It's now also saved properly.
- The boolean options in the config file were ignored because they were not loaded properly.
- The table headers on the main page were missing.
- The Settings panel is no longer useful and has been hidden until we refactor the configuration.
- A typo made the background subtraction option default to true.
- Scaling to a Q region under Q_c now works for any Q range. It used to apply only to the first run.

