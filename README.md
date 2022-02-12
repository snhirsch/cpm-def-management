# cpm-def-management
Parse, generate and work with CP/M diskette filesystem definitions

The CP/M operating system was used on a large number of 8080 and Z80 based systems during the early years of microcomputing. Unfortunately, there was little to no standardization with regard to diskette physical format and filestructure.  Over the years there have been a number of tools developed to analyze and transfer data in or out of CP/M diskettes and captured diskette images.  Examples include 22Disk by Sydex (a commercial product) and free software such as cpmtools and libdisk.  As with the original diskette media, all of these applications had different configuration schemes, usually involving a structured text file to hold settings and parameters.  

This GitHub project is the first step towards what I hope will become a suite of utilities to read and generate CP/M definition files and translate between them.  Currently the project has working parsers for 22Disk and cpmtools that build objects representing the definition.  The objects can serialize themselves back to a text representation that logically matches the input.  Still needed are the 'smarts' to translate between the formats.

The code is written in Python (version 3.6 or greater required) and uses the Lark parser package.  Developing parser code can be a bit difficult, but I'm willing to own that bit going forward.  It would be great if others can join the effort and help with interpretation of the data and translation to other formats.  In the long view I envision a GUI tool where users can fill in a form with required information and push a button to generate definitions for the tool of their choice.  But, one step at a time.

How to work with the code:  

Install Python 3.6 or newer on your system, which can be Windows, Linux or MacOS.  Most recent Linux distributions will already have this requirement met.  Next, install the latest release of Lark.  This is generally done by running 'pip3', e.g. (for Linux) **pip3 lark**.  Lark may be available through your package manager, but it's best to get the latest release version as I do not test with older ones.  

There are (2) executable programs:

cpmtools_parser.py
twotwodisk_parser.py

These expect the name of the input definition file as a command line
argument.  I have included a large cpmtools diskdef file as a parser test, but
have not reviewed the contents for correctness with cpmtools and real data. The
22Disk definitions are technically proprietary to Sydex so I have not included them
in the project.

The parsers will complain about any obvious syntax errors, missing
required parameters and, in the case of 22Disk, parameter
ordering. More checking can and should be added.

If no syntax errors are found, the program will read all definitions
in alphabetical order and serialize their contents to stdout as valid
definitions.
