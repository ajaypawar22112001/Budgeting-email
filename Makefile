# Variables
APP_NAME=budgeting-app
GCP_PROJECT_ID=learning-gcp-445308
REGION=us-central1
IMAGE=gcr.io/$(GCP_PROJECT_ID)/$(APP_NAME)

# Run locally
run:
	docker-compose up --build

# Stop local containers
stop:
	docker-compose down

# Build & push Docker image to GCR
build-push:
	docker build -t $(IMAGE) .
	docker push $(IMAGE)

# Deploy to Google Cloud Run
deploy:
	gcloud run deploy $(APP_NAME) --image $(IMAGE) --platform managed --region $(REGION) --allow-unauthenticated
