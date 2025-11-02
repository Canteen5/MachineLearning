from flask import Flask, request, jsonify
import pandas as pd

menu_df = pd.read_csv('fake_menu.csv')
order_df = pd.read_csv('fake_orders.csv')

item_popularity = order_df['item_id'].value_counts().reset_index()
item_popularity.columns = ['item_id', 'total_orders']
menu_df = menu_df.merge(item_popularity, on='item_id', how='left').fillna({'total_orders': 0})

app = Flask(__name__)

@app.route('/')
def home():
    return "🍽️ Canteen Recommendation API is running on Vercel!"

@app.route('/recommendations')
def get_recommendations():
    category = request.args.get('category', default='Snacks')
    top_n = int(request.args.get('top_n', 5))
    subset = menu_df[menu_df['category'].str.lower() == category.lower()]
    top_items = subset.sort_values('total_orders', ascending=False).head(top_n)
    return jsonify(top_items[['item_name', 'price', 'total_orders']].to_dict(orient='records'))

# Vercel expects app to be named "app"
# No need for if __name__ == "__main__"
if __name__ == "__main__":
    app.run(debug=True)

