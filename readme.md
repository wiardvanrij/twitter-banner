# Very basic how-to

> :warning: **This is intended as hackathon/hobby material**: I have made this in a few hours on a friday. It is more intended for inspriration rather than actual 24/7/365 usage. Even though it works. This is merely a explanation on _how_ it works, rather than a full-blown mature project. So many things should be different/better. I know. That said: enjoy!


Make sure to have longhorn on your cluster or remove the PVC part in `kube-prometheus/manifests/prometheus-prometheus.yaml` 


Apply setup (like crds)

`kubectl apply -f kube-prometheus/manifests/setup` 


Create your own dashboards by checking the `dashboard` folder.
Each entry has to be tweaked. If you only want to track one dashboard, make sure you remove all other entries. For each one you want to keep:

- Change the `name.json` to a unique entry
- Change the name of the configmap to a unique entry
- Change the query so that the dashboard looks up the correct Twitter user. The query is *case sensitive* so make sure you set it as the Twitter username is on the site.

```"expr": "twitter_followers{job=\"json_probe\",instance!=\"localhost:7979\",username=\"RijWiard\"}",```

In the above, it would show a dashboard for the Twitter user `RijWiard`

Next check the `kube-prometheus/manifests/grafana-deployment.yaml` and make sure each dashboard you have created is included as configmap and mount.


Apply the rest of prometheus/grafana

`kubectl apply -f kube-prometheus/manifests`

Apply grafana image renderer

`kubectl apply -f grafana-image`

Apply the dashboards 

`kubectl apply -f dashboards/dash.yaml`

Get your Twitter API keys and edit `json_exporter/config.yaml` to fill in the bearer token you have acquired from the Twitter API configuration for your application. Then, apply the json_exporter:

`kubectl apply -f json_exporter` 

Next, we need to configure the scrape of the data. Edit `scrape/scrapeconfig.yaml` to include the username(s) of the Twitter accounts you defined in the Grafana deployment above. Again, these are case sensitive.

The `scrape/scrapeconfig.yaml` should be applyed as a secret like:

```kubectl create secret generic additional-configs -n monitoring --from-file=scrapeconfig.yaml --dry-run=client -o yaml``` 

To actually get it on your cluster, either remove the dry-run or use the output to apply this manually.

If everything is fine, you should be able to login to Grafana (port forward to grafana on port 3000):

```
$ kubectl get pods -n monitoring | grep grafana
grafana-78f7774c99-mcmw5                    1/1     Running   0          13m
$ kubectl port-forward -n monitoring grafana-78f7774c99-mcmw5 3000:3000
```
Navigate to `localhost:3000` in your browser.

Login with admin/admin. When prompted, do not change the password. 

Check if all your dashboards are correct. Open a dashboard and click on the dropdown of the panel. Click 'Share' -> click "Direct link rendered image". 

This is the URL you should save as input for the Docker Image to run the `job.yaml` with. Do remove the `&from=xxx&to=xxx` part of the URL. *We don't need this.*

Make sure it has the proper dimensions for Twitter, which is: `&width=1500&height=500` Adjust this in the params.

Now in `job.yaml` fill in the environment variables. The tokens should be from the Twitter API. The image_url is the url from above. Remember to remove the `&from` and `&to` part. Since we have auth on Grafana, we have to add a prefix to the url with so it looks like: `http://admin:admin@grafana:3000` 

If you ever run this publicly, refactor this with an API key.

Apply the job. `kubectl apply -f job.yaml`

Note that the moment the job runs successfully, your account banner will be updated. There is no warning or confirmation.

Or build your own image. The source of the image is in `twitter-python` 
