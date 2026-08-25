import os
import json
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BedrockService:
    """Service for interacting with AWS Bedrock AI models using the Converse API"""
    
    def __init__(self):
        """Initialize Bedrock client with credentials from environment"""
        self.aws_bearer_token = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
        self.aws_region = os.getenv("AWS_REGION", "ap-southeast-2")
        self.model_id = os.getenv("MODEL_ID", "amazon.nova-lite-v1:0")
        
        # Configure Bedrock client
        self.bedrock_runtime = self._configure_bedrock()
    
    def _configure_bedrock(self):
        """Configure AWS Bedrock client with API credentials"""
        try:
            client = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.aws_region,
            )
            return client
        except Exception as e:
            print(f"Error configuring Bedrock client: {e}")
            return None
    
    def get_ai_recommendation(self, prompt: str, max_tokens: int = 4096) -> str:
        """Get AI recommendation from AWS Bedrock using the unified Converse API"""
        if self.bedrock_runtime is None:
            return self._generate_fallback_response(prompt)
        
        try:
            # Menggunakan Amazon Bedrock Converse API yang mendukung Amazon Nova & Claude
            response = self.bedrock_runtime.converse(
                modelId=self.model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                inferenceConfig={
                    "maxTokens": max_tokens,
                    "temperature": 0.7,
                }
            )
            
            # Ekstrak teks respons dengan aman dari struktur respons Converse API
            output_message = response.get("output", {}).get("message", {})
            content_blocks = output_message.get("content", [])
            
            for block in content_blocks:
                if "text" in block:
                    return block["text"]
            
            return str(response)
                
        except Exception as e:
            print(f"Error getting AI recommendation: {e}")
            return self._generate_fallback_response(prompt)
    
    def _generate_fallback_response(self, prompt: str) -> str:
        """Generate a rich structured fallback response in markdown when Bedrock is unavailable"""
        return """# ✈️ Custom AI Itinerary

## 📋 Trip Overview
- **Destination:** Custom Destination
- **Duration:** As requested
- **Total Budget:** Unlimited / No Limit
- **Travel Style:** Flexible

---

## 🗓️ Daily Itinerary
### 🌅 Day 1: Arrival & Grand Exploration
- 🛬 **Airport Arrival** — VIP Transfer & Check-in.
- 🍽️ **Dining** — Premium local dining experience.
---"""
    
    def plan_trip_itinerary(
        self,
        destination: str,
        days: int,
        budget: float,
        travel_style: str
    ) -> str:
        """Generate a rich, structured trip itinerary using AWS Bedrock AI for up to 30 days with optional unlimited budget."""
        
        # Format budget display (jika budget sangat besar atau 0, anggap tanpa limit / unlimited)
        is_unlimited = budget >= 99999 or budget <= 0
        budget_str = "Unlimited / No Limit (Luxury & Flexibility)" if is_unlimited else f"USD {budget:,.2f}"
        daily_budget_str = "Unlimited" if is_unlimited else f"USD {budget / max(days, 1):,.2f}"

        prompt = f"""You are a world-class travel planner with 20 years of experience crafting highly detailed, personalized travel itineraries. Your task is to create an exceptional, comprehensive {days}-day itinerary for {destination}.

=== TRIP PARAMETERS ===
- Destination   : {destination}
- Duration      : {days} Days (You MUST generate ALL days from Day 1 to Day {days} completely without truncation!)
- Total Budget  : {budget_str}
- Daily Budget  : {daily_budget_str}
- Travel Style  : {travel_style}

=== STRICT OUTPUT FORMAT (MANDATORY) ===
Respond ONLY in valid Markdown. Follow this exact structure for EVERY single day (Day 1 through Day {days}):

# ✈️ {destination} — {days}-Day {travel_style} Itinerary

## 📋 Trip Overview
- **Destination:** {destination}
- **Duration:** {days} Days
- **Total Budget:** {budget_str}
- **Daily Budget:** {daily_budget_str}
- **Travel Style:** {travel_style}

## 🗓️ Daily Itinerary

[IMPORTANT: You must write out the schedule for EVERY SINGLE DAY from Day 1 to Day {days}. Do not summarize or stop early.]

### 🌅 Day 1: [Catchy theme title]
#### ☀️ Morning (07:00 – 12:00)
- 🏛️ **[Activity 1]** — [Description]. Cost: $X. Duration: X hrs.
- ☕ **[Breakfast]** — [Description]. Cost: $X.
#### 🌤️ Afternoon (12:00 – 18:00)
- 🏯 **[Cultural Site]** — [Description]. Cost: $X.
- 🍜 **[Lunch]** — [Description]. Cost: $X.
#### 🌙 Evening (18:00 – 22:00)
- 🍽️ **[Dinner]** — [Description]. Cost: $X.

*(Repeat the above Day structure sequentially for ALL remaining days up to Day {days}: Day 2, Day 3, ..., Day {days})*

## 💰 Complete Budget Breakdown
| Category | Total Cost | Notes |
|----------|-----------|-------|
| 🏨 Accommodation | $X | {days} nights |
| 💳 GRAND TOTAL | **{budget_str}** | **Customized for {days} days** |

## 📱 Essential Tips
### 💡 Top 5 Insider Tips
1. [Specific tip]
2. [Specific tip]

### 🍽️ Must-Try Local Foods
- **[Dish 1]:** [Description]
- **[Dish 2]:** [Description]
---
"""

        # Set max_tokens lebih tinggi (misal 8192) agar mampu merender itinerary panjang hingga 30 hari
        max_tokens = 8192 if days > 10 else 4096
        return self.get_ai_recommendation(prompt, max_tokens=max_tokens)


# Create a singleton instance
bedrock_service = BedrockService()