# Deployment

`deploy.sh` builds the image with Cloud Build and deploys the Cloud Run
service in the dev project (`harbour-support-dev`, `europe-west2`), private
ingress behind the existing load balancer and IAP. It is the only deployment
script so far; it creates nothing besides the image and the revision.

Owned resources and their state are recorded in each ticket's Evidence.
