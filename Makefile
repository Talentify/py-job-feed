NAMESPACE := ji-feed
AWS_PROFILE := default

qemu:
	docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

install-dependencies:
	mkdir -p .venv && pipenv install --ignore-pipfile --dev

# Staging

STAGING_EKS_CLUSTER := arn:aws:eks:us-east-1:124082513016:cluster/data-extraction-cluster-staging
STAGING_ECR_REPO := 124082513016.dkr.ecr.us-east-1.amazonaws.com

aws-ecr-auth-staging:
	clear
	aws ecr get-login-password --region us-east-1  --profile ${AWS_PROFILE} | docker login --username AWS --password-stdin ${STAGING_ECR_REPO}

clean-up-staging: aws-ecr-auth-staging
	kubectl delete --ignore-not-found=true -f kubernetes/staging/deployment/feed-downloader.yaml --context=${STAGING_EKS_CLUSTER} -n ${NAMESPACE}

docker-build-staging-core: qemu
	docker buildx build --rm --push --tag ${STAGING_ECR_REPO}/py-job-feed-core:stage --platform=linux/arm64 -f docker/staging/JobFeedCore.stage.dockerfile .

docker-build-staging: qemu
	docker buildx build --rm --push --tag ${STAGING_ECR_REPO}/py-job-feed-downloader:stage --platform=linux/arm64 -f docker/staging/JobFeedDownloader.stage.dockerfile .

staging-env-vars:
	kubectl apply -k kubernetes/staging/config --context=${STAGING_EKS_CLUSTER} -n ${NAMESPACE}

staging-deploy: clean-up-staging
	kubectl apply -f kubernetes/staging/deployment/feed-downloader.yaml --context=${STAGING_EKS_CLUSTER} -n ${NAMESPACE}

staging: docker-build-staging staging-deploy

staging-core: docker-build-staging-core staging

staging-full: staging-env-vars \
	staging-core