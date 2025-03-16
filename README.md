# EntryWave

EnteryWave is a CLI or GUI utility that repeatedly adds text into a text file until a specified line count is reached.

## Features

**Random Numbers** - You can use any random number between 0 and 32,768 in the file name, contents, or line count. Simply put `&random&` where you would put your value, and the program will automatically generate a random number for that particular value.

**Line Count** - You can add `&linecount&` in the file contents to add the current line count. For example, `Line &linecount&` would be `Line 20`, if the line was on line 20.

**And even more, coming soon!**

## Speed

It all really depends on your own PC's specs, but with my PC with an i3-12100F, generating 100,000,000 `&linecount&` lines took 32.21 seconds, with an average of 3,104,939.42 LPS (Lines Per Second).
