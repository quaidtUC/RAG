import os


def generate_answer(query: str, context: str) -> str:
    """Generate an answer to ``query`` using ``context`` as background.

    If ``OPENAI_API_KEY`` is set in the environment, the function will use the
    OpenAI API to generate a response. Otherwise, it falls back to a small
    open-source model from Hugging Face via ``transformers``.
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        import openai

        openai.api_key = openai_key
        model = os.getenv("OPENAI_MODEL", "text-davinci-003")
        prompt = f"{context}\n\n{query}\n"
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=256,
            temperature=0.7,
        )
        return response.choices[0].text.strip()

    # Fall back to an open-source model
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch

    model_name = os.getenv("HF_MODEL", "distilgpt2")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    inputs = tokenizer(f"{context}\n\n{query}", return_tensors="pt").to(device)
    output_ids = model.generate(
        **inputs,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7,
    )
    text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    # Remove the context from the beginning of the generated text if present
    if text.startswith(context):
        text = text[len(context):].lstrip()
    return text.strip()
