<a href="https://travis-ci.org/innolitics/dicom-standard">
   <img src="https://travis-ci.org/innolitics/dicom-standard.svg?branch=master">
</a>

# DICOM Standard Parser

This program parses the web version of the [DICOM Standard][nema] into human
and machine-friendly JSON files. The purpose of these JSON files is twofold:

1. To provide a standardized and machine-readable way to access DICOM Standard
   information for software applications

2. To provide a logical model for the relationships between cross-referenced
   sections in the DICOM Standard

The finalized JSON output of this program is in the `standard` directory at the
top level of this project.

These JSON files are used to make the [DICOM Standard Browser][standard-browser].

[nema]: http://dicom.nema.org/
[standard-browser]: https://dicom.innolitics.com

## JSON Data Guarantees

The JSON generated by this program adheres to the following four rules:

1. New fields may be added
2. Bugs or incorrect data will be fixed as the standard changes
3. No fields are removed, maintaining backwards compatibility
4. The shape and organization of the JSON files will remain the same

The JSON files can be viewed [here][json_link].

[json_link]: https://github.com/innolitics/dicom-standard/tree/master/standard

## JSON Data Format

The generated JSON files conform to these formatting rules:

- JSON files representing tables are lists of objects, each object containing a unique `id` field
- JSON files containing relational data between tables contain "foreign keys" to the relevant table JSON file. These field names end with `Id` (e.g. `ciodId` and `moduleId`)

Occasionally, files may deviate from this format when there is a very compelling reason. For example, `references.json` should be a list of reference objects where the href is the `id` for each object. However, since almost every use case for `references.json` will use the `href` as a lookup, it makes more sense for the file to be set up as an object containing href to HTML pairs.

Applications that use the JSON files from this repository may need to re-organize data. A separate script must be written to join data from multiple tables into one file or prune out unnecessary fields.

## Current Status

This program currently parses the DICOM Standard sections related to
Information Object Definitions, modules, and attributes, as well as
cross-referenced sections in other parts of the standard. This translates to
the following sections:

Completely processed:

- PS3.3
- PS3.6

Processed for references:

- PS3.4
- PS3.15
- PS3.16
- PS3.17
- PS3.18

## Development Setup

The python scripts used to generate the JSON files are designed to be as
extensible as possible. If you want to run the code yourself or configure your
own custom parsing stage, you'll need the following system-level dependencies:

- Python 3.7
- Make + Unix tools

You will probably also want to setup a "virtual environment" (e.g. using Conda,
or Pyenv + Virtualenv) to install the project dependencies into.  Once you are
in your "virtual environment", you can run:

    $ make

to install and compile everything. Add the `-j` flag to speed this process up
significantly.

### Updating the Standard

To download and parse the most up-to-date web version of the DICOM Standard,
run the following commands:

    $ make clean
    $ make updatestandard
    $ make

## Using the Library

Parsing stages are indicated by prefixed names (i.e. `extract_xxx.py` or
`process_xxx.py`) and use a variety of utility functions from `parse_lib.py`
and other `*_utils.py` modules.

### Design Philosophy

The overall data flow of this program takes the following form:

```
          extract                      (post)process
Raw HTML ---------> JSON intermediate ---------------> JSON final

```

During this process, the following invariants are maintained:

- Each step in the parsing process is classified as either an "extract" stage,
  or a "process" stage.
- Stages are python scripts that take one or more files as inputs, and write
  their output to standard out.
- "Extract" stages takes one more more HTML input files and print out JSON.
- "Process" stages take one or more JSON files as inputs and print out JSON.

In this way, raw HTML is not touched by any stage other than `extract_*.py`,
and successive processing steps use increasingly refined JSON.

### Parser Stages

A map of all extraction and processing pathways is shown below:

![process_map]

## Contact

Find a bug? JSON files missing a piece of information? [We welcome pull
requests!][gh_link] Feel free to make a PR or make a GitHub issue for any bugs
you may find.

[process_map]: https://user-images.githubusercontent.com/9055029/78311870-b33c6a00-7517-11ea-8366-8cd2cc3ea745.png
[gh_link]: https://www.github.com/innolitics/dicom-standard