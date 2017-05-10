# Scalable cloud community
#### The only file needed in this repo to spawn a cluster with the application is the "createall.sh" bash script.


Create an account for google cloud engine (GCE). (console.cloud.google.com)

Enable Compute engine and Container engine API:

`API manager > Library > Compute Engine API`

`API manager > Library > Container Engine API`

Download a service account file in json format for your GCE project:

`API manager > Credentials > Create credentials > Service account key` (Use "Compute Engine default service account if you don't know what to pick")

You need to have docker installed. To install on debian or ubuntu, run: `sudo apt-get install docker-ce`.

Now run `createall.sh` and follow the instructions. A cluster with the application will be installed in a couple of minutes.
