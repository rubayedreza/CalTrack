from django.shortcuts import render

# Create your views here.
def home(request):
    import json
    import requests
    if request.method == 'POST':
        query = request.POST['query']
        # OpenFoodFacts Search API
        api_url = f'https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&action=process&json=1&page_size=1'
        
        try:
            response = requests.get(api_url)
            data = json.loads(response.content)
            products = data.get('products', [])
            
            if not products:
                api = "oops! There was an error"
            else:
                product = products[0]
                nutriments = product.get('nutriments', {})
                
                # Manual Mapping to match previous API Ninjas structure
             # Local Fallback Database
                LOCAL_FOOD_DB = {
                    # Regional
                    "macher jhol": { "name": "Macher Jhol (Fish Curry)", "calories": 320, "protein_g": 22, "carbohydrates_total_g": 12, "fat_total_g": 18, "image": "https://www.archanaskitchen.com/images/archanaskitchen/1-Author/usashis-gmail.com/Macher_Jhol_Bengali_Style_Fish_Curry.jpg" },
                    "biryani": { "name": "Chicken Biryani", "calories": 290, "protein_g": 10, "carbohydrates_total_g": 35, "fat_total_g": 12, "image": "https://recipes.timesofindia.com/thumb/msid-54308405,width-1600,height-900/54308405.jpg" },
                    "dal": { "name": "Dal (Lentil Soup)", "calories": 120, "protein_g": 8, "carbohydrates_total_g": 18, "fat_total_g": 3, "image": "https://www.connoisseurusveg.com/wp-content/uploads/2020/02/red-lentil-dal-16-500x500.jpg" },
                    "roti": { "name": "Roti (Chapati)", "calories": 70, "protein_g": 3, "carbohydrates_total_g": 15, "fat_total_g": 0.4, "image": "https://static.toiimg.com/thumb/61545633.cms?imgsize=306132&width=800&height=800" },
                    "rasgulla": { "name": "Rasgulla", "calories": 125, "protein_g": 2, "carbohydrates_total_g": 25, "fat_total_g": 1, "image": "https://static.toiimg.com/thumb/52755223.cms?imgsize=244791&width=800&height=800" },
                    "samosa": { "name": "Samosa", "calories": 260, "protein_g": 6, "carbohydrates_total_g": 24, "fat_total_g": 17, "image": "https://static.toiimg.com/thumb/61050397.cms?imgsize=246859&width=800&height=800" },
                    "dosa": { "name": "Masala Dosa", "calories": 350, "protein_g": 8, "carbohydrates_total_g": 55, "fat_total_g": 10, "image": "https://vismaifood.com/storage/app/uploads/public/8b4/19e/427/thumb__700_0_0_0_auto.jpg" },
                    "paneer": { "name": "Paneer Butter Masala", "calories": 450, "protein_g": 14, "carbohydrates_total_g": 18, "fat_total_g": 35, "image": "https://www.ruchiskitchen.com/wp-content/uploads/2020/12/Paneer-Butter-Masala-1.jpg" },

                    # Common Generics
                    "cake": { "name": "Chocolate Cake (Slice)", "calories": 280, "protein_g": 4, "carbohydrates_total_g": 35, "fat_total_g": 14, "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" },
                    "pizza": { "name": "Pizza (Cheese Slice)", "calories": 285, "protein_g": 12, "carbohydrates_total_g": 36, "fat_total_g": 10, "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" },
                    "burger": { "name": "Cheeseburger", "calories": 350, "protein_g": 20, "carbohydrates_total_g": 30, "fat_total_g": 18, "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" },
                    "fries": { "name": "French Fries (Medium)", "calories": 312, "protein_g": 3, "carbohydrates_total_g": 41, "fat_total_g": 15, "image": "https://images.unsplash.com/photo-1573080496987-a199f8cd6268?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" },
                    "chicken": { "name": "Grilled Chicken Breast (100g)", "calories": 165, "protein_g": 31, "carbohydrates_total_g": 0, "fat_total_g": 3.6, "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" },
                    "apple": { "name": "Apple (Medium)", "calories": 52, "protein_g": 0.3, "carbohydrates_total_g": 14, "fat_total_g": 0.2, "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" }
                }
                api = [{
                    'name': product.get('product_name', query),
                    'image': product.get('image_url', ''),
                    'calories': nutriments.get('energy-kcal_value', 0),
                    'serving_size_g': 100, # Standardization
                    'fat_total_g': nutriments.get('fat_value', 0),
                    'fat_saturated_g': nutriments.get('saturated-fat_value', 0),
                    'protein_g': nutriments.get('proteins_value', 0),
                    'sodium_mg': nutriments.get('sodium_value', 0) * 1000 if nutriments.get('sodium_unit') == 'g' else nutriments.get('sodium_value', 0), # Check units if possible, usually OFF normalized
                    'potassium_mg': nutriments.get('potassium_value', 0),
                    'cholesterol_mg': 0, # OFF often lacks this specific field in basic api, defaulting to 0
                    'carbohydrates_total_g': nutriments.get('carbohydrates_value', 0),
                    'fiber_g': nutriments.get('fiber_value', 0),
                    'sugar_g': nutriments.get('sugars_value', 0),
                }]
                print(api)
        except Exception as e:
            api = "oops! There was an error"
            print(e)
            
        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'query': 'Enter a valid query'})
