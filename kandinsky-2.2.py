output = replicate.run(
    "ai-forever/kandinsky-2.2:ad9d7879fbffa2874e1d909d1d37d9bc682889cc65b31f7bb00d2362619f194a",
    input={
        "width": 1024,
        "height": 1024,
        "prompt": "A moss covered astronaut with a black background",
        "num_outputs": 1,
        "output_format": "webp",
        "num_inference_steps": 75,
        "num_inference_steps_prior": 25
    }
)

# To access the file URL:
print(output[0].url())
#=> "http://example.com"

# To write the file to disk:
with open("my-image.png", "wb") as file:
    file.write(output[0].read())