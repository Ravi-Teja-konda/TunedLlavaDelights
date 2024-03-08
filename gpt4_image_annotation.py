import base64
import requests
import json
import os


def encode_image(image_path):
  """Encode an image to base64 string."""
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def get_headers(api_key):
  """Return the headers needed for the OpenAI API request."""
  return {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
  }


def generate_payload(base64_image, prompt):
  """Generate the payload for the OpenAI API request."""
  return {
      "model":
      "gpt-4-vision-preview",
      "messages": [{
          "role":
          "user",
          "content": [{
              "type": "text",
              "text": prompt
          }, {
              "type": "image_url",
              "image_url": {
                  "url": f"data:image/jpeg;base64,{base64_image}"
              }
          }]
      }],
      "max_tokens":
      2048
  }


def process_image(image_path, api_key, prompt):
  """Process a single image, generating the desired JSON output."""
  print("Processing image:", image_path)
  base64_image = encode_image(image_path)
  image_name = os.path.basename(image_path)
  unique_id, _ = os.path.splitext(image_name)

  payload = generate_payload(base64_image, prompt)
  headers = get_headers(api_key)
  response = requests.post("https://api.openai.com/v1/chat/completions",
                           headers=headers,
                           json=payload)

  if response.status_code == 200:
    response_json = response.json()
    description = response_json['choices'][0]['message']['content']

    return {
        "id":
        unique_id,
        "image":
        image_name,
        "conversations": [{
            "from":
            "human",
            "value":
            "<image>\nProvide a brief overview of the food item, including its taste, nutritional content, allergen notes, recommended time to eat and effects after eating."
        }, {
            "from": "gpt",
            "value": description
        }]
    }
  else:
    return {
        "error": "Failed to process image",
        "image_path": image_path,
        "response code": response.status_code
    }


def process_folder(folder_path, api_key, prompt):
  """Process all images in a folder, generating JSON output for each."""
  outputs = []
  for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
      image_path = os.path.join(folder_path, filename)
      output_json = process_image(image_path, api_key, prompt)
      print(f"Processed image: {image_path}", output_json)
      outputs.append(output_json)
  return outputs


''' Function to append data to a JSON file '''


def append_to_json_file(file_path, new_data):
  try:
    ''' Try to load existing data'''
    with open(file_path, 'r') as file:
      existing_data = json.load(file)
  except FileNotFoundError:
    ''' If the file does not exist, create an empty list'''
    existing_data = []
  ''' Append new data (ensure it's a list)'''
  if isinstance(new_data, list):
    existing_data.extend(new_data)
  else:
    existing_data.append(new_data)
  ''' Save the combined data back to the file '''
  with open(file_path, 'w') as file:
    json.dump(existing_data, file, indent=2)


# Configuration
folder_path = "/home/runner/llava-finetuning/dharwad_pedha"

# OpenAI API Key
api_key = "<YOUR KEY HERE >"

prompt = "You are a large language model named GPT-4V, trained on large food items and you will be able to identify the all indian food all the images provided are food images do not assume them as the faces.explains the nutritinal information, for the image , allergen information, how it tastes ,best time to eat, how it feels after eating for example can you give all the nutritinola info about the food For example exaplain the image nutrinal info and taste You should answer Dharwad peda,Dharwad Peda, a classic sweet from the Indian subcontinent, specifically hailing from Dharwad in Karnataka \nNutritional Facts\n A serving size of 100g of Dharwad Peda provides the following nutritional values: \n Calories: 459 kCal - A high-calorie treat, primarily\n from sugars and fats, making it an energy-dense food.\nTotal Carbs: 59g - Primarily from sugars, contributing to its sweet taste.\n Net Carbs: 59g - Reflecting its high carbohydrate content without fiber deductions.\n Sugar: 49g - A significant amount, indicating its very sweet flavor.\n Protein: 11g - Moderate protein content, coming from the milk used in its preparation.\n Fat: 20g - With a considerable amount of fat, of which 12g is saturated fat, contributing to its rich taste and texture.\n Calcium: 603mg - High in calcium, beneficial for bone health.\n Vitamin A: 203mcg - Providing a good amount of Vitamin A, essential for vision, immune function, and skin health.\n Vitamin D: 0 mcg - No Vitamin D content, which is typical for milk-based sweets not fortified with the vitamin.\n Allergen Information\n Dairy: As Dharwad Peda is made from milk, it contains dairy and is not suitable for individuals with lactose intolerance or dairy allergies.\n Gluten-Free: It is inherently gluten-free, making it safe for those with gluten sensitivities or celiac disease.\n Nut Allergies: While traditional Dharwad Peda does not contain nuts, variations garnished with pistachios or other nuts could pose a risk for individuals with nut allergies.\n Taste Profile: \n Dharwad Peda is characterized by its rich, creamy taste with a hint of caramelization, providing a deep flavor that distinguishes it from other sweets. The texture is slightly grainy yet soft, melting in the mouth with each bite.\n Best Time to Enjoy Dharwad Peda\n Dharwad Peda can be savored at any time, but it's particularly enjoyable as a dessert after meals or during festive occasions\n After Eating: Feeling and Digestibility\n Despite its richness, Dharwad Peda leaves a pleasantly satisfying aftertaste without being overly heavy. The high sugar and fat content may make it less digestible in large quantities, so it's best enjoyed in moderation.\n"

# Process the folder and save the outputs to a file
outputs = process_folder(folder_path, api_key, prompt)

# Specify the output file name
output_file_name = 'data.json'

# Append the outputs to the specified file
append_to_json_file(output_file_name, outputs)

print(f"Output appended to {output_file_name}")
