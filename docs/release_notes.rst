.. _release_notes:

Release Notes
=============

<Next Release>
--------------
(date of release, with format YYYY-MM-DD)

**Of interest to the User**:

- MR #XYZ: one-liner description

**Of interest to the Developer:**

- PR #154: Convert to pixi from conda
- MR #152: Modernize installation process from setup.py to pyproject.toml


5.2.1
-----
YYYY-MM-DD

**Of interest to the User**:

- MR #XYZ: one-liner description

**Of interest to the Developer:**

-  PR #150 Update mantid to 6.12.0

5.2.0
-----
2025-03-18

**Of interest to the User**:
- MR #141: Add instrument geometry settings to reduction workflow
- MR #138: remove right-click option "Display Metadata..." from the reduction table
- MR #135: update popup message for v4 deprecation
- MR #134: add column in the reduction table for constant Q binning during reduction


**Of interest to the Developer:**
- MR #126: structure documentation and publish in readthedocs

5.1.0
-----
2024-07-16

**Of interest to the User**:

- MR #118: add detector dead-time correction to the scaling factor calculation
- MR #117: add detector dead-time correction to the reduction workflow
- MR #111: dialog to set the peak and background boundaries
- MR #108: Introduce a second background for better peak resolution

**Of interest to the Developer:**

- MR #109: substitute the raw numpy array big_table_data with a customized Class having meaningful method names
- MR #105: avoid accessing GUI elements from another thread than the main thread

5.0.0
-----
2023-04-23

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

