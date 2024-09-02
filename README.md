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
```

Access the API:
```shell
kubectl get services stride-api
```

Access Grafana:
```shell
kubectl get services grafana
```

Set up Grafana:
- add postgresSQL data source using the postgres service name as the host.
- create dashboard with a panel using:
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

# Taking note of time used

2 hrs 35 minutes on `task1/scraper` branch completion.
challenge: needed to recreate an AWS account for the s3 bucket. 

2 hours on `task2/rewards_caculation` branch completion.
challenge: the math for `calculate_rewards` was really tricky.

1 hour 15 mins on `task3/rewards_calculation` branch completion.

59 minutes on `task4/api-service` on Saturday.

1 hour 18 minutes on `task5/claims` on Monday.
also fixes to api-service.

