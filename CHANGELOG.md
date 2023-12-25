# CHANGELOG


## [0.7.2] - 2023-12-25
### Changed
- Updating smmap (5.0.0 -> 5.0.1)
- Updating gitdb (4.0.10 -> 4.0.11)
- Updating lazy-object-proxy (1.9.0 -> 1.10.0)
- Updating pbr (5.11.1 -> 6.0.0)
- Updating pygments (2.15.1 -> 2.17.2)
- Updating wrapt (1.15.0 -> 1.16.0)
- Updating astroid (2.15.6 -> 2.15.8)
- Updating click (8.1.6 -> 8.1.7)
- Updating gitpython (3.1.32 -> 3.1.40)
- Updating isort (5.12.0 -> 5.13.2)
- Updating numpy (1.25.1 -> 1.26.2)
- Updating packaging (23.1 -> 23.2)
- Updating pathspec (0.11.1 -> 0.12.1)
- Updating platformdirs (3.9.1 -> 4.1.0)
- Updating pluggy (1.2.0 -> 1.3.0)
- Updating pytz (2023.3 -> 2023.3.post1)
- Updating rich (13.4.2 -> 13.7.0)
- Updating tomlkit (0.11.8 -> 0.12.3)
- Updating typing-extensions (4.7.1 -> 4.9.0)
- Updating bandit (1.7.5 -> 1.7.6)
- Updating pylint (2.17.4 -> 2.17.7)


## [0.7.1] - 2023-07-22
### Changed
- Updating Python libraries.


## [0.7.0] - 2022-03-04
### Changed
- Ignoring pylint warning.
- Updating pbr (5.8.0 -> 5.8.1)
- Updating pyparsing (3.0.6 -> 3.0.7)
- Updating click (8.0.3 -> 8.0.4)
- Updating gitpython (3.1.26 -> 3.1.27)
- Updating numpy (1.22.1 -> 1.22.2)
- Updating platformdirs (2.4.1 -> 2.5.1)
- Updating typing-extensions (4.0.1 -> 4.1.1)
- Updating bandit (1.7.1 -> 1.7.4)
- Updating pandas (1.3.5 -> 1.4.1)


## [0.6.0] - 2022-02-11
### Added
- Added input validation to enforce 5-character words.
### Changed
- Searching for green letters before yellow letters to more quickly pare down
  the list.
### Removed
- Removed functions assigning value to words (need to re-work this).


## [0.5.1] - 2022-01-30
### Changed
- Broke sorting list alphabetically somewhere along the way so fixed this.
- Cleaned up the code a little bit by creating a list to track the column
  headers of the Pandas DataFrame versus typing it out at length every time it
  was called.
### Removed
- Removed some debug code.


## [0.5.0] - 2022-01-24
### Changed
- Changed all references to dataframes to specify the columns containing the
  letters.  Now that each dataframe contains more than a string the old method
  for working with dataframes no longer works.
- Changed script to allow user to determine if they want to use the easy or hard
  word list.  If they select hard it will combine both the easy and hard words
  into a single list.
### Added
- Added functionality to calculate the distribution of letters in the word list
  and apply a value to each word.  The more common letters present in a word the
  more 'valuable' the word is.  I'm not a statistician but I *think* providing
  this sorted list to the user may be useful?
- Added additional debug logging to track how the dataframe changes between
  functions.
- Added checks to the presence of yellow/green letters to prevent functions from
  attempting to process blank inputs from the user.


## [0.4.1] - 2022-01-21
### Changed
- README.md: Cleaned up headers.
- wordle_solver.png: Combined two screenshots into one image.
- wordle_solver.py: Fixed grammar.


## [0.4.0] - 2022-01-21
### Added
- get_input(), validate_input(): Added input validation.
- remove_columns(): Removed columns (rows, really) where yellows did not match.
### Changed
- Corrected matching_dataframe Pandas query to correct situations that would
  cause an error when the User supplies non-matching input.
- Renamed a couple functions to better reflect their purpose.
- README.md: Improved documentation.
- wordle_*.png: Updated to show improved functionality.


## [0.3.1] - 2022-01-20
### Changed
- Added space between Word: and the user input.


## [0.3.0] - 2022-01-20
### Changed
- Added new functions to improve code re-use.
- Addressed linting issues.


## [0.2.0] - 2022-01-29
### Added
- Added user-interactive part to collect inputs from user.


## [0.1.0] - 2022-01-18
### Added
- Creating a new project to help solve Wordle game.
- Created initial functionality to provide a list of possible matches.