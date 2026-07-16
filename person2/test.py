from google import genai

client = genai.Client(
    api_key="AIzaSyC4uDjDY0KczFiWA_YcFkCiMBnhb3Vq0JU"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello"
)

print(response.text)