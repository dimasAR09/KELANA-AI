import boto3
import os
from dotenv import load_dotenv

load_dotenv()

KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID", "EW7EM5BPON")
AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")
MODEL_ID = os.getenv("MODEL_ID", "amazon.nova-lite-v1:0")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Client untuk retrieve dari Knowledge Base
kb_client = boto3.client(
    "bedrock-agent-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

# Client untuk generate jawaban via LLM
bedrock_runtime = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def ask_knowledge_base(question: str):
    """
    RAG manual:
    1. retrieve() — ambil chunks relevan dari Knowledge Base
    2. Kirim chunks + pertanyaan ke Bedrock LLM untuk dirangkum
    3. Kembalikan jawaban terstruktur + sumber dokumen
    """

    # --- Step 1: Retrieve chunks dari Knowledge Base ---
    try:
        print(f"[KB] Retrieving from KB_ID={KNOWLEDGE_BASE_ID}, question={question!r}")
        response = kb_client.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={"text": question},
        )
    except Exception as e:
        print(f"[KB] retrieve() GAGAL: {type(e).__name__}: {str(e)}")
        return {
            "answer": f"Maaf, gagal mengambil informasi dari Knowledge Base: {str(e)}",
            "sources": []
        }

    retrieval_results = response.get("retrievalResults", [])

    if not retrieval_results:
        return {
            "answer": "Maaf, tidak ditemukan informasi yang relevan di Knowledge Base.",
            "sources": []
        }

    # --- Step 2: Kumpulkan teks chunks dan sumber ---
    context_parts = []
    sources = []

    for result in retrieval_results:
        content_text = result.get("content", {}).get("text", "").strip()
        if content_text:
            context_parts.append(content_text)

        location = result.get("location", {})
        if location.get("type") == "S3":
            uri = location.get("s3Location", {}).get("uri", "")
            if uri:
                filename = uri.split("/")[-1]
                if filename not in sources:
                    sources.append(filename)

    context = "\n\n---\n\n".join(context_parts)

    # --- Step 3: Kirim ke LLM untuk merangkum jawaban ---
    prompt = f"""You are a helpful travel assistant for Indonesian travelers. 
Answer the following question based ONLY on the provided context. 
Be concise, clear, and structured. If the context does not contain enough information, say so.

Context:
{context}

Question: {question}

Answer:"""

    try:
        print(f"[KB] Sending to LLM model={MODEL_ID}")
        llm_response = bedrock_runtime.converse(
            modelId=MODEL_ID,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            inferenceConfig={
                "maxTokens": 1024,
                "temperature": 0.3,
            }
        )

        output_message = llm_response.get("output", {}).get("message", {})
        content_blocks = output_message.get("content", [])

        answer = ""
        for block in content_blocks:
            if "text" in block:
                answer = block["text"]
                break

        if not answer:
            answer = "Maaf, LLM tidak menghasilkan jawaban."

    except Exception as e:
        print(f"[KB] LLM generate GAGAL: {type(e).__name__}: {str(e)}")
        # Fallback: kembalikan raw chunks jika LLM gagal
        answer = context if context else "Maaf, tidak ditemukan informasi yang relevan."

    return {
        "answer": answer,
        "sources": sources
    }
