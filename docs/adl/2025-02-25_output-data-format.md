#  Output data format

**Status:** _accepted_.

## Context

* There is a need to pass parsed input data for further processing.

## Decision

We decided to use 
[pandera DataFrameModel](https://pandera.readthedocs.io/en/latest/dataframe_models.html)
to define input data structure and validate it before further processing.

This approach allows to easily cast input data to
[pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html),
which is widely used in the data processing and analysis.

## Consequences

Data processing and data analysis are depended on a specific framework.

## Alternatives

The Alternative would be to use
[dataclasses](https://docs.python.org/3/library/dataclasses.html),
but it's not effective for large amounts of data.

## Decision date

> 2025-02-25
