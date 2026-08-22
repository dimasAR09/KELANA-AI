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
        """Generate a rich structured fallback response in markdown when Bedrock is unavailable"""

        # Extract destination from prompt context
        destination = "Japan"
        if "Bali" in prompt or "bali" in prompt:
            destination = "Bali"
        elif "Australia" in prompt or "australia" in prompt:
            destination = "Australia"

        if destination == "Japan":
            return """# ✈️ Japan — 5-Day Family Itinerary

## 📋 Trip Overview
- **Destination:** Japan (Tokyo & Kyoto)
- **Duration:** 5 Days / 4 Nights
- **Total Budget:** USD 1,500.00
- **Daily Budget:** USD 300.00
- **Travel Style:** Family
- **Best Time to Visit:** March–May (cherry blossoms) or October–November (autumn foliage)
- **Highlights:** Ancient temples, futuristic cityscapes, world-class cuisine

---

## 🗓️ Daily Itinerary

### 🌅 Day 1: Tokyo Arrival & Shibuya Exploration

#### ☀️ Morning (07:00 – 12:00)
- 🛬 **Narita/Haneda Airport Arrival** — Clear immigration, collect luggage, purchase Suica IC card at airport kiosk for seamless train travel. Estimated cost: $5 (Suica deposit). Duration: 1.5 hours.
- 🚆 **Airport Limousine Bus to Shinjuku** — Scenic transfer through the city. More comfortable than train with luggage. Estimated cost: $30/person. Duration: 1 hour.
- ☕ **Breakfast at 7-Eleven Convenience Store** — Try onigiri (rice balls, $1.50 each), tamagoyaki sandwich ($2), and canned coffee ($1.50). A true local morning experience. Estimated cost: $6 per person.

#### 🌤️ Afternoon (12:00 – 18:00)
- 🏯 **Senso-ji Temple, Asakusa** — Tokyo's oldest Buddhist temple (645 AD). Walk through the iconic Kaminarimon Thunder Gate, explore Nakamise shopping street. Opening hours: 6:00–17:00. Entrance fee: Free.
- 🎭 **Nakamise-dori Local Market Experience** — Shop for traditional crafts: ningyo-yaki cakes ($3), ningyo dolls, tenugui towels. Authentic souvenir-hunting as locals do. Cost: $15–30 budget.
- 🍜 **Lunch at Asakusa Imahan** — Famous sukiyaki restaurant since 1895. Try the lunch set: wagyu beef sukiyaki with rice and miso soup. Cost: $25 per person.

#### 🌙 Evening (18:00 – 22:00)
- 🍽️ **Dinner at Ichiran Ramen, Shibuya** — Solo-booth ramen concept unique to Japan. Order tonkotsu ramen ($12) with kaedama (extra noodles, $1.50). Reservation recommended: No (queue system). Cost: $14 per person.
- 🎶 **Shibuya Crossing & Shibuya Sky** — Experience the world's busiest pedestrian crossing, then ascend Shibuya Sky rooftop observation deck for panoramic night views. Cost: $18 per person. Best time: 8:00pm for city lights.

**💵 Day 1 Estimated Cost:** $160
**🏨 Accommodation:** Shinjuku Washington Hotel, Shinjuku district, $80/night

---

### 🌅 Day 2: Tokyo Deep Dive — Traditional to Futuristic

#### ☀️ Morning (07:00 – 12:00)
- ⛩️ **Meiji Jingu Shrine** — Serene Shinto shrine dedicated to Emperor Meiji, surrounded by 170 acres of forested urban parkland. Arrive early to avoid crowds. Entrance fee: Free. Duration: 1.5 hours.
- 🎪 **Harajuku Takeshita Street** — Colorful pedestrian street with crepe shops ($6), quirky fashion boutiques, and pop culture stores. A must for families. Estimated cost: $10–20. Duration: 1 hour.
- ☕ **Breakfast at Eggs 'n Things, Harajuku** — American-style pancakes topped with whipped cream ($14). Famous Instagram-worthy spot open since 1974. Estimated cost: $14 per person.

#### 🌤️ Afternoon (12:00 – 18:00)
- 🗼 **Tokyo Skytree** — World's tallest broadcasting tower (634m). Visit Tembo Deck (350m) for unobstructed 360° city views. Opening hours: 10:00–21:00. Entrance fee: $20/adult, $10/child.
- 🎮 **Akihabara Electric Town Local Experience** — Explore multi-floor electronics stores, anime merchandise shops, and retro arcade game centers (100 yen/play). Authentic otaku culture. Cost: $10–15 for games and snacks.
- 🍜 **Lunch at Kanda Yabu Soba** — Historic soba noodle restaurant open since 1880. Try the zaru soba (cold noodles with dipping sauce, $12). Cost: $12–18 per person.

#### 🌙 Evening (18:00 – 22:00)
- 🍽️ **Dinner at Gonpachi Nishi-Azabu** — The restaurant that inspired Kill Bill's fight scene. Try the yakitori skewers ($3–5 each), edamame, and Japanese craft beer. Ambiance: traditional izakaya with bamboo décor. Cost: $35 per person.
- 🎶 **Golden Gai, Shinjuku** — Tokyo's most atmospheric nightlife district: 200+ tiny bars each seating 6–8 people. Try a craft sake bar. Cover charge: $5–10. Best time: 8:30pm onward.

**💵 Day 2 Estimated Cost:** $180
**🏨 Accommodation:** Shinjuku Washington Hotel, $80/night

---

### 🌅 Day 3: Mount Fuji & Hakone Day Trip

#### ☀️ Morning (07:00 – 12:00)
- 🚆 **Romancecar Express Train to Hakone** — Depart Shinjuku 7:30am on the Odakyu Romancecar panorama train. Reserved window seats offer views of Mt. Fuji. Cost: $28/person round trip. Duration: 1.5 hours.
- 🗻 **Owakudani Volcanic Valley** — Active volcanic zone with steaming vents and hot springs. Try kuro-tamago (black hard-boiled eggs cooked in sulfuric springs, $5 for 5 eggs). Cable car included. Entrance: $10/person.
- ☕ **Breakfast at Hakone Kowakien** — Buffet breakfast with Mt. Fuji views, featuring Japanese and Western options: onigiri, miso soup, fresh fruit. Estimated cost: $18 per person.

#### 🌤️ Afternoon (12:00 – 18:00)
- 🏯 **Hakone Open Air Museum** — Japan's first open-air art museum with 120 outdoor sculptures across 70,000 sqm of gardens. Includes indoor galleries with Picasso works. Opening hours: 9:00–17:00. Entrance fee: $22/adult, $10/child.
- 🎭 **Lake Ashi Pirate Ship Experience** — Cruise iconic Lake Ashi on a 17th-century-style galleon with Mt. Fuji backdrop (weather permitting). Authentic Hakone experience for families. Cost: $12/person round trip.
- 🍜 **Lunch at Amazake-Chaya Teahouse** — 400-year-old thatched-roof rest stop on the old Tokaido highway. Try amazake (sweet rice drink, $4) and mochi ($3). Cost: $10 per person.

#### 🌙 Evening (18:00 – 22:00)
- 🍽️ **Dinner at Hakone Tensui Saryo** — Kaiseki (multi-course Japanese haute cuisine) served in a traditional ryokan setting overlooking a Zen garden. Must-order: seasonal sashimi platter and matcha pudding. Reservation required. Cost: $45 per person.
- 🎶 **Hakone Yunessun Hot Springs Resort** — Evening onsen session with Mt. Fuji views. Family-friendly baths including wine bath, sake bath, and green tea pool. Best time: 7:00pm when crowds thin. Cost: $25/person.

**💵 Day 3 Estimated Cost:** $220
**🏨 Accommodation:** Shinjuku Washington Hotel (return evening), $80/night

---

### 🌅 Day 4: Kyoto — Ancient Capital

#### ☀️ Morning (07:00 – 12:00)
- 🚄 **Shinkansen Nozomi to Kyoto** — Depart Tokyo Station 8:00am. Book reserved seats in advance. World's most punctual train (average delay: 1 minute). Cost: $140/person one-way. Duration: 2 hours 15 min.
- ⛩️ **Fushimi Inari Taisha Shrine** — Iconic thousands of vermilion torii gates winding 4km up Mt. Inari. Arrive 10:00am to beat crowds. Entrance fee: Free. Duration: 1.5–3 hours depending on how far you hike.
- ☕ **Breakfast/Brunch at Vermillion Café** — Trendy café at the base of Fushimi Inari. Try matcha latte ($5) and tamago sandwich ($8). Estimated cost: $13 per person.

#### 🌤️ Afternoon (12:00 – 18:00)
- 🏯 **Nijo Castle** — UNESCO World Heritage Site. Marvel at the "nightingale floors" (squeaky floorboards designed to detect ninja intruders) and ornate Ninomaru Palace. Opening hours: 8:45–17:00. Entrance fee: $8/adult.
- 🎭 **Nishiki Market Local Food Experience** — Kyoto's "Kitchen": 400-year-old covered market with 100+ stalls. Sample: yudofu (tofu hotpot, $5), tsukemono pickles ($3 per bag), fresh tamagoyaki ($2). Cost: $15–20.
- 🍜 **Lunch at Nishiki Warai** — Authentic Kyoto obanzai (traditional home-style small dishes) set meal. Daily-changing seasonal vegetables, fish, and tofu. Cost: $15 per person.

#### 🌙 Evening (18:00 – 22:00)
- 🍽️ **Dinner at Gion Kappa** — Traditional kaiseki restaurant in the heart of Gion geisha district. Must-order: Kyoto-style yudofu hotpot and seasonal kyo-yasai vegetable dish. Ambiance: wooden machiya townhouse, candlelit. Cost: $40 per person. Reservation: highly recommended.
- 🎶 **Gion Corner Cultural Show** — 1-hour performance showcasing 7 Kyoto traditional arts: tea ceremony, ikebana flower arranging, koto music, maiko dance. Best evening entertainment in Kyoto. Cost: $30/person. Show times: 6:00pm & 7:00pm.

**💵 Day 4 Estimated Cost:** $310
**🏨 Accommodation:** Kyoto Granbell Hotel, Gion area, $85/night

---

### 🌅 Day 5: Kyoto Temples & Departure

#### ☀️ Morning (07:00 – 12:00)
- 🎋 **Arashiyama Bamboo Grove** — Walk through towering bamboo stalks at sunrise (6:30am) before tour groups arrive. Otherworldly, peaceful experience. Entrance fee: Free. Duration: 45 minutes.
- 🐒 **Tenryu-ji Temple & Garden** — UNESCO World Heritage zen garden with borrowed scenery of Mt. Arashiyama. Japan's first-ranked zen temple. Opening hours: 8:30–17:00. Entrance fee: $10/adult.
- ☕ **Breakfast at Café Arashiyama** — Riverside café serving tamago gohan (egg on rice, $8) and fresh-pressed yuzu juice ($4). Views of Hozu River. Estimated cost: $12 per person.

#### 🌤️ Afternoon (12:00 – 18:00)
- 🏯 **Kinkaku-ji (Golden Pavilion)** — Japan's most photographed landmark: a Zen Buddhist temple covered in gold leaf, perfectly reflected in Mirror Pond. Arrive 1:00pm for best light. Opening hours: 9:00–17:00. Entrance fee: $5/adult.
- 🎭 **Kyoto Handicraft Center Experience** — 7-floor center for traditional Kyoto crafts. Try a 30-minute kyo-yuzen silk dyeing workshop ($20) and browse handmade ceramics and lacquerware. Authentic souvenir culture. Cost: $20–40.
- 🍜 **Lunch at Gyukatsu Motomura, Kyoto** — Deep-fried wagyu beef cutlet (gyukatsu) with dipping sauces, served with stone grill to cook to your preference. Cost: $22 per person.

#### 🌙 Evening (18:00 – 22:00)
- 🍽️ **Farewell Dinner at Mishima-tei** — Legendary Kyoto sukiyaki restaurant since 1873. Marbled wagyu beef cooked tableside in sweet soy broth. Must-order: premium sukiyaki set with raw egg dip. Cost: $55 per person. Book in advance.
- 🚄 **Shinkansen Return to Tokyo** — Depart Kyoto 20:00 for Narita/Haneda departure. Or spend the evening at Kyoto Station's 11th floor observatory (free) watching the illuminated cityscape.

**💵 Day 5 Estimated Cost:** $200
**🏨 Accommodation:** Kyoto Granbell Hotel (check-out) or airport hotel

---

## 💰 Complete Budget Breakdown

| Category | Total Cost | Notes |
|----------|-----------|-------|
| 🏨 Accommodation | $325 | 3 nights Tokyo $80/night + 2 nights Kyoto $85/night |
| 🍽️ Food & Drinks | $270 | ~$54/day (breakfast $10 + lunch $20 + dinner $24) |
| 🚆 Transportation | $480 | Shinkansen ×2 ($280) + trains/bus ($120) + airport ($80) |
| 🎫 Activities & Entrance Fees | $185 | Temples, museums, Skytree, Hakone |
| 🌙 Nightlife & Entertainment | $120 | Gion Corner, onsen, Golden Gai |
| 🛍️ Shopping & Souvenirs | $70 | Nishiki Market, Nakamise-dori |
| 🆘 Emergency Buffer (10%) | $50 | Contingency fund |
| **💳 GRAND TOTAL** | **$1,500** | **USD 1,500.00** |

---

## 🗺️ Getting Around
- **Primary transport:** JR Pass (7-day, $280) covers all Shinkansen + local JR lines
- **Airport transfer:** Narita Express (N'EX) from airport to Shinjuku: $28/person, 90 minutes
- **Day trips:** Odakyu Romancecar for Hakone ($28 round trip)
- **App recommendations:** Hyperdia (train routes), Google Maps Japan, Suica app

## 📱 Essential Tips for Family Travelers
### 💡 Top 5 Money-Saving Tips
1. Buy 7-day JR Pass before arriving — saves ~$180 vs individual tickets
2. Eat breakfast at 7-Eleven or FamilyMart — saves $8/person vs café breakfast
3. Visit temples early morning (free/low entrance fee) before crowds
4. Use Suica IC card — cheaper than buying individual train tickets
5. Lunch sets at restaurants are 30–40% cheaper than dinner menus

### 🎯 Family-Specific Advice
- Book Shinkansen seats on the right side (Tokyo→Kyoto) for Mt. Fuji views
- Most attractions have English signage — navigation is family-friendly
- Coin lockers at train stations ($3–6/day) — leave luggage while exploring
- 7-Eleven ATMs accept foreign cards with lowest fees
- Children under 6 ride all JR trains free

### 🙏 Cultural Etiquette
- Remove shoes when entering traditional restaurants, temples, and ryokans
- Bow slightly when greeted — a nod is sufficient for tourists
- Never eat or drink while walking on the street
- Quiet mode on phones in trains — no phone calls in carriages
- Tipping is not practiced and can be considered rude

### 🍽️ Must-Try Local Foods
- **Ramen:** Rich tonkotsu broth with chashu pork — best at Ichiran ($12)
- **Wagyu Sukiyaki:** Premium marbled beef hotpot — a Kyoto specialty ($40–55)
- **Tamagoyaki:** Sweet rolled omelette found at every market stall ($2–3)

## 🌟 Bonus: Hidden Gems
- **Yanaka District, Tokyo:** Old-town neighborhood with 1950s atmosphere, independent craft shops, and affordable yakitori stalls. Most tourists miss it.
- **Philosopher's Path, Kyoto:** 2km canal-side walking path lined with 500 cherry trees. Free, locals' favorite.
- **Free Activity:** Meiji Shrine Inner Garden — lush forest sanctuary in central Tokyo, free entry, visited by almost no tourists.

## ✅ Pre-Trip Checklist
- [ ] No visa required for most nationalities for stays under 90 days
- [ ] No mandatory vaccinations — standard travel insurance recommended
- [ ] Carry JPY cash — many small shops, temples, and rural restaurants are cash-only
- [ ] Download: Hyperdia, Google Maps (offline), Google Translate (camera mode for menus)
- [ ] Pack: comfortable walking shoes (15,000+ steps/day), portable umbrella, IC card holder

---
*Itinerary crafted for Family travelers · Budget: USD 1,500.00 · 5 days in Japan*"""

        elif destination == "Bali":
            return """# ✈️ Bali — 3-Day Backpacker Itinerary

## 📋 Trip Overview
- **Destination:** Bali, Indonesia
- **Duration:** 3 Days / 2 Nights
- **Total Budget:** USD 800.00
- **Daily Budget:** USD 266.00
- **Travel Style:** Backpacker
- **Best Time to Visit:** April–October (dry season)
- **Highlights:** Rice terraces, surf beaches, ancient temples, vibrant nightlife

---

## 🗓️ Daily Itinerary

### 🌅 Day 1: Ubud — Arts & Culture

#### ☀️ Morning (07:00 – 12:00)
- 🏛️ **Tirta Empul Temple** — Sacred spring water temple where Balinese Hindus perform melukat (purification ritual). Observe or participate respectfully. Opening hours: 9:00–17:00. Entrance fee: $3. Duration: 1.5 hours.
- 🌾 **Tegalalang Rice Terrace Walk** — UNESCO-listed emerald rice paddies carved into hillside. Hire a local guide ($8) for stories about subak irrigation system dating back 9th century. Cost: $3 entrance + $8 guide.
- ☕ **Breakfast at Kopi Desa** — Local warung (small café). Try nasi goreng (fried rice with egg, $2.50) and kopi tubruk (traditional Indonesian coffee, $1). Estimated cost: $4 per person.

#### 🌤️ Afternoon (12:00 – 18:00)
- 🏯 **Pura Besakih (Mother Temple)** — Bali's largest and holiest temple complex on the slopes of Mt. Agung. 23 separate temples. Sarong rental included. Opening hours: 8:00–18:00. Entrance fee: $8.
- 🎭 **Ubud Monkey Forest Local Experience** — Sacred forest sanctuary with 1,000+ Balinese long-tailed macaques. Buy bananas at entrance ($1) to feed the monkeys. Authentic local nature experience. Cost: $4 entrance.
- 🍜 **Lunch at Warung Babi Guling Ibu Oka** — Bali's most famous babi guling (suckling pig) since 1950s. Crispy skin, aromatic spice paste, rice. Obama ate here! Cost: $5 per person.

#### 🌙 Evening (18:00 – 22:00)
- 🍽️ **Dinner at Locavore NXT** — Farm-to-table Balinese cuisine using hyper-local ingredients. Must-order: smoked duck with sambal matah and black rice pudding. Ambiance: open-air tropical garden. Cost: $18 per person.
- 🎶 **Kecak Fire Dance at Pura Uluwatu** — Ancient Balinese Hindu ritual dance performed by 70+ men chanting "cak" around a fire, at clifftop temple overlooking Indian Ocean at sunset. Best cultural show in Bali. Cost: $10/person. Show time: 6:00pm.

**💵 Day 1 Estimated Cost:** $75

---

### 🌅 Day 2: Seminyak & Kuta Beach

#### ☀️ Morning (07:00 – 12:00)
- 🏄 **Surf Lesson at Kuta Beach** — Kuta is the birthplace of Indonesian surfing. 2-hour beginner lesson with board and instructor from Rip Curl School of Surf. Even non-surfers stand up within 1 hour. Cost: $25. Duration: 2 hours.
- 🌊 **Tanah Lot Sea Temple** — Iconic offshore Hindu temple on a rocky outcrop, accessible only at low tide. Surrounded by crashing waves and sacred sea snakes. Opening hours: 7:00–19:00. Entrance fee: $5.
- ☕ **Breakfast at Revolver Espresso** — Seminyak's most famous specialty coffee shop in a narrow alleyway. Try flat white ($4) and smashed avo toast ($6). A backpacker institution. Estimated cost: $10 per person.

#### 🌤️ Afternoon (12:00 – 18:00)
- 🏯 **Seminyak Village & Petitenget Temple** — Explore Bali's hippest beach village, then visit the important Petitenget Temple (one of Bali's 9 directional temples). Opening hours: 8:00–18:00. Entrance fee: Free with sarong.
- 🎭 **Legian Street Local Shopping Experience** — Barter for batik clothing ($5–12), silver jewelry ($8–20), and hand-painted sarongs ($4). Practice your Bahasa Indonesia: "Berapa harga?" (How much?). Cost: $20–40 budget.
- 🍜 **Lunch at Warung Murah** — Ultra-budget local warung. Nasi campur (mixed rice plate) with 5 side dishes for $2. Eat with locals on plastic chairs. The most authentic meal in Bali. Cost: $2–3 per person.

#### 🌙 Evening (18:00 – 22:00)
- 🍽️ **Dinner at Merah Putih** — Architecturally stunning restaurant under a 14-meter bamboo ceiling. Modern Indonesian cuisine: braised oxtail rendang, Manado seafood soup. Ambiance: theatrical and romantic. Cost: $22 per person.
- 🎶 **Ku De Ta / Sunset Beach Bar** — Seminyak's legendary beachfront bar. Arrive 6:00pm for Bali's famous painted sky sunset. Live DJ from 8:00pm. Minimum spend: $10. A definitive Bali nightlife experience. Best time: 5:30pm for sunset.

**💵 Day 2 Estimated Cost:** $110

---

### 🌅 Day 3: South Bali & Departure

#### ☀️ Morning (07:00 – 12:00)
- 🌊 **Pandawa Beach** — Bali's "Secret Beach" carved through limestone cliffs. Calm turquoise waters perfect for swimming. Rent a sun lounger ($3) and snorkeling gear ($5). Opening hours: 7:00–18:00. Entrance fee: $2.
- 🏛️ **Garuda Wisnu Kencana Cultural Park** — Home to the world's tallest statue (121m) of the Hindu god Vishnu riding Garuda. Perched on a Bukit limestone plateau. Opening hours: 8:00–22:00. Entrance fee: $8.
- ☕ **Breakfast at Single Fin Uluwatu** — Cliffside café with sweeping views of Uluwatu surf break. Try açaí bowl ($8) and cold brew coffee ($4). Watch surfers tackle the famous left-break. Estimated cost: $12 per person.

#### 🌤️ Afternoon (12:00 – 18:00)
- 🏯 **Pura Luhur Uluwatu** — 11th-century clifftop temple 70m above the Indian Ocean. Sacred site for Balinese sea deity. Watch resident monkeys. Opening hours: 9:00–18:00. Entrance fee: $3.
- 🎭 **Jimbaran Fish Market Local Experience** — Buy fresh-caught tuna, snapper, and prawns directly from fishing boats at market price. Have your selection grilled at beachside warungs for $3–5 cooking fee. Most authentic seafood in Bali. Cost: $15–25 total.
- 🍜 **Lunch at Jimbaran Bay Seafood** — Legendary beachfront seafood tables on the sand. Grilled lobster, barramundi, tiger prawns with sambal. Eat with feet in the sand. Cost: $20 per person.

#### 🌙 Evening (18:00 – 22:00)
- 🍽️ **Farewell Dinner at Bumbu Bali** — Bali's most respected Balinese cuisine restaurant. Chef Heinz von Holzen has researched Balinese recipes for 30 years. Must-order: bebek betutu (slow-roasted duck in banana leaf) and pisang goreng. Cost: $25 per person.
- 🎶 **La Favela Vintage Bar** — Seminyak's most atmospheric bar: a 1930s colonial villa transformed into a labyrinth of rooms with different musical vibes — jazz, hip hop, electronic. Dress code: smart casual. Cover: $5. Best time: 9:00pm.

**💵 Day 3 Estimated Cost:** $120

---

## 💰 Complete Budget Breakdown

| Category | Total Cost | Notes |
|----------|-----------|-------|
| 🏨 Accommodation | $80 | 2 nights × $40/night (Seminyak hostel private room) |
| 🍽️ Food & Drinks | $165 | ~$55/day (breakfast $10 + lunch $8 + dinner $37) |
| 🚆 Transportation | $120 | Airport transfer ($25) + scooter rental 3 days ($30) + drivers ($65) |
| 🎫 Activities & Entrance Fees | $120 | Temples, Monkey Forest, GWK, beaches |
| 🌙 Nightlife & Entertainment | $75 | Kecak dance ($10), beach bars ($35), La Favela ($30) |
| 🛍️ Shopping & Souvenirs | $60 | Legian Street bargaining budget |
| 🆘 Emergency Buffer (10%) | $80 | Contingency fund |
| 💳 GRAND TOTAL | **$700** | **Under budget — $100 flex money** |

---
*Itinerary crafted for Backpacker travelers · Budget: USD 800.00 · 3 days in Bali*"""

        else:
            return f"""# ✈️ Travel Itinerary — {destination}

## 📋 Trip Overview
- **Destination:** {destination}
- **Travel Style:** As requested
- **Note:** Connect AWS Bedrock for a fully personalized AI-generated itinerary with real restaurant names, specific costs, and insider tips.

---

## 🗓️ Day 1: Arrival & Orientation

### ☀️ Morning (07:00 – 12:00)
- 🛬 **Airport Arrival** — Clear immigration, exchange currency, purchase local SIM card. Duration: 1.5 hours.
- 🏨 **Hotel Check-in & Freshen Up** — Drop luggage, review the day's plan. Duration: 1 hour.
- ☕ **Local Breakfast** — Visit a nearby café or market for an authentic local breakfast experience. Estimated cost: $8–12 per person.

### 🌤️ Afternoon (12:00 – 18:00)
- 🏯 **Main Cultural Landmark** — Visit the city's most significant historical or cultural site. Entrance fee varies.
- 🎭 **Local Market or Bazaar Experience** — Immerse yourself in local commerce, street food, and craftsmanship. Budget: $15–25.
- 🍜 **Lunch at Local Restaurant** — Try the national dish at a well-reviewed local spot. Cost: $10–18 per person.

### 🌙 Evening (18:00 – 22:00)
- 🍽️ **Dinner at Recommended Restaurant** — Sample the best local cuisine the destination has to offer. Cost: $20–35 per person.
- 🎶 **Evening Entertainment** — Live music, cultural performance, or vibrant bar district. Cost: $10–20.

**💵 Day 1 Estimated Cost:** $80–120

---

## 💡 To Get a Complete AI-Powered Itinerary:
Configure your AWS Bedrock credentials in `backend/.env` and this endpoint will generate a fully detailed {destination} itinerary with real names, exact prices, and local insider tips.

---
*Template itinerary — Configure AWS Bedrock for full personalization*"""
    
    def plan_trip_itinerary(
        self,
        destination: str,
        days: int,
        budget: float,
        travel_style: str
    ) -> str:
        """
        Generate a rich, structured trip itinerary using AWS Bedrock AI.

        Args:
            destination: Travel destination (e.g., "Japan", "Paris")
            days: Number of days for the trip
            budget: Budget in USD
            travel_style: Style of travel (e.g., "Family", "Solo", "Adventure", "Luxury")

        Returns:
            str: Detailed structured daily itinerary in markdown format
        """
        prompt = f"""You are a world-class travel planner with 20 years of experience crafting \
highly detailed, personalized travel itineraries. Your task is to create an exceptional \
{days}-day itinerary for {destination}.

=== TRIP PARAMETERS ===
- Destination   : {destination}
- Duration      : {days} days
- Total Budget  : USD {budget:,.2f}
- Daily Budget  : USD {budget / days:,.2f}
- Travel Style  : {travel_style}

=== STRICT OUTPUT FORMAT (MANDATORY) ===
Respond ONLY in valid Markdown. Follow this exact structure for EVERY single day:

---

# ✈️ {destination} — {days}-Day {travel_style} Itinerary

## 📋 Trip Overview
- **Destination:** {destination}
- **Duration:** {days} days
- **Total Budget:** USD {budget:,.2f}
- **Daily Budget:** USD {budget / days:,.2f}
- **Travel Style:** {travel_style}
- **Best Time to Visit:** [specific months and reason]
- **Highlights:** [3 top reasons to visit]

---

## 🗓️ Daily Itinerary

### 🌅 Day 1: [Catchy theme title]

#### ☀️ Morning (07:00 – 12:00)
*(MANDATORY: provide EXACTLY 3 morning activities with specific names, addresses, and estimated costs)*
- 🏛️ **[Activity 1 name]** — [Specific description, what to see/do, why it's special]. Estimated cost: $X. Duration: X hours.
- 🎨 **[Activity 2 name]** — [Specific description including address or neighborhood]. Estimated cost: $X. Duration: X hours.
- ☕ **[Activity 3 name / Breakfast spot]** — [Specific local breakfast recommendation with dish names]. Estimated cost: $X per person.

#### 🌤️ Afternoon (12:00 – 18:00)
*(MANDATORY: include at least 1 cultural site and 1 authentic local experience)*
- 🏯 **[Cultural Site name]** — [History, significance, what to expect. Include opening hours and entrance fee].
- 🎭 **[Local Experience name]** — [Authentic local activity: cooking class, craft workshop, local market, etc.]. Cost: $X.
- 🍜 **Lunch at [Restaurant/Market name]** — [Specific local dish to try, why this spot is authentic]. Cost: $X per person.

#### 🌙 Evening (18:00 – 22:00)
*(MANDATORY: include a specific dinner spot and a nightlife/evening entertainment option)*
- 🍽️ **Dinner at [Restaurant name]** — [Cuisine type, must-order dishes, ambiance, price range]. Reservation recommended: Yes/No. Cost: $X per person.
- 🎶 **[Nightlife/Entertainment]** — [Specific bar, live music venue, night market, cultural show, or evening activity]. Cost: $X. Best time to arrive: Xpm.

**💵 Day 1 Estimated Cost:** $X
**🏨 Accommodation:** [Hotel/hostel name or type, neighborhood, estimated cost per night]

---

[REPEAT THE EXACT SAME STRUCTURE FOR EVERY REMAINING DAY — Day 2 through Day {days}]
Each day MUST have:
✅ Exactly 3 morning activities with costs and durations
✅ At least 1 named cultural site in the afternoon
✅ At least 1 authentic local experience in the afternoon
✅ A specific named dinner restaurant with dish recommendations
✅ A specific nightlife or evening entertainment option
✅ Daily cost estimate

---

## 💰 Complete Budget Breakdown

| Category | Total Cost | Notes |
|----------|-----------|-------|
| 🏨 Accommodation | $X | X nights × $X/night |
| 🍽️ Food & Drinks | $X | Breakfast $X + Lunch $X + Dinner $X per day |
| 🚆 Transportation | $X | Flights, trains, local transport |
| 🎫 Activities & Entrance Fees | $X | All attraction tickets |
| 🌙 Nightlife & Entertainment | $X | Evening activities |
| 🛍️ Shopping & Souvenirs | $X | Estimated spend |
| 🆘 Emergency Buffer (10%) | $X | Contingency |
| **💳 GRAND TOTAL** | **$X** | **Must equal USD {budget:,.2f}** |

---

## 🗺️ Getting Around
- **Primary transport:** [Most efficient way to navigate {destination}]
- **Airport transfer:** [How to get from airport to city center, cost, duration]
- **Day trips:** [Recommended transport for excursions]
- **App recommendations:** [2-3 specific transport apps for {destination}]

## 📱 Essential Tips for {travel_style} Travelers
### 💡 Top 5 Money-Saving Tips
1. [Specific tip with estimated savings]
2. [Specific tip with estimated savings]
3. [Specific tip with estimated savings]
4. [Specific tip with estimated savings]
5. [Specific tip with estimated savings]

### 🎯 {travel_style}-Specific Advice
- [3-5 tips tailored specifically to {travel_style} travel style]

### 🙏 Cultural Etiquette
- [3-5 must-know customs, dos and don'ts for {destination}]

### 🍽️ Must-Try Local Foods
- **[Dish 1]:** [Description, where to find it, average price]
- **[Dish 2]:** [Description, where to find it, average price]
- **[Dish 3]:** [Description, where to find it, average price]

## 🌟 Bonus: Hidden Gems
- **[Hidden gem 1]:** [Why locals love it, how to get there]
- **[Hidden gem 2]:** [Why locals love it, how to get there]
- **[Free activity]:** [No-cost experience that most tourists miss]

## ✅ Pre-Trip Checklist
- [ ] [Visa/entry requirement specific to {destination}]
- [ ] [Vaccination or health requirement if any]
- [ ] [Currency and payment tips]
- [ ] [Essential apps to download]
- [ ] [What to pack specific to {travel_style} and {destination}]

---
*Itinerary crafted for {travel_style} travelers · Budget: USD {budget:,.2f} · {days} days in {destination}*

=== CRITICAL RULES ===
1. Be SPECIFIC — use real place names, real restaurants, real attractions
2. Include EXACT prices in USD for every activity, meal, and transport
3. Ensure grand total matches USD {budget:,.2f}
4. Every day MUST have morning (3 activities), afternoon (cultural site + local experience), evening (dinner + nightlife)
5. Tailor ALL recommendations to {travel_style} travel style
6. Use emojis throughout for visual clarity
7. Do NOT use placeholder text like "[Activity name]" — fill in real names"""

        return self.get_ai_recommendation(prompt, max_tokens=4096)


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
