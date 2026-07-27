# Designing a Star Schema for SACCO Contribution Tracking

A star schema for SACCOs typically includes:

- FactContributions: contributor_id, amount, contribution_date_id, product_id, branch_id
- DimContributor: contributor details
- DimDate: standard date dimension
- DimProduct: savings / loan product variants
- DimBranch: location and region

Design notes:

- Avoid wide facts; keep fact table narrow and use surrogate keys
- Use slowly changing dimensions for contributor status
- Consider nearline/OLAP aggregation tables for monthly reporting
