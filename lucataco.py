output = replicate.run(
    "lucataco/ssd-1b:b19e3639452c59ce8295b82aba70a231404cb062f2eb580ea894b31e8ce5bbb6",
    input={
        "seed": 36446545872,
        "width": 768,
        "height": 768,
        "prompt": "with smoke, half ice and half fire and ultra realistic in detail.wolf, typography, dark fantasy, wildlife photography, vibrant, cinematic and on a black background",
        "scheduler": "K_EULER",
        "lora_scale": 0.6,
        "num_outputs": 1,
        "batched_prompt": False,
        "guidance_scale": 9,
        "apply_watermark": True,
        "negative_prompt": "scary, cartoon, painting",
        "prompt_strength": 0.8,
        "num_inference_steps": 25
    }
)

# To access the file URL:
print(output[0].url())
#=> "http://example.com"

# To write the file to disk:
with open("my-image.png", "wb") as file:
    file.write(output[0].read())