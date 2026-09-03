"""
conversation_service.py
-----------------------
Business logic untuk Conversation Memory (Session 10).

Flow saat user mengirim pesan:
  1. Simpan user message ke DB
  2. Load semua previous messages dari conversation
  3. Build prompt (full conversation history)
  4. Panggil Amazon Bedrock
  5. Simpan AI response ke DB
  6. Kembalikan response
"""

from sqlalchemy.orm import Session
from models.conversation import Conversation, Message
from services.bedrock_service import bedrock_service

# Jumlah maksimum message yang dikirim ke Bedrock (trim context window - Part 8)
MAX_HISTORY_MESSAGES = 20


# ── Conversation CRUD ────────────────────────────────────────────────────────

def create_conversation(db: Session, user_id: int, title: str | None = None) -> Conversation:
    """Buat conversation baru dan kembalikan objeknya."""
    conv = Conversation(user_id=user_id, title=title)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


def list_conversations(db: Session, user_id: int) -> list[Conversation]:
    """Daftar semua conversation milik user, paling baru dulu."""
    return (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .all()
    )


def get_conversation(db: Session, conversation_id: int, user_id: int) -> Conversation | None:
    """Ambil satu conversation, pastikan milik user yang sedang login."""
    return (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        .first()
    )


def rename_conversation(db: Session, conversation_id: int, user_id: int, title: str) -> Conversation | None:
    """Ganti title conversation (Challenge: rename)."""
    conv = get_conversation(db, conversation_id, user_id)
    if conv is None:
        return None
    conv.title = title
    db.commit()
    db.refresh(conv)
    return conv


# ── Message & Prompt Builder ─────────────────────────────────────────────────

def get_messages(db: Session, conversation_id: int) -> list[Message]:
    """Ambil semua message dalam conversation, diurutkan dari yang terlama."""
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )


def _save_message(db: Session, conversation_id: int, role: str, content: str) -> Message:
    """Simpan satu message ke DB."""
    msg = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def _build_bedrock_messages(history: list[Message], new_user_content: str) -> list[dict]:
    """
    Part 5 — Prompt Builder:
    Rekonstruksi full conversation history sebagai list message
    yang siap dikirim ke Amazon Bedrock Converse API.

    Juga menerapkan Part 8 (trim context window):
    hanya ambil MAX_HISTORY_MESSAGES pesan terakhir dari history
    sebelum menambah pesan baru.
    """
    # Trim context: ambil N pesan terakhir saja
    trimmed = history[-MAX_HISTORY_MESSAGES:] if len(history) > MAX_HISTORY_MESSAGES else history

    messages = []
    for msg in trimmed:
        messages.append({
            "role": msg.role,           # "user" atau "assistant"
            "content": [{"text": msg.content}],
        })

    # Tambah pesan user terbaru
    messages.append({
        "role": "user",
        "content": [{"text": new_user_content}],
    })

    return messages


def send_message(db: Session, conversation_id: int, user_id: int, user_content: str) -> Message | None:
    """
    Orkestrasi lengkap (Part 4 — Send Message API):
      1. Validasi conversation milik user
      2. Simpan user message
      3. Load previous messages
      4. Build prompt dengan history
      5. Panggil Bedrock
      6. Simpan AI response
      7. Kembalikan AI Message object
    """
    # 1. Validasi
    conv = get_conversation(db, conversation_id, user_id)
    if conv is None:
        return None

    # Auto-set title dari pesan pertama jika belum ada
    if conv.title is None:
        short_title = user_content[:60].strip()
        conv.title = short_title
        db.commit()

    # 2. Simpan user message
    _save_message(db, conversation_id, role="user", content=user_content)

    # 3. Load semua previous messages (tidak termasuk yang baru saja disimpan)
    history = get_messages(db, conversation_id)

    # 4. Build prompt — semua history (termasuk pesan user terbaru sudah ada di DB)
    #    Kita kirim semua messages yang ada di history sebagai context
    #    (pesan user terbaru sudah masuk lewat _save_message di atas,
    #    jadi kita reconstruct dari DB agar ordernya konsisten)
    bedrock_messages = _build_bedrock_messages(
        history=history[:-1],          # semua kecuali yang baru disimpan
        new_user_content=user_content,
    )

    # 5. Panggil Amazon Bedrock dengan context-aware messages
    try:
        ai_text = _call_bedrock_with_history(bedrock_messages)
    except Exception as e:
        print(f"[ConvService] Bedrock error: {e}")
        ai_text = "Maaf, terjadi kesalahan saat menghubungi AI. Silakan coba lagi."

    # 6. Simpan AI response
    ai_message = _save_message(db, conversation_id, role="assistant", content=ai_text)

    return ai_message


def _call_bedrock_with_history(messages: list[dict]) -> str:
    """
    Panggil Bedrock Converse API dengan full conversation history.
    Berbeda dengan get_ai_recommendation() yang hanya menerima single prompt string —
    di sini kita kirim seluruh thread sebagai multi-turn messages.
    """
    client = bedrock_service.bedrock_runtime
    if client is None:
        return _fallback_response(messages[-1]["content"][0]["text"])

    try:
        response = client.converse(
            modelId=bedrock_service.model_id,
            system=[{
                "text": (
                    "Kamu adalah KelanaAI, asisten perjalanan cerdas untuk traveler Indonesia. "
                    "Kamu membantu merencanakan itinerary, memberikan rekomendasi destinasi, "
                    "tips perjalanan, dan menjawab pertanyaan seputar wisata. "
                    "Jawab dengan bahasa yang ramah, informatif, dan terstruktur. "
                    "Ingat seluruh konteks percakapan sebelumnya saat menjawab."
                )
            }],
            messages=messages,
            inferenceConfig={
                "maxTokens": 2048,
                "temperature": 0.7,
            },
        )

        output_message = response.get("output", {}).get("message", {})
        for block in output_message.get("content", []):
            if "text" in block:
                return block["text"]

        return "Maaf, AI tidak menghasilkan respons."

    except Exception as e:
        print(f"[ConvService] _call_bedrock_with_history error: {e}")
        return _fallback_response(messages[-1]["content"][0]["text"])


def _fallback_response(user_message: str) -> str:
    """Fallback sederhana saat Bedrock tidak tersedia."""
    return (
        f"Halo! Saya KelanaAI. Anda bertanya: \"{user_message}\"\n\n"
        "Saat ini koneksi ke AI sedang tidak tersedia. "
        "Pastikan konfigurasi AWS Bedrock sudah benar di file .env."
    )
