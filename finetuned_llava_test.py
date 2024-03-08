import replicate

output = replicate.run(
    "yorickvp/llava-v1.6-34b:741ecfbfb261e6c1adf3ad896c9066ca98346996dc4045c5bc944a79d430f174",
    input={
        "image": "bqYanWd6EEkVS6tO-4.jpg",
        "top_p": 1,
        "prompt": "What's unusable about this image?",
        "max_tokens": 1024,
        "temperature": 0.2
    })
print(output)
