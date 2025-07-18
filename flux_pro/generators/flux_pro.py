import replicate

def generate_image(prompt, **params):
    """
    Genera una imagen usando el modelo Flux Pro de black-forest-labs.
    """
    client = replicate.Client()
    
    prediction = client.predictions.create(
        version="black-forest-labs/flux-pro",
        input={
            "prompt": prompt,
            **params
        }
    )
    
    return prediction
