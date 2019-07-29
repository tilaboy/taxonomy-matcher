
# gazetteer-matcher

## Description

Given a gazetteer/taxonomy and some input document, `gz-matcher` could be used to find all matched phrases

## Requirements

Python 3.6+

## Installation

    pip install gz-matcher


## Usage

### Use gazetteer-matcher module
- From normalized table in json format:
```
from gz_matcher.matcher import GazetteerMatcher
gz_matcher = GazetteerMatcher(normtable=json_file)
for matched in gz_matcher.matching(text):
    print(matched)
```

And an example of the Taxonomy in JSON:
```
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
```

- From gazetteer:
```
from gz_matcher.matcher import GazetteerMatcher
gz_matcher = GazetteerMatcher(gazetteer=gz_file)
for matched in gz_matcher.matching(text):
    print(matched)
```

and an example of the gazetteer

```
# gazetteer
mobile data
risk analysis
quantitative risk assessment
risk assessment
.....
```

- From Taxonomy Codetable:
```
from gz_matcher.matcher import GazetteerMatcher
ct_matcher = GazetteerMatcher(codetable=ct_file)
for matched in ct_matcher.matching(text):
    print(matched)
```

CodeTable is a XML version of the JSON example given above.

### other functions
- Context words:
When context are needed for extracted phrases, e.g. for some validation functions, enable the with_context option:
```
from gz_matcher.matcher import GazetteerMatcher
gz_matcher = GazetteerMatcher(normtable=json_file,with_context=True)
for matched in gz_matcher.matching(text):
    print(matched.left_context, matched.right_context)
```

- Code Property lookup
If need to lookup the property of an Code in the taxonomy, check the matcher Class
property 'code_property_mapping', it is a dictionary mapping id to description and
category, it is in the form of:

```
dict[code_id] = {
    'desc':code_description,
    'type':code_category
}
```

E.g. to get the description of the codeid:
```
codeid = 12345
from gz_matcher.matcher import GazetteerMatcher
gz_matcher = GazetteerMatcher(normtable=json_file)
if codeid in gz_matcher.code_property_mapping:
    print(gz_matcher.code_property_mapping[codeid]['desc'])
```

### check the metainfo of the Taxonomy or Gazetteer:
Note: currently only available for the Normalized code json.

The metainfo can be stored in meta part of the json document,
e.g. if the following information is listed in the json meta section:
```
"meta": {
  "language": "EN",
  "release_datetime": "2019-04-17T12:22:10.729673",
  "concept_type": "skills",
  "purpose": "normalization"
},
```

We can fetch it via the matcher object
```
from gz_matcher.matcher import GazetteerMatcher
gz_matcher = GazetteerMatcher(normtable=json_file)
print(gz_matcher['meta_info'])
```

output will be:
```
{'language': 'EN',
'release_datetime': '2019-04-17T12:22:10.729673',
'concept_type': 'skills',
'purpose': 'normalization'}
```


### output of the matching: MatchedPhrase
matcher.matching is a iterable which return a MatchedPhrase instance, the instance has the following attributes:
  - normalize pattern form: matched_pattern
  - surface form: surface_form
  - start position and end position: start_pos, end_pos
  - code_id and code_description (None if not set in the pattern file)
  - left context and right context of the extracted skills (only availabe if with_context=True )

```
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
```


## Development

To install package and its dependencies, run the following from project root directory:

	python setup.py install

### Testing

To run unit tests, execute the following from the project root directory:

	python setup.py test
