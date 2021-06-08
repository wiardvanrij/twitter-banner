# Very basic how-to

> :warning: **This is intended as hackathon/hobby material**: I have made this in a few hours on a friday. It is more intended for inspriration rather than actual 24/7/365 usage. Even though it works. This is merely a explanation on _how_ it works, rather than a full-blown mature project. So many things should be different/better. I know. That said: enjoy!


Make sure to have longhorn on your cluster or remove the PVC part in `kube-prometheus/manifests/prometheus-prometheus.yaml` 


Apply setup (like crds)

`kubectl apply -f kube-prometheus/manifests/setup` 


Create your own dashboards by checking the `dashboard` folder.
Each entry has to be tweaked. 

- Change the `name.json` towards an unique entry
- Change the name of the configmap to an unique entry
- Change the query so that the dashboard equals the correct twitter user

```"expr": "twitter_followers{job=\"json_probe\",instance!=\"localhost:7979\",username=\"RijWiard\"}",```

In the above, it would show a dashboard for the Twitter user `RijWiard`

Next check the `kube-prometheus/manifests/grafana-deployment.yaml` and make sure each dashboard you have created is included as configmap and mount.


Apply the rest of prometheus/grafana

`kubectl apply -f kube-prometheus/manifests`

Apply grafana image renderer

`kubectl apply -f grafana-image`

Apply the dashboards 

`kubectl apply -f dashboards/dash.yaml`

Get your Twitter API keys and edit `json_exporter/config.yaml` in fill in the bearer token.

`kubectl apply -f json_exporter` 


The `scrape/scrapeconfig.yaml` should be applyed as a secret like:

```kubectl create secret generic additional-configs -n monitoring --from-file=scrapeconfig.yaml --dry-run=client -o yaml``` 

Either remove the dry-run or use the output to apply this manually

If everything is fine, you should be able to login to grafana (port forward to grafana on port 3000)
Login with admin/admin. 

Check if all your dashboards are correct. Open a dashboard and click on the dropdown of the panel. Click 'Share' -> click "Direct link rendered image". 

This is the URL you should save as input for the docker Image to run the `job.yaml` with. Do remove the `&from=xxx&to=xxx` part of the URL. *We don't need this.*

Now in `job.yaml` fill in the environment variables. The tokens should be from the Twitter API. The image_url is the url from above. Remember to remove the `from` and `to` part. Since we have auth on Grafana, we have to add a prefix to the url with so it looks like: `http://admin:admin@grafana:3000` 

If you ever run this publicly, refactor this with an API key.

Apply the job. `kubectl apply -f job.yaml`

Or build your own image. The source of the image is in `twitter-python` 