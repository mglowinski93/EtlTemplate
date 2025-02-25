# OutputData domain data model type.

**Status:** Done.

## Context

There was a discussion about what type we should use for the final ETL OutputData domain model. Two options were discussed:
- pandas.DataFrame
- @dataclass

## Decision

In-build python @dataclass was chosen as a type of ETL OutputData.

## Consequences

At the last stage of the ETL (Load), we don't need to validate the data again (validation is done before). @dataclass is also much easier to serialize. 

## Alternatives

The alternative is to consistently use pandas.DataFrame through the whole ETL, including OutputData. This approach is seemingly correct, but once Data is fully processed by ETL, we do not benefit anymore from using a DataFrame. 

## Decision date

25.02.2025
