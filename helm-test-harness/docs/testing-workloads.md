# Testing workloads


## Looking up containers or attributes within containers

Many workloads have a template of a _Pod_ embedded. Some have an additional
template embedded, like _CronJob_ wich has a _Job_ template embedded which
itself has a template of a _Pod_.

This leads to different levels of nesting when trying to find a container or
anything in a container via _JSONPath_. Using the prefix `..` typically allows
to cover both bases:

```python
class Example:
    path_main_container = "..spec.template.spec.containers[?@.name=='main']"
    path_volume_secret_ldap = "..spec.template.spec.volumes[?@.name=='secret-ldap']"
```
