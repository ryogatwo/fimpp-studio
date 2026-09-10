FIM++ program structure
=====================

FIM++ programs can have one of two structures:

* Main function contains functions inside (wrapped style).

* Functions precede the main function, and the main function, being the last one in the code, contains statements (C style).

In all examples below, colons can be replaced with full stops, except after the word Celestia. Parts in braces {...} are optional.

Wrapped style:
-------------

Execution of the program will start from the function that has the same name as the main function. It will be called with no arguments.

    Dear Princess Celestia: <module identifier> :

	Today I learned {about} <identifier: main function name>:

		<function declarations>

	Your faithful student, <identifier>.

C style
------

Execution of the program will start from the main function.

    Dear Princess Celestia: <module identifier> :

    <function declarations>

	Today I learned {about} {<identifier: main function name>}:

		<statements>

	Your faithful student, <identifier>.

Postscript comments
-------------------

After the signature, either program structure may include comments:

    Your faithful student, Twilight Sparkle.
    PS This is a note.
    PSS This is another note.
    P.S.No space is required after a dotted marker.
    P.P.S.This is the spelling in the FiM++ 1.0 specification.

Comments end at a newline or end of file. Markers are case-insensitive and
also work between statements or after statements on the same line.
`P.S.S.`, additional `P.` prefixes, and undotted `PPS` are accepted too.
Quoted text is not treated as a comment. Use a marker on each comment line.
