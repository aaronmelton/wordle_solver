# TODO

1. Create a GUI front-end to improve use.
2. Remove logging; Does anyone else actually care about this?
3. Improve possible matches by ignoring words that contain a matching letter in
the same position as a former yellow letter.  For example: If you guess AUDIO
and get a yellow match on the letter "I", the script should remove all words
that also contain an "I" in the 4th position.
4. Input validation.
5. Accept no matches for yellow/green words (sometimes produces error).