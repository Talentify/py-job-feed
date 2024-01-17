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

clean-up-staging-downloader: aws-ecr-auth-staging
	kubectl delete --ignore-not-found=true -f kubernetes/staging/deployment/feed-downloader.yaml --context=${STAGING_EKS_CLUSTER} -n ${NAMESPACE}

clean-up-staging-generator: aws-ecr-auth-staging
	kubectl delete --ignore-not-found=true -f kubernetes/staging/deployment/feed-generator-acme.yaml --context=${STAGING_EKS_CLUSTER} -n ${NAMESPACE}
	# Add more clients here

docker-build-staging-core: qemu
	docker buildx build --rm --push --tag ${STAGING_ECR_REPO}/py-job-feed-core:stage --platform=linux/arm64 -f docker/staging/JobFeedCore.stage.dockerfile .

docker-build-staging-downloader: qemu
	docker buildx build --rm --push --tag ${STAGING_ECR_REPO}/py-job-feed-downloader:stage --platform=linux/arm64 -f docker/staging/JobFeedDownloader.stage.dockerfile .

docker-build-staging-generator: qemu
	docker buildx build --rm --push --tag ${STAGING_ECR_REPO}/py-job-feed-generator:stage --platform=linux/arm64 -f docker/staging/JobFeedGenerator.stage.dockerfile .

staging-env-vars: aws-ecr-auth-staging
	kubectl apply -k kubernetes/staging/config --context=${STAGING_EKS_CLUSTER} -n ${NAMESPACE}
	kubectl apply -k kubernetes/staging/secrets --context=${STAGING_EKS_CLUSTER} -n ${NAMESPACE}

staging-deploy-downloader: clean-up-staging-downloader
	kubectl apply -f kubernetes/staging/deployment/feed-downloader.yaml --context=${STAGING_EKS_CLUSTER} -n ${NAMESPACE}

staging-deploy-generator: clean-up-staging-generator
	kubectl apply -f kubernetes/staging/deployment/feed-generator-acme.yaml --context=${STAGING_EKS_CLUSTER} -n ${NAMESPACE}
	# Add more clients here

staging-downloader: staging-env-vars docker-build-staging-downloader staging-deploy-downloader

staging-generator: staging-env-vars docker-build-staging-generator staging-deploy-generator

staging: staging-downloader staging-generator

staging-core: docker-build-staging-core staging
