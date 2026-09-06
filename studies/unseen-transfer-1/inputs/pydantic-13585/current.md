The nested schemas explain these six outcomes. A local reproduction with Pydantic 2.13.4 and pydantic-core 2.46.4 matched all six.

For input `0`, both before-validator arrangements produce `1` before the relevant `lt=1` check, so both fail. With the wrap and after validators, placing `Field(lt=1)` after the validator checks the returned `1` and fails. Placing the field constraint first lets it accept `0`, after which the validator returns `1` without another constraint check.

Pydantic can attach a numeric constraint directly to an integer schema. If the existing schema is a function wrapper, it can instead apply the constraint through an outer after-validation step. The [versioned implementation](https://github.com/pydantic/pydantic/blob/v2.13.4/pydantic/_internal/_known_annotated_metadata.py) and `TypeAdapter(...).core_schema` let you inspect the structure for a particular annotation.

That explains these examples, but does not establish a stable global ordering rule for all mixed metadata or constraints. The maintainer's accepted reply warns that annotation interactions are inconsistent.
