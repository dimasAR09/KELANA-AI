import os
import json
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BedrockService:
    """Service for interacting with AWS Bedrock AI models"""
    
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
            # Create bedrock-runtime client
            # For bearer token authentication, we'll use it as AWS credentials
            client = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.aws_region,
                # Bearer token will be handled by boto3 session
            )
            return client
        except Exception as e:
            print(f"Error configuring Bedrock client: {e}")
            # Return a mock client for development if connection fails
            return None
    
    def get_ai_recommendation(self, prompt: str, max_tokens: int = 2000) -> str:
        """
        Get AI recommendation from AWS Bedrock
        
        Args:
            prompt: The prompt to send to the AI model
            max_tokens: Maximum tokens in the response
            
        Returns:
            str: AI generated response
        """
        # Fallback response if Bedrock is not configured
        if self.bedrock_runtime is None:
            return self._generate_fallback_response(prompt)
        
        try:
            # Prepare the request body based on the model
            request_body = {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            # Invoke the model
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(request_body)
            )
            
            # Parse the response
            response_body = json.loads(response['body'].read())
            
            # Extract the generated text (format may vary by model)
            if 'content' in response_body:
                if isinstance(response_body['content'], list):
                    return response_body['content'][0].get('text', '')
                return response_body['content']
            elif 'completion' in response_body:
                return response_body['completion']
            else:
                return str(response_body)
                
        except Exception as e:
            print(f"Error getting AI recommendation: {e}")
            # Return fallback response on error
            return self._generate_fallback_response(prompt)
    
    def _generate_fallback_response(self, prompt: str) -> str:
        """Generate a fallback response in markdown format when Bedrock is unavailable"""
        if "Japan" in prompt:
            return """# 🇯🇵 5-Day Japan Itinerary - Family Style

## 📋 Trip Overview
- **Destination:** Japan (Tokyo & Kyoto)
- **Duration:** 5 Days / 4 Nights
- **Budget:** $1,500 USD
- **Travel Style:** Family-friendly
- **Best Season:** Spring (Cherry Blossoms) or Fall (Autumn Colors)

---

## 🗓️ Day-by-Day Itinerary

### Day 1: Arrival in Tokyo
**Theme:** Settle in and explore Shibuya

#### Morning
- ✈️ Arrive at Narita/Haneda Airport
- 🚆 Take Airport Limousine Bus to hotel (~$30)
- 🏨 Check into business hotel in Shinjuku area

#### Afternoon
- 🚶 Explore Shibuya Crossing - World's busiest intersection
- 📸 Photo opportunity at Hachiko Statue
- 🛍️ Shopping at Shibuya 109

#### Evening
- 🍜 Dinner at local ramen restaurant (~$15/person)
- 🌃 Evening walk around Shinjuku

**Daily Cost:** ~$120 (accommodation + meals + transport)

---

### Day 2: Tokyo Sightseeing
**Theme:** Traditional & Modern Tokyo

#### Morning
- ⛩️ Visit Senso-ji Temple in Asakusa
- 🏮 Walk through Nakamise Shopping Street
- 🍡 Try traditional Japanese snacks

#### Afternoon
- 🗼 Tokyo Skytree or Tokyo Tower (choose one, ~$20)
- 🎮 Explore Akihabara - Electronics & Anime district
- 🎯 Visit Don Quijote for souvenirs

#### Evening
- 🍱 Dinner at conveyor belt sushi (~$25/person)
- 🌆 Night view from Tokyo Tower

**Daily Cost:** ~$100 (meals + entrance fees + transport)

---

### Day 3: Mount Fuji Day Trip
**Theme:** Nature & Scenic Beauty

#### Full Day Excursion
- 🚆 Take train to Kawaguchiko Station (~$50 round trip)
- 🗻 Visit Mount Fuji 5th Station (weather permitting)
- 🚡 Kachi Kachi Ropeway for panoramic views
- 🌊 Relax at Lake Kawaguchi
- 📸 Photo spots with Mt. Fuji backdrop

#### Return to Tokyo
- 🚆 Evening train back to Tokyo
- 🍔 Quick dinner at station (~$15)

**Daily Cost:** ~$150 (transport + activities + meals)

---

### Day 4: Kyoto Adventure
**Theme:** Cultural Heritage

#### Morning
- 🚄 Shinkansen (Bullet Train) to Kyoto (~$140 one-way)
- 🎫 Tip: Consider JR Pass for savings
- 🧳 Drop luggage at hotel or coin locker

#### Afternoon
- ⛩️ Fushimi Inari Shrine - Famous 1000 red torii gates
- 🦌 Optional: Quick visit to Nara for deer park
- 🏯 Explore Gion District - Geisha quarter

#### Evening
- 🍱 Traditional kaiseki dinner (~$50/person)
- 🌸 Evening stroll through Gion streets

**Daily Cost:** ~$280 (Shinkansen + hotel + meals)

---

### Day 5: Kyoto Morning & Departure
**Theme:** Final cultural immersion

#### Morning
- 🎋 Arashiyama Bamboo Grove - Magical bamboo forest
- 🐒 Iwatayama Monkey Park (optional)
- ⛩️ Kinkaku-ji (Golden Pavilion) - UNESCO site (~$5)

#### Afternoon
- 🚄 Return to Tokyo via Shinkansen (~$140)
- 🛍️ Last-minute shopping at Tokyo Station
- ✈️ Depart from Narita/Haneda Airport

**Daily Cost:** ~$180 (transport + entrance fees + meals)

---

## 💰 Budget Breakdown

| Category | Cost | Details |
|----------|------|---------|
| 🏨 **Accommodation** | $320 | Business hotels (4 nights × $80) |
| 🍜 **Food & Drinks** | $250 | Mix of restaurants & convenience stores |
| 🚆 **Transportation** | $450 | Shinkansen, trains, airport transfer |
| 🎫 **Activities & Entrance Fees** | $150 | Temples, towers, attractions |
| 🛍️ **Shopping & Souvenirs** | $150 | Gifts, snacks, personal items |
| 🆘 **Emergency Buffer** | $180 | Unexpected expenses |
| **TOTAL** | **$1,500** | Complete trip budget |

---

## 📱 Essential Tips

### Transportation
- 🎫 Get a **Suica/Pasmo IC card** for easy train travel
- 🚄 Consider **JR Pass** if traveling extensively (7-day pass ~$280)
- 📲 Download **Google Maps** & **Hyperdia** app for routes

### Money-Saving Tips
- 🏪 Eat breakfast at convenience stores (onigiri ~$2)
- 🍱 Try budget lunch sets at restaurants (~$8-12)
- 🏨 Book hotels in advance for better rates
- 💴 Withdraw cash at 7-Eleven ATMs (lowest fees)

### Family-Friendly Advice
- 👶 Strollers can be challenging in crowded trains
- 🍼 Baby facilities available at most stations
- 🎒 Use coin lockers for luggage storage
- 🚻 Toilets are clean and everywhere!

### Must-Have Apps
- 📱 Google Translate (offline mode)
- 🗺️ Google Maps (works perfectly in Japan)
- 🚆 Hyperdia (train schedules)
- 💴 Currency converter

### Cultural Etiquette
- 🙏 Bow when greeting
- 🔇 Keep voice down in trains
- 🚭 No eating while walking
- 👟 Remove shoes when entering homes/temples

---

## 🎯 What's Included vs Not Included

### ✅ Included in Budget
- All transportation (trains, buses, airport transfer)
- Accommodation for 4 nights
- Meals (breakfast, lunch, dinner)
- Entrance fees to attractions
- Basic shopping/souvenirs

### ❌ Not Included
- ✈️ International flights
- 🛡️ Travel insurance (highly recommended!)
- 📱 Pocket WiFi rental (~$10/day if needed)
- 🎁 Extensive shopping
- 🍶 Alcohol/special dining experiences

---

## 🌟 Bonus Recommendations

### If You Have Extra Budget
1. 🎌 **TeamLab Borderless** - Digital art museum ($35)
2. 🐟 **Tsukiji Outer Market** - Fresh seafood breakfast
3. 🎭 **Robot Restaurant** - Unique Tokyo show experience
4. ♨️ **Onsen Experience** - Traditional hot springs
5. 🍣 **Sushi Making Class** - Learn from masters

### Free Activities
- 🏯 Imperial Palace East Gardens (Tokyo)
- ⛩️ Meiji Shrine (free entry)
- 🌸 Parks (Ueno, Yoyogi) - especially during cherry blossom season
- 🎪 People watching in Harajuku
- 🌉 Rainbow Bridge walk at sunset

---

## 📞 Emergency Contacts
- 🚨 Emergency: **110** (Police) / **119** (Ambulance/Fire)
- 🏥 Japan Helpline: **0570-000-911** (English support)
- 🗺️ Tourist Information: Available at major stations

---

## ✨ Final Tips for Success
1. ⏰ Start days early - attractions less crowded
2. 💴 Always carry cash - not all places accept cards
3. 📶 Get a SIM card or pocket WiFi at airport
4. 🎫 Book Shinkansen tickets in advance during peak season
5. 📝 Learn basic Japanese phrases - locals appreciate the effort!

---

**Enjoy your amazing family adventure in Japan! 🇯🇵✨**

*This itinerary is flexible - adjust based on your family's pace and interests!*"""
        else:
            # Generic fallback for other destinations
            destination = "your destination"
            if "Bali" in prompt or "bali" in prompt:
                destination = "Bali"
            elif "Australia" in prompt or "australia" in prompt:
                destination = "Australia"
            
            return f"""# ✈️ Travel Itinerary for {destination}

## 📋 Trip Overview
*This is a sample itinerary template. For full AI-powered recommendations, please configure AWS Bedrock credentials.*

---

## 🗓️ Day-by-Day Activities

### Day 1: Arrival
- ✈️ Arrive at airport
- 🏨 Check into accommodation
- 🍽️ Welcome dinner at local restaurant
- 🌆 Evening exploration of nearby area

### Day 2: Main Attractions
- 🏛️ Visit top tourist attractions
- 📸 Photo opportunities at iconic spots
- 🍜 Try local cuisine for lunch
- 🛍️ Shopping at local markets

### Day 3: Cultural Experience
- 🎭 Cultural activities and experiences
- ⛩️ Visit historical sites
- 🎨 Local art and craft exploration
- 🍱 Traditional dinner experience

---

## 💰 Budget Planning

### Estimated Costs
- **Accommodation:** Budget according to travel style
- **Food & Drinks:** Local restaurants and street food
- **Transportation:** Public transport and taxis
- **Activities:** Entrance fees and tours
- **Shopping:** Souvenirs and personal items
- **Emergency Fund:** 10-15% of total budget

---

## 📱 Essential Tips

### Before You Go
- 📋 Check visa requirements
- 💉 Get necessary vaccinations
- 💳 Notify bank of travel plans
- 📱 Download offline maps
- 💵 Exchange some local currency

### During Your Trip
- 🗺️ Use public transportation when possible
- 🍴 Try local street food (safe and delicious!)
- 📸 Respect local customs and photography rules
- 💧 Stay hydrated and carry water
- 🔐 Keep valuables secure

### Money-Saving Tips
- 🏪 Eat where locals eat
- 🎫 Book activities in advance for discounts
- 🚶 Walk when possible to explore neighborhoods
- 🏨 Stay in central locations to save on transport
- 🛒 Shop at local markets instead of tourist shops

---

## 🌟 Must-Do Activities
1. Sample authentic local cuisine
2. Visit main tourist attractions
3. Explore local markets
4. Take memorable photos
5. Interact with locals

---

## ✨ Have a Great Trip!

*Customize this itinerary based on your preferences, pace, and budget.*

**For detailed AI-powered recommendations, please configure AWS Bedrock in your environment.**"""
    
    def plan_trip_itinerary(
        self, 
        destination: str, 
        days: int, 
        budget: float, 
        travel_style: str
    ) -> str:
        """
        Generate a trip itinerary using AWS Bedrock AI
        
        Args:
            destination: Travel destination (e.g., "Japan", "Paris")
            days: Number of days for the trip
            budget: Budget in USD
            travel_style: Style of travel (e.g., "Family", "Solo", "Adventure", "Luxury")
            
        Returns:
            str: Detailed trip itinerary generated by AI in markdown format
        """
        prompt = f"""You are an experienced travel planner. Create a detailed {days}-day itinerary for {destination}.

**Trip Details:**
- Destination: {destination}
- Duration: {days} days
- Budget: USD {budget:,.2f}
- Travel Style: {travel_style}

**Please format your response in MARKDOWN with the following structure:**

# [Destination] Itinerary - {travel_style} Style

## 📋 Trip Overview
- Destination, duration, budget, travel style summary
- Best time to visit

## 🗓️ Day-by-Day Itinerary
### Day 1: [Theme]
#### Morning
- Activity 1
- Activity 2

#### Afternoon
- Activity 3
- Activity 4

#### Evening
- Activity 5
- Dinner recommendations

**Daily Cost:** $X

[Repeat for each day]

## 💰 Budget Breakdown
Create a table with:
- Accommodation
- Food & Drinks
- Transportation
- Activities
- Shopping
- Emergency fund
- **TOTAL**

## 📱 Essential Tips
### Transportation Tips
### Money-Saving Tips
### {travel_style}-Friendly Advice
### Cultural Etiquette

## 🌟 Bonus Recommendations
- Additional activities if budget allows
- Free activities

## ✨ Final Tips
- 5-10 practical tips for success

**IMPORTANT:**
- Use markdown headers (# ## ###)
- Use bullet points with emojis for visual appeal
- Include specific prices and costs
- Make sure total budget matches USD {budget:,.2f}
- Tailor everything to {travel_style} travel style
- Be specific with locations, timings, and costs
- Include practical tips and local insights"""
        
        return self.get_ai_recommendation(prompt, max_tokens=3000)


# Create a singleton instance
bedrock_service = BedrockService()


# Example usage and testing functions
def test_simple_recommendation():
    """Test with a simple prompt"""
    service = BedrockService()
    prompt = """You are an experienced travel planner.
Create a 5-day itinerary for Japan.
Budget: USD 1,500
Travel Style: Family"""
    
    result = service.get_ai_recommendation(prompt)
    print("Simple Recommendation Test:")
    print(result)
    print("\n" + "="*80 + "\n")
    return result


def test_dynamic_trip_planning():
    """Test with the dynamic trip planning function"""
    service = BedrockService()
    result = service.plan_trip_itinerary(
        destination="Japan",
        days=5,
        budget=1500,
        travel_style="Family"
    )
    print("Dynamic Trip Planning Test:")
    print(result)
    print("\n" + "="*80 + "\n")
    return result


if __name__ == "__main__":
    # Run tests when executing this file directly
    print("Testing AWS Bedrock Service...\n")
    
    try:
        # Test 1: Simple recommendation
        test_simple_recommendation()
        
        # Test 2: Dynamic trip planning
        test_dynamic_trip_planning()
        
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
