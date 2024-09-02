# How to run 

Build and push Docker images:
```shell
docker build -f docker/Dockerfile.api -t stride-mac-registry/stride-api:latest .
docker build -f docker/Dockerfile.reward_calculator -t stride-mac-registry/stride-reward-calculator:latest .
docker build -f docker/Dockerfile.scraper -t stride-mac-registry/stride-scraper:latest .

# had to re-tag all images:
docker tag stride-mac-registry/stride-api:latest theghostmac/stride-api:latest
docker tag stride-mac-registry/stride-reward-calculator:latest theghostmac/stride-reward-calculator:latest
docker tag stride-mac-registry/stride-scraper:latest theghostmac/stride-scraper:latest

docker push theghostmac/stride-api:latest
docker push theghostmac/stride-reward-calculator:latest
docker push theghostmac/stride-scraper:latest
```

Apply kubernetes manifests:
```shell
kubectl apply -f kubernetes/aws-credentials.yaml
kubectl apply -f kubernetes/database-url.yaml
kubectl apply -f kubernetes/postgres-secrets.yaml
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/api-deployment.yaml
kubectl apply -f kubernetes/scraper-job.yaml
kubectl apply -f kubernetes/reward-calculator-job.yaml
kubectl apply -f kubernetes/grafana-deployment.yaml
```

Verify all pods are running:
```shell
kubectl get pods
NAME                                   READY   STATUS              RESTARTS   AGE
grafana-d97c55c95-tr8xm                1/1     Running             0          46m
postgres-c4769ff99-wbz9x               1/1     Running             0          65s
stride-api-554fbf5f7f-46pt7            1/1     Running             0          60s
stride-api-554fbf5f7f-bwnzg            1/1     Running             0          60s
stride-api-554fbf5f7f-gmjd2            1/1     Running             0          60s
```

Access the API:
```shell
kubectl get services stride-api
NAME         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
stride-api   LoadBalancer   10.99.147.144   <pending>     80:30787/TCP   2m29s
```

Access Grafana:
```shell
kubectl get services grafana
NAME      TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
grafana   LoadBalancer   10.98.113.109   <pending>     80:31876/TCP   48m
```

Set up Grafana:
- access Grafana:
  - external-ip pending, so port-forwarding: `kubectl port-forward service/grafana 3000:80`
  - open browser at http://localhost:3000
  - login with username: admin, password: admin. change password after.
- add postgresSQL data source using the postgres service name as the host.
  - click Gear icon to open Config menu
  - select "Data Sources"
  - Add data source
  - Choose "PostgreSQL"
  - fill the info:
    - name: Stride Airdrop DB
    - host: postgres:5432
    - database: stride_airdrop
    - user: ghostmac
    - password: gh05tm4c
    - ssl mode: disable
  - click save and test.
  - create new dashboard: click +, select Dashboard, and Add new panel.
  - select PostgreSQL data source, switch to Code mode, add the SQL query below:
```sql
SELECT
  date_trunc('day', date) AS time,
  SUM(amount) OVER (ORDER BY date_trunc('day', date)) AS total_claimed
FROM
  claims
GROUP BY
  time
ORDER BY
  time
```
  - in panel options on right, set the title to "Total Rewards Claimed Over Time", under visualization, choose Time Series.
  - click "Apply"
- Save the dashboard: click Save icon. Name it "Stride Airdrop Analytics", click Save.
- add more panels for different metrics.
- setup auto-refresh, 1 hour for hourly updates.

Connecting directly:
```shell
kubectl run -it --rm --image=postgres:15 --restart=Never postgres-client -- psql -h postgres -U ghostmac -d stride_airdrop
```

Test the scraper and reward calculator jobs:
```shell
kubectl create job --from=cronjob/stride-scraper stride-scraper-test
kubectl create job --from=cronjob/stride-reward-calculator stride-reward-calculator-test
```

Monitor logs:
```shell
kubectl logs job/stride-scraper-test
kubectl logs job/stride-reward-calculator-test
```

Troubleshooting PostgreSQL data source for Grafana:
```shell
kubectl logs $(kubectl get pods -l app=postgres -o jsonpath="{.items[0].metadata.name}")
```

# Taking note of time used

2 hrs 35 minutes on `task1/scraper` branch completion.
challenge: needed to recreate an AWS account for the s3 bucket. 

2 hours on `task2/rewards_caculation` branch completion.
challenge: the math for `calculate_rewards` was really tricky.

1 hour 15 mins on `task3/rewards_calculation` branch completion.

59 minutes on `task4/api-service` on Saturday.

1 hour 18 minutes on `task5/claims` on Monday.
also fixes to api-service.

1 hour 3 minutes on `task6/dashboard` on Monday.
updates to manifests, deploying grafana, and setting up all services on Docker and K8s.