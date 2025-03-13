import asyncio
import ollama
from config import USER_PROMPT, REFERENCE_MODELS, AGGREGATOR_MODEL, AGGREGATOR_SYSTEM_PROMPT


async def run_llm(model):
    """Run a single LLM call using Ollama."""
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": USER_PROMPT}]
    )
    return response['message']['content']


async def main():
    # Run all the reference models in parallel
    results = await asyncio.gather(*[run_llm(model) for model in REFERENCE_MODELS])

    # Create the final prompt for the aggregator model
    final_prompt = AGGREGATOR_SYSTEM_PROMPT + "\n" + "\n".join([f"{i + 1}. {resp}" for i, resp in enumerate(results)])

    # Get the final aggregated response by streaming from the aggregator model
    stream = ollama.chat(
        model=AGGREGATOR_MODEL,
        messages=[
            {"role": "system", "content": final_prompt},
            {"role": "user", "content": USER_PROMPT}
        ],
        stream=True
    )

    # Stream and print the result
    for chunk in stream:
        print(chunk['message']['content'], end="", flush=True)


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())