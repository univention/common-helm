# test-helm-values

Test chart for checks related to Helm's value handling

- **Version**: 0.1.0
- **Type**: application
-

## Introduction

This is a test chart which renders all available values.

Its purpose is to be used when trying to understand special behavior in the way
how Helm is merging values from various sources (defaults, value files, CLI).

Examples:

    # Default values
    helm template .

    # Setting a value to "null" makes the key disappear suddenly
    helm template . --set client.auth.password=null

## Requirements

| Repository | Name | Version |
|------------|------|---------|
|  | nubus-common | * |

## Values

<table>
	<thead>
		<th>Key</th>
		<th>Type</th>
		<th>Default</th>
		<th>Description</th>
	</thead>
	<tbody>
		<tr>
			<td>client.auth.existingSecret.keyMapping.password</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>client.auth.existingSecret.name</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>client.auth.password</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
	</tbody>
</table>

