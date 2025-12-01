from huggingface_hub import HfApi, upload_folder

api = HfApi()

upload_folder(
    folder_path="models/summarizer",
    repo_id="aliabbi/flan-t5-samsum-lora",
    repo_type="model"
)

print("Upload completed successfully!")