from ollama import Client
import base64

def setup_client(host):
    return Client(host=f'http://{host}:11434', headers={'Content-Type': 'application/json'})


def list_models(client):
    model_data = client.list()
    models = []
    for m in model_data.models:
        models.append(m.model)
    return models


def ask_model(client, model, prompt):
    response = client.chat(model=model, messages=[
      {
        'role': 'user',
        'content': prompt,
      },
    ])
    return response


def ask_model_with_image(client, model, prompt, img_data):
    messages = [
        {
            "role": "user",
            "content": prompt,
            "images": [base64.b64encode(img_data).decode('utf-8')]
        }
    ]
    return client.chat(model=model,messages=messages)


def delete_model(client, model):
    client.delete(model)
    print(f'[+] Deleting {model}')


def download_model(client, model):
    print(f'[+] Pulling model: {model}')
    client.pull(model)
