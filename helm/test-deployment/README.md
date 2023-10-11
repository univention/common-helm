# test-deployment

Test chart for the deployment template

- **Version**: 0.1.0
- **Type**: application
- **Homepage:** <https://git.knut.univention.de/univention/customers/dataport/upx/common-helm>

## Introduction

This is a Test chart. The intended use is to verify and document the intended
usage patterns of the "common" chart's deployment template.

## Requirements

| Repository | Name | Version |
|------------|------|---------|
|  | common | * |

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
			<td>image</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>probes.liveness</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>probes.readiness</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>service</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
	</tbody>
</table>

