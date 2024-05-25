# API Requester

## Requirements
- 2 CPUs or more
- 2GB of free memory
- 20GB of free disk space
- Internet connection
- Container or virtual machine manager, such as: Docker, QEMU, Hyperkit, Hyper-V, KVM, Parallels, Podman, VirtualBox, or VMware Fusion/Workstation
- Minikube: Installed via https://minikube.sigs.k8s.io/docs/start/ depending on your OS and Arch
- Helm 3 - https://helm.sh/docs/intro/install/

## What it is and how it works

![alt text](https://github.com/trevorvoncannon/angi/blob/main/res/angi.jpg?raw=true)

API Requester is a simple python code that queries a public API endpoint and stores the response data in JSON format in the /api-data directory. This directory is mounted to a persistent volume `api-data-pv` in your Minikube Kubernetes cluster. The API Requester code runs in a k8s pod that is controlled by a k8s Cronjob, which runs on a configured schedule.

As the API Requester job is relatively quick, the container running the code generally does not stay in a Running state for too long. To view the data on the persistent volume, I have provided a `pv-inspector` pod that also mounts the volume and allows you to view the JSON files created by the jobs.

## How to deploy the API Requester
The requester is packaged in a Helm chart and is therefore deployed using the helm cli, so make sure you have Helm 3 installed. 

The Helm chart is located at https://github.com/trevorvoncannon/angi/tree/main/charts/api-requester - make sure to review the README.md for configuration options in the values file 

:information_source: **This is how you can configure the requester's schedule**

### Helm Install Command

:warning: **Run this from the charts/api-requester directory**
```bash
helm install -f values.yaml api-requester . --namespace angi --create-namespace
```
After running this command, you should see this output:

```
NAME: api-requester
LAST DEPLOYED: <date>
NAMESPACE: angi
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

This means your release was successfully deployed!

### Validation

To confirm that all of the resources are running, you can run the following kubectl command:

```bash
kubectl get all -n angi
```

Example output:

```
NAME                                   READY   STATUS      RESTARTS   AGE
pod/api-requester-job-28611158-877xt   0/1     Completed   0          2m59s
pod/api-requester-job-28611159-m9kr5   0/1     Completed   0          119s
pod/api-requester-job-28611160-cj5kw   0/1     Completed   0          59s
pod/pvc-inspector                      1/1     Running     0          97s

NAME                              SCHEDULE    SUSPEND   ACTIVE   LAST SCHEDULE   AGE
cronjob.batch/api-requester-job   * * * * *   False     0        59s             5m21s

NAME                                   COMPLETIONS   DURATION   AGE
job.batch/api-requester-job-28611158   1/1           9s         2m59s
job.batch/api-requester-job-28611159   1/1           9s         119s
job.batch/api-requester-job-28611160   1/1           17s        59s
```
#### Data Validation

Remember the `pv-inspector` pod I mentioned earlier? This is where it comes into play. Run the following command to exec into the inspector pod and confirm data is being extracted from the API and stored on the volume.

```bash
kubectl exec -it pvc-inspector -n angi -- ls -l api-data
```

Example output:

```
$ kubectl exec -it pvc-inspector -n angi -- ls -l api-data
total 972
-rw-r--r--    1 root     root         33550 May 25 19:57 api-data-20240525-195708.json
-rw-r--r--    1 root     root         33550 May 25 19:58 api-data-20240525-195808.json
-rw-r--r--    1 root     root         33550 May 25 19:59 api-data-20240525-195908.json
-rw-r--r--    1 root     root         33550 May 25 20:00 api-data-20240525-200016.json
-rw-r--r--    1 root     root         33550 May 25 20:01 api-data-20240525-200109.json
-rw-r--r--    1 root     root         33550 May 25 20:02 api-data-20240525-200210.json
-rw-r--r--    1 root     root         33550 May 25 20:03 api-data-20240525-200309.json
-rw-r--r--    1 root     root         33550 May 25 20:04 api-data-20240525-200409.json
```
ℹ️ **Notice that the files created by the query are timestamped with the date and time (YYYYMMDD-HHMMSS)**

🥳 That's it! All there is to it!

### Teardown/Removal

Simply run the helm uninstall command to remove the release from your environment.

```bash
helm uninstall api-requester -n angi
```
