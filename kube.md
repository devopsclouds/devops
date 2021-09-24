completions: 2
backoffLimit 


how to delete jobs in kubernetes after completion using feature gate
open  the kube-apiserver and kube controller yaml files under /etc/kubernetes/manifests
add this line - --feature-gates=TTLAfterFinished=true
open the job yaml file ttlSecondsAfterFinished add this job spec configuration ---- it means whenever the job is completed after 20 seconds the job will terminated


