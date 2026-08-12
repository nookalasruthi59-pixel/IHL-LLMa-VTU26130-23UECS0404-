from mcp.server.fastmcp import FastMCP
from openai import OpenAI

mcp = FastMCP("Creative Story Server")

# Connect to LM Studio
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)


@mcp.tool()
def write_story(topic: str) -> str:
    """
    Write a very creative story about the given topic
    and save it as a text file.
    """

    prompt = f"""
Write a very creative and engaging story about:

{topic}

Requirements:
- Create an interesting title.
- Make the story imaginative and original.
- Include memorable characters.
- Include emotions, dialogue and descriptions.
- Have a clear beginning, middle and ending.
- Make the story enjoyable to read.
- Do not explain how you created the story.
- Output only the story.
"""

    response = client.chat.completions.create(
        model="local-model",
        messages=[
            {
                "role": "system",
                "content": "You are an extremely creative fiction writer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1.0,
        max_tokens=2000
    )

    story = response.choices[0].message.content

    with open("creative_story.txt", "w", encoding="utf-8") as file:
        file.write(story)

    return f"Story created successfully and saved to creative_story.txt\n\n{story}"


if __name__ == "__main__":
    mcp.run()