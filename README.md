# API Requester

## Requirements
- 2 CPUs or more
- 2GB of free memory
- 20GB of free disk space
- Internet connection
- Container or virtual machine manager, such as: Docker, QEMU, Hyperkit, Hyper-V, KVM, Parallels, Podman, VirtualBox, or VMware Fusion/Workstation
- Minikube: Installed via https://minikube.sigs.k8s.io/docs/start/ depending on your OS and Arch

## What it is and how it works

![alt text](https://github.com/trevorvoncannon/angi/blob/main/res/angi.jpg?raw=true)

API Requester is a simple python code that queries a public API endpoint and stores the response data in JSON format in the /api-data directory. This directory is mounted to a persistent volume `api-data-pv` in your Minikube Kubernetes cluster. The API Requester code runs in a k8s pod that is controlled by a k8s Cronjob, which runs on a configured schedule.

As the API Requester job is relatively quick, the container running the code generally does not stay in a Running state for too long. To view the data on the persistent volume, I have provided a `pv-inspector` pod that also mounts the volume and allows you to view the JSON files created by the jobs.

