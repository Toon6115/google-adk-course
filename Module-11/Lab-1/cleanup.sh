# Delete the Cloud Run service
gcloud run services delete weather-agent-service \
  --region=$GOOGLE_CLOUD_LOCATION \
  --quiet

# Delete container images from Artifact Registry
gcloud artifacts docker images list \
  $GOOGLE_CLOUD_LOCATION-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/cloud-run-source-deploy \
  --format="value(IMAGE)" | while read image; do
    gcloud artifacts docker images delete "$image" --quiet --delete-tags 2>/dev/null
done

# (Optional) Delete the Artifact Registry repository
 gcloud artifacts repositories delete cloud-run-source-deploy \
   --location=$GOOGLE_CLOUD_LOCATION \
   --quiet

# Verify cleanup
gcloud run services list --region=$GOOGLE_CLOUD_LOCATION
