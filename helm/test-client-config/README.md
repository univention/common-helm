# test-client-config

Test chart for the client configuration pattern

- **Version**: 0.0.1
- **Type**: application
-

## Introduction

This is a Test chart. The intended use is to verify and document the intended
usage patterns of the client configuration.

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
			<td>global.memcached.auth.username</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.smtp.auth.username</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>memcached.auth.password</td>
			<td>string</td>
			<td><pre lang="json">
"stub-values-password"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>memcached.auth.username</td>
			<td>string</td>
			<td><pre lang="json">
"stub-values-username"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>smtp.auth.existingSecret.keyMapping.password</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>smtp.auth.existingSecret.name</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>smtp.auth.password</td>
			<td>string</td>
			<td><pre lang="json">
"stub-values-password"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>smtp.auth.username</td>
			<td>string</td>
			<td><pre lang="json">
"stub-values-username"
</pre>
</td>
			<td></td>
		</tr>
	</tbody>
</table>

