## CONTEXT

Hub-like Modularization (HM) is a class-level design smell that occurs when **both** the target class's Fan-In and Fan-Out are high. If either metric is medium or low, HM is absent.

This refactoring targets **Fan-Out only**. Reducing the number of distinct outgoing class dependencies sufficiently to bring Fan-Out below the high category can remove HM even when Fan-In remains high. Do not optimize Fan-In as a substitute for reducing Fan-Out.

## TASK

The goal is to reduce the target class's Fan-Out while preserving its behavior, responsibilities' cohesion, and public compatibility. Aim to remove 2 to 4 net outgoing dependencies when feasible; the actual reduction needed to eliminate HM depends on the target's metrics and the detector's thresholds, if provided in the input.

Based on the target class's code and its outgoing dependencies, follow this reasoning:
- Identify coherent responsibilities implemented by methods and fields of the target class. Group elements by their behavior, shared state, and collaboration, **not** simply because they use the same dependency.
- For each candidate responsibility, identify the distinct external classes it references and check whether those classes are also referenced elsewhere in the target class.
- Favor changes that eliminate **all direct references** from the target class to several outgoing dependency classes. A dependency is not removed from Fan-Out if any direct reference to it remains in the target class.
- Consider the effects of the target's fields, constructors, methods, inheritance, annotations, parameter and return types, and required compatibility wrappers. Do not assume that moving a method or deleting an import removes a dependency.
- Select the most suitable combination of allowed refactorings. Extract Class is one possible strategy, not a mandatory one; moving cohesive methods or fields to an appropriate existing class may be better. Avoid unnecessary new classes, forwarding layers, circular dependencies, and dependency replacements that merely disguise coupling.
- Account for **new outgoing dependencies** introduced into the target class (such as a newly extracted helper). Estimate the **net Fan-Out change** as the number of distinct outgoing dependencies genuinely eliminated minus the number of new distinct outgoing dependencies introduced.
- Prefer a small, cohesive change with a credible positive net reduction over a larger refactoring that only redistributes code. Do not sacrifice behavior or design quality to force a numeric reduction.
- Before producing the plan, verify for each proposed removed dependency why the target class will no longer reference it. Identify dependencies that must remain, and do not count them toward the expected reduction.
- The plan must consist of 1 to 3 small blocks, each independently compilable. A block may prepare a transformation without immediately reducing Fan-Out, provided the overall plan has a credible net reduction.

Observations:
- Moving methods alone does not guarantee a Fan-Out reduction. The target class must stop referring to the outgoing dependency classes being counted as removed.
- If the target class gains one new helper dependency, removing only one existing dependency gives **zero net reduction**. Removing two existing dependencies gives a net reduction of one, assuming no other changes.
- A dependency is still present when the target class references it through fields, method signatures, local variables, object creation, static calls, annotations, inheritance, or other direct type usages. Imports alone are not evidence of a dependency, and removing an import alone does not establish a Fan-Out reduction.
- Preserve necessary public APIs. If compatibility requirements leave the old dependencies in public signatures, account for them rather than claiming they were removed.
- If the input does not provide enough evidence for a reliable reduction, do not invent methods, fields, or dependencies or claim that HM will be removed. Return an empty `blocks` array rather than an unjustified transformation.

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

The expected output format and constraints for that output are presented below.

```json
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
```

For each planned block, use `goal` and `details` to explain the cohesive responsibility being redistributed, the **specific outgoing dependency classes expected to disappear from the target**, any newly introduced target dependencies, and why the expected **net Fan-Out change** is positive. Make these claims only when supported by the input. Do not add new JSON fields.

## CONSTRAINTS

- Reference only packages, classes, methods, and fields present in the input, except for names of new classes or packages explicitly created by the plan.
- Each block must be small and independently compilable.
- New classes must be placed in the same package as the target class unless the input clearly justifies otherwise.
- The target class must retain its original fully qualified name (FQN) throughout the refactoring; MOVE_CLASS may be applied to other classes, but not to the target class.
- Preserve behavior and required public interfaces. Do not change tests merely to conceal regressions.
- Do not propose a package reorganization as the primary strategy for reducing class-level HM.
- Never assert that HM has been removed solely from a predicted Fan-Out change; the actual result must be measured after the refactoring.
