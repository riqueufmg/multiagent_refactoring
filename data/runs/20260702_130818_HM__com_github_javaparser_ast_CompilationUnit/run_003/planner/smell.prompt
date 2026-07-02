## CONTEXT

Hub-like Modularization is a design smell that occurs when an class has dependencies (both incoming and outgoing) with a large number of other classes.

One way to remove Hub-like Modularization is to reduce the target class FAN-OUT by moving cohesive dependency-heavy responsibilities out of the target class, while preserving behavior.

## TASK

The goal is to reduce the target class's output coupling (fan-out) by 2 to 4 dependencies.

Based on an analysis of the target class's code and external calls, follow this reasoning:
- For each class coupled to the target class, create a group containing all methods that utilize it.
- An external dependency class should not be in two groups.
- Then, identify 2 to 4 groups of highly cohesive methods. Preferably for smaller groups, that is, with fewer methods.
- In each block of the plan, move the methods from the groups into a new class.
- You cannot move methods from only a single group into a new class; doing so would increase the fan-out, and reducing the fan-out by just one would not result in a genuine reduction of the metric.
- The plan must consist of 1 to 3 blocks, each aimed at reducing the dependency count by 2 to 4.

Observations:
- When a new class is introduced, the target class may gain a dependency on that new class. Therefore, a useful extraction should remove at least two existing direct dependencies from the target class for each new dependency introduced.
- Do not claim that a dependency is removed if it remains in the target class through imports, fields, method parameters, return types, local variables, object creation, static calls, inheritance clauses, or public method signatures.

## ALLOWED REFACTORINGS
A list of refactorings allowed in the refactoring plan is presented as following:
- ADD_OR_UPDATE_IMPORTS(file): Adds, removes, or updates imports required by the refactoring.
- CREATE_PACKAGE(pkgA.subpkg): Creates a new package under the current source root.
- EXTRACT_CLASS(pkgA.C1, pkgA.C2): Extracts part of class C1 into a new class C2.
- EXTRACT_INTERFACE(pkgA.C1, pkgA.I1): Extracts an interface I1 from class C1.
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

## CONTRAINTS
- Reference only packages, classes, methods, and fields present in the input.
- Each block must be small and independently compilable.
- New classes must be placed in the same package as the target class unless the input clearly justifies otherwise.