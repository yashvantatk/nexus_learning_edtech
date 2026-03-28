import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load your Gemini key from the .env file
load_dotenv(override=True)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def process_solo_notes(raw_notes):
    """Converts messy individual notes into a structured guide."""
    prompt = f"""
    You are an expert academic tutor. Take these messy, unstructured lecture notes and convert them into a highly structured, easy-to-read study guide.
    Format the output using Markdown:
    - Include a brief 'Executive Summary' at the top.
    - Use clear Headings (##) for main topics.
    - Use bullet points for key details.
    - If applicable, extract any data or comparisons into a Markdown table.

    Raw Notes:
    {raw_notes}
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text


def process_collab_notes(notes_list):
    """Merges multiple sets of notes into one Master Guide."""
    combined_notes = "\n\n--- NEXT STUDENT'S NOTES ---\n\n".join(notes_list)
    prompt = f"""
    You are an expert academic synthesizer. You have been given lecture notes from multiple students on the same topic.
    Your job is to merge them into one 'Master Study Guide'. 
    - Fill in the gaps: If Student A missed something that Student B caught, combine them logically.
    - Format using beautiful Markdown (Headings, bullet points, bold text for key terms).
    - Add a section at the bottom called 'Synthesized Insights' highlighting the most critical concepts they all shared.

    Combined Notes:
    {combined_notes}
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text