from groq import Groq

client = Groq(api_key="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")
completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "hi"
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
