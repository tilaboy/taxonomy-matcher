taxonomy-matcher
=================

CI Status
-----------

.. image:: https://travis-ci.org/tilaboy/taxonomy-matcher.svg?branch=master
    :target: https://travis-ci.org/tilaboy/taxonomy-matcher

.. image:: https://pyup.io/repos/github/tilaboy/taxonomy-matcher/shield.svg
    :target: https://pyup.io/repos/github/tilaboy/taxonomy-matcher/
    :alt: Updates

.. image:: https://readthedocs.org/projects/gazetteer-matcher/badge/?version=latest
    :target: https://gazetteer-matcher.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Description
-----------

Given a gazetteer/taxonomy and input text, ``taxonomy-matcher`` can
be used to find all phrases which matches the codes/instances/keywords in the
gazetteer or taxonomy.

For each match, it will return the information of,

  - surface_form

  - matched position

  - Code ID and Code Description

  - and other code related information



Requirements
------------

Python 3.6+


Usage
-----

Use taxonomy-match script:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    usage: taxonomy-match input_file taxonomy_file [--output_file OUTPUT_FILE]


    load taxonomy phrases from the taxonomy file, and find all matched phrases
    from the input text. The result will eithor write to an output file or print
    to the screen.

    positional arguments:
      input_file            input text file, text to mine phrases
      taxonomy_file         taxonomy file, support json/xml/txt, see documentation
                            for more details

    optional arguments:
      --output_file         output file of matched phrases, supports
                            jsonl/csv/tsv/txt format, print matched phrases to
                            the screen if not defined


Use taxonomy-matcher module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  From normalization table in JSOM format:

::

   from taxonomy_matcher.matcher import Matcher
   taxonomy_matcher = Matcher(normtable=json_file)
   for matched in taxonomy_matcher.matching(text):
       print(matched)

And an example of the normalization table in JSON:

::

    {
      "meta": {
        "concept_type": "skills",
        "release_datetime": "2019-xx-xx"
      },
      "concepts": [
        {
          "display_name": "Risk Analysis",
          "category": "Financial Skill",
          "id": "ABCDEFG001",
          "surface_forms": [
            {
              "surface_form": "risk analysis",
              "skill_likelihood": 0.9
            },
            {
              "surface_form": "quantitative risk assessment",
              "skill_likelihood": 1.0
            },
            {
              "surface_form": "risk assessment",
              "skill_likelihood": 0.7
            }
          ]
        },
        .......
        {
          "display_name": "Mobile Data",
          "category": "Computer Skill",
          "id": "ABCDEFG002",
          "surface_forms": [
            {
              "surface_form": "mobile data"
            }
          ]
        }
      ]
    }

-  From gazetteer:

::

   from taxonomy_matcher.matcher import Matcher
   taxonomy_matcher = Matcher(gazetteer=gz_file)
   for matched in taxonomy_matcher.matching(text):
       print(matched)

and an example of the gazetteer

::

    # gazetteer
    mobile data
    risk analysis
    quantitative risk assessment
    risk assessment
    .....

-  From Taxonomy Codetable:

::

   from taxonomy_matcher.matcher import Matcher
   ct_matcher = Matcher(codetable=ct_file)
   for matched in ct_matcher.matching(text):
       print(matched)

CodeTable is a XML version of the JSON example given above.

other functions
~~~~~~~~~~~~~~~

-  Context words:

When context are needed for matched phrases, e.g. for the following up
validation functions, enable the ``with\_context`` option:

::

   from taxonomy_matcher.matcher import Matcher
   taxonomy_matcher = Matcher(normtable=json_file,with_context=True)
   for matched in taxonomy_matcher.matching(text):
       print(matched.left_context, matched.right_context)

-  Code Property lookup

If need to lookup the property of an Code in the taxonomy,
check the matcher Class property 'code\_property\_mapping',
it is a dictionary mapping id to description and category, it is in
the form of:

::

    dict[code_id] = {
        'desc':code_description,
        'type':code_category
    }

E.g. to get the description of the codeid:

::

    codeid = 12345
    from taxonomy_matcher.matcher import Matcher
    taxonomy_matcher = Matcher(normtable=json_file)
    if codeid in taxonomy_matcher.code_property_mapping:
        print(taxonomy_matcher.code_property_mapping[codeid]['desc'])


check the Metainfo of the Taxonomy or Gazetteer:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Note: currently only available for the Normalized code JSOM.

The metainfo can be stored in meta part of the JSON document, e.g. if
the following information is listed in the JSOM meta section:

::

    "meta": {
      "language": "EN",
      "release_datetime": "2019-04-17T12:22:10.729673",
      "concept_type": "skills",
      "purpose": "normalization"
    },

We can fetch it via the matcher object

::

    from taxonomy_matcher.matcher import Matcher
    taxonomy_matcher = Matcher(normtable=json_file)
    print(taxonomy_matcher['meta_info'])

output will be:

::

    {
      'language': 'EN',
      'release_datetime': '2019-04-17T12:22:10.729673',
      'concept_type': 'skills',
      'purpose': 'normalization'
    }

matched phrase object: MatchedPhrase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

matcher.matching is an iterable which return a MatchedPhrase instance,
the instance has the following attributes:

- normalize pattern form: matched\_pattern

- surface form: surface\_form

- start position and end position: start\_pos, end\_pos

- code\_id and code\_description (None if not set in the pattern file)

- left context and right context of the matched skills (only availabe if with\_context=True )


::

    for match in matcher.matching(text):
        print("found pattern [{}] in the form of [{}] at position ({}:{}), code:{} {} {}".format(
            matched.matched_pattern
            matched.surface_form
            matched.start_pos
            matched.end_pos
            matched.code_id
            matched.code_description
            matched.category
            matched.left_context
            matched.right_context
        )

Development
-----------

To install package and its dependencies, run the following from project
root directory:

::

    python setup.py install

Testing
~~~~~~~

To run unit tests, execute the following from the project root
directory:

::

    python setup.py test
