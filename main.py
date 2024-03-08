import replicate

training = replicate.trainings.create(
    version=
    "yorickvp/llava-13b:a0fdc44e4f2e1f20f2bb4e27846899953ac8e66c5886c5878fa1d6b73ce009e5",
    input={
        "train_data":
        "https://replicate.delivery/pbxt/KUgOc1jTxpa1y1Dc3EDMm4TsRSv84AURqDlQaIU9RChc1Nwm/data.zip",
        "num_train_epochs": "16",
    },
    destination=
    "ravi-teja-konda/llava_fine_tune_indian_desserts_with_nutritional_info")

while (1):
  training.reload()
  print(training.status)
  print("\n".join(training.logs.split("\n")[-10:]))
