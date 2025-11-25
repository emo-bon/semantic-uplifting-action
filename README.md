# semantic-uplifting-action

## Usage 

Example workflow file:

```
on:
  push:
jobs:
  job0:
    runs-on: ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v3
      - name: semantify
        uses: vliz-be-opsci/semantify@main
      - name: commit
        uses: stefanzweifel/git-auto-commit-action@v4
```

## Description 

The purpose of this package is to automate the semantic uplifting of tabular data into RDF triples, based on predefined templates that specify both the data model and the semantics of the data values.

The package supports a configurable and reusable workflow for transforming structured data (e.g. CSV or other tabular formats) into semantically rich triples using templates that reflect domain-specific ontologies or data models.

Contents of this package include:
- The core logic for interpreting and applying semantic uplifting templates
- Support for configurable iteration and population of template parameters
- Integration with environment-specific settings and profiles
- Utilities for reading input data and writing output triples
- Interfaces for working with templating rules, transformation logic, and output formats

This package is typically used within the context of `./*-profile` repositories that define specific semantic uplifting configurations and templates, such as for example:    
- [observatory profile](https://github.com/emo-bon/observatory-profile)
- [analysis results profile](https://github.com/emo-bon/analysis-results-profile)
- [sequencing profile](https://github.com/emo-bon/sequencing-profile)


## Configuration

This semantic uplifting process is highly configurable and context-dependent, with data sources and settings specified through environment-aware configurations.

**Configuration File:** `sembench.yaml`   
Specifies the main configuration for the uplifting action, which includes:
- The template to be used for semantic uplifting
- The input data files to be transformed (typically tabular logsheets)
- The output triple files to be generated (in RDF-compatible formats)
- Template population settings, such as iteration rules and transformation parameters
- Additional environment variables that affect the behavior of the uplifting process

This file can be found either locally or within `./*-profile` repositories, making it easy to adapt the workflow to specific data domains or projects.

**Templates:**  
Semantic uplifting templates are typically stored in the `./templates` folder of `./*-profile` repositories. These templates define how to map raw data values into structured RDF triples, using domain-specific ontologies or models.

**Input Data:**  
Input data files (i.e. transformed logsheets) are usually located in the `/logsheets/transformed/` directory of the relevant `./observatory-*-crate` repositories. These files represent cleaned and pre-processed data, ready for semantic transformation.

