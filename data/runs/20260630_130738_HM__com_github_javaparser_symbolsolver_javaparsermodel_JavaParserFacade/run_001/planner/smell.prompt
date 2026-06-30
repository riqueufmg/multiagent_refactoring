 ## CONTEXT

Hub-like Modularization is a design smell that occurs  when an class has dependencies (**both incoming and outgoing**) with a large number of other classes.

The primary goal is to reduce the target class FAN-OUT by moving cohesive dependency-heavy responsibilities out of the target class, while preserving behavior and avoiding artificial indirection.

## TASK

Evaluate the input elements and create a plan in JSON format with the goal of removing (or reducing) Hub-like Modularization.

Strategy:
- Reduce the FAN-OUT of the class by grouping cohesive attributes and methods.
- MOVE and CREATE refactorings are only allowed at the same level as the entry or at a sub-level.
- Prefer moving private methods and dependency-heavy logic first. Public methods may be kept as delegating methods in the target class unless the plan also updates all required call sites.
- Test refactoring does not need to be included, as this will be done later.

## ALLOWED REFACTORINGS
A list of refactorings allowed in the refactoring plan is presented as following:
- ADD_OR_UPDATE_IMPORTS(file): Adds, removes, or updates imports required by the refactoring.
- CREATE_PACKAGE(pkgA.subpkg): Creates a new package under the current source root.
- EXTRACT_CLASS(pkgA.C1, pkgA.C2): Extracts part of class C1 into a new class C2.
- EXTRACT_INTERFACE(pkgA.C1, pkgA.I1): Extracts an interface I1 from class C1.
- INTRODUCE_FACADE(pkgA.C1, pkgA.Facade): Creates a facade to centralize access to related collaborators.
- MOVE_CLASS(pkgA.C1, pkgB.C1): Moves class C1 from package A to package B.
- MOVE_FIELD(pkgA.C1.field, pkgA.C2.field): Moves a field from class C1 to class C2.
- MOVE_METHOD(pkgA.C1.m(), pkgA.C2.m()): Moves a method from class C1 to class C2.
- REPLACE_DEPENDENCY(pkgA.C1, pkgA.C2): Replaces a direct dependency in C1 with a different dependency C2.
- UPDATE_CALL_SITES(pkgA.C1.m(), pkgA.C2.m()): Updates callers to use the new method or class location.

## INPUT
{input}

## OUTPUT

The expected output format and contraints for that output are presented below.

{
  "smell_type": "Hub-like Modularization",
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