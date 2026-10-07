## CONTEXT

Insufficient Modularization is a design smell that occurs when a class exists that has not been completely decomposed, and a further decomposition could reduce its size, implementation complexity, or both.

The factors that characterize Insufficient Modularization are considered in the following priority order:
- Too many public methods (poorly cohesive API).
- Too many general methods.
- Overly complex methods.

## TASK

Evaluate the input elements and create a plan in JSON format with the goal of removing (or reducing) Insufficient Modularization.

Strategy:
- Reduce the size and complexity of the class by grouping cohesive attributes and methods.
- MOVE and CREATE refactorings are only allowed at the same level as the entry or at a sub-level.
- When the smell is caused by too many public methods, prefer plans that move a cohesive group of public and private methods out of the target class.
- Test refactoring does not need to be included, as this will be done later.

## ALLOWED REFACTORINGS
A list of refactorings allowed in the refactoring plan is presented as following:
- ADD_OR_UPDATE_IMPORTS
- CREATE_PACKAGE
- DEPENDENCY_INVERSION
- EXTRACT_CLASS
- EXTRACT_INTERFACE
- INTRODUCE_FACADE
- MOVE_CLASS
- MOVE_FIELD
- MOVE_METHOD
- REPLACE_DEPENDENCY
- UPDATE_CALL_SITES

## INPUT
{input}

## OUTPUT

The expected output format and contraints for that output are presented below.

{
  "smell_type": "Insufficient Modularization",
  "target_level": "class",
  "target": "<class FQN from input>",
  "blocks": [
    {
      "id": 1,
      "goal": "...",
      "files": ["..."],
      "ops": [
        {
          "op": "<allowed op>",
          "inputs": ["..."],
          "outputs": ["..."],
          "details": "...",
          "risk": "low|medium|high"
        }
      ]
    }
  ]
}

Contraints:
- Reference only packages, classes, methods, and fields present in the input.
- Each block must be small and independently compilable.
- New classes must be placed in the same package as the target class unless the input clearly justifies otherwise.