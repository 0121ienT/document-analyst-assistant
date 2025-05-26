import asyncio
from azure.storage.blob.aio import BlobServiceClient, ContainerClient
from azure.storage.blob import CorsRule  # Add this import
from azure.core.exceptions import ResourceExistsError


async def init_azure_storage():
    connection_string = (
        "DefaultEndpointsProtocol=http;"
        "AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "BlobEndpoint=http://localhost:10000/devstoreaccount1"
    )

    async with BlobServiceClient.from_connection_string(
        connection_string
    ) as blob_service_client:
        container_client: ContainerClient = blob_service_client.get_container_client(
            "my-container"
        )

        try:
            # Create container if it doesn't exist
            await container_client.create_container(
                public_access="blob"  # This makes blobs publicly accessible
            )
            print("Container 'my-container' created successfully")
        except ResourceExistsError:
            print("Container 'my-container' already exists")

        # Set CORS rules using CorsRule class
        cors_rule = CorsRule(
            allowed_origins=["*"],
            allowed_methods=["GET", "POST", "PUT"],
            allowed_headers=["*"],
            exposed_headers=["ETag"],
            max_age_in_seconds=3600,
        )

        await blob_service_client.set_service_properties(cors=[cors_rule])
        print("CORS rules set successfully")


if __name__ == "__main__":
    asyncio.run(init_azure_storage())
