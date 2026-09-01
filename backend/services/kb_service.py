import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Menggunakan bedrock-agent-runtime khusus untuk Knowledge Base (RAG)
kb_client = boto3.client(
    "bedrock-agent-runtime",
    region_name=os.getenv("AWS_REGION", "ap-southeast-2")
)

def ask_knowledge_base(question: str):
    """
    Menggunakan retrieve_and_generate() agar LLM merangkum jawaban dari Knowledge Base.
    Fallback ke retrieve() jika retrieve_and_generate tidak tersedia.
    """
    KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID", "EW7EM5BPON")
    aws_region = os.getenv("AWS_REGION", "ap-southeast-2")
    MODEL_ARN = f"arn:aws:bedrock:{aws_region}::foundation-model/amazon.nova-lite-v1:0"

    # --- Coba retrieve_and_generate terlebih dahulu ---
    try:
        response = kb_client.retrieve_and_generate(
            input={"text": question},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": MODEL_ARN,
                },
            },
        )

        answer = response.get("output", {}).get("text", "")

        # Ambil citations / sumber dari retrieve_and_generate
        sources = []
        citations = response.get("citations", [])
        for citation in citations:
            for ref in citation.get("retrievedReferences", []):
                location = ref.get("location", {})
                if location.get("type") == "S3":
                    uri = location.get("s3Location", {}).get("uri", "")
                    if uri:
                        filename = uri.split("/")[-1]
                        if filename not in sources:
                            sources.append(filename)

        if not answer:
            answer = "Maaf, tidak ditemukan informasi yang relevan di Knowledge Base."

        return {"answer": answer, "sources": sources}

    except Exception as e:
        print(f"retrieve_and_generate gagal, fallback ke retrieve: {str(e)}")

    # --- Fallback: retrieve() + gabungkan teks chunk ---
    try:
        response = kb_client.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={"text": question},
        )

        retrieval_results = response.get("retrievalResults", [])
        sources = []
        answer_texts = []

        for result in retrieval_results:
            content_text = result.get("content", {}).get("text", "")
            if content_text:
                answer_texts.append(content_text)

            location = result.get("location", {})
            if location.get("type") == "S3":
                uri = location.get("s3Location", {}).get("uri", "")
                if uri:
                    filename = uri.split("/")[-1]
                    if filename not in sources:
                        sources.append(filename)

        generated_text = (
            "\n\n".join(answer_texts)
            if answer_texts
            else "Maaf, tidak ditemukan informasi yang relevan di Knowledge Base."
        )

        return {"answer": generated_text, "sources": sources}

    except Exception as e:
        print(f"Error querying Knowledge Base: {str(e)}")
        return {
            "answer": f"Maaf, gagal mengambil informasi dari Knowledge Base: {str(e)}",
            "sources": [],
        }
