import replicate

input = {
    "output_quality": 100
}

output = replicate.run(
    "fofr/sticker-maker:4acb778eb059772225ec213948f0660867b2e03f277448f18cf1800b96a65a1a",
    input=input
)

# To access the file URLs:
print(output[0].url())
#=> "https://replicate.delivery/.../output_0.webp"

# To write the files to disk:
for index, item in enumerate(output):
    with open(f"output_{index}.webp", "wb") as file:
        file.write(item.read())
#=> output_0.webp written to disk