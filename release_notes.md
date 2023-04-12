# RefRed Reduction Application for the Liquids Reflectometer

## Release notes

 - version 5 [04/2023]: RefRed v5 now uses a new reduction package <https://github.com/neutrons/LiquidsReflectometer>. Apart from being an event-based implementation of the same reduction process, the main difference with previous version is the addition of a gravity correction and the use of an effective sample-to-detector distance that takes into account the average emission time of neutrons in the moderator.

   Other changes to version 5 include:
    - The normalization option (which is a global option in the current UI) was ignored. It's now also saved properly.
    - The boolean options in the config file were ignored because they were not loaded properly.
    - The table headers on the main page were missing.
    - The Settings panel is no longer useful and has been hidden until we refactor the configuration.
    - A typo made the background subtraction option default to true.
