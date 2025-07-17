output = replicate.run(
    "google/veo-3-fast",
    input={
        "prompt": "A hyper-speed superhero, resembling The Flash, is sprinting through a dense, dark forest at night. The trees blur into streaks of green and black as he moves. Fiery trails burst behind him with every stride, igniting parts of the underbrush in glowing embers. As he weaves between the trees, the blazing trail he leaves behind slowly forms the words 'VEO 3 FAST' in glowing, molten fire on the forest floor. The camera zooms up to show the entire text.",
        "enhance_prompt": True
    }
)

# To access the file URL:
print(output.url())
#=> "http://example.com"

# To write the file to disk:
with open("my-image.png", "wb") as file:
    file.write(output.read())