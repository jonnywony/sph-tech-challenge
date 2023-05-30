tf-init:
	terraform init -backend-config=terraform/backend/${env}/tfvars

tf-plan:
	terraform plan -var-file=terraform/var/${env}/tfvars -out=terraform/${env}.tfplan

tf-apply-plan:
	terraform apply terraform/${env}.tfplan

tf-plan-destroy:
	terraform plan -var-file=terraform/var/${env}/tfvars -out=terraform/${env}.tfplan -destroy

tf-apply-destroy:
	terraform apply terraform/${env}.tfplan

docker-build-push:
	docker build -t ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG} .
	docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
