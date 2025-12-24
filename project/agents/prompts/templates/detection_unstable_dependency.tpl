# Task

You are a software engineering expert in software refactoring.

Your task is to detect the smell: Unstable Dependency.

Definition:
This smell arises when a component depends on other less stable components. Stable Dependencies Principle states that the dependencies between packages should be in the direction of the stability of packages. Hence, a package should only depend on packages that are more stable than itself. An unstable dependency architecture smell occurs when this principle is not followed.

# Constraints

- Perform the analysis at the **package level** and evaluate each package individually.
- Do not rely on fixed metric thresholds; use contextual judgment based on the provided data.
- Give the answer exactly in the structure defined in the **#Successful Output** section.
- Do not include comments, explanations, or text outside the defined output format.
- All fields in the **#Successful Output** are mandatory.
- Only perform the analysis if the provided data are sufficient; otherwise, follow the **#Unsuccessful Output** format.

# Input

The following metrics and dependencies are available at package level:

```json
{INPUT_DATA}
```

# Successful Output

Provide the output in this structure:

```json
{
  "smell": "Unstable Dependency",
  "detections": [
    {
      "package": "[package_name]",
      "detection": false,
      "justification": "[Reasons for the detection result, citing the elements that justify the decision]"
    },
    {
      "package": "[package_name]",
      "detection": true,
      "justification": "[Reasons for the detection result, citing the elements that justify the decision]"
    },
    {
      "package": "[package_name]",
      "detection": false,
      "justification": "[Reasons for the detection result, citing the elements that justify the decision]"
    }
  ]
}
```

# Unsucessfull Output

If the available data are insufficient to detect this smell, return:

```json
{
    "message": "It is impossible to detect {SMELL_NAME} with the available data."
}
```