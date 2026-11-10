# Berik Satybaldy — 240107019 — Group B — Drill 4

```text
Impact: Users could not reach the drill service; the check reported "the service does NOT answer", and both Pods were stuck in CreateContainerConfigError.
Detection: kubectl -n drill describe pod drill-6db786866f-dzzxm showed "Error: couldn't find key PORT in ConfigMap drill/drill-config".
Root cause: The ConfigMap defined lowercase port, but the Deployment referenced uppercase PORT; the configuration keys did not match and nothing checked the reference.
Fix: Renamed the ConfigMap key from port to PORT, keeping the value 8080, and restarted deployment/drill; bash drill/start.sh check then returned ok.
Prevention: Validate that every configMapKeyRef matches an existing, case-sensitive ConfigMap key, and require a successful rollout and service health check in CI.
```
