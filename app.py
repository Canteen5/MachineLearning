from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load your CSVs
menu_df = pd.read_csv('fake_menu.csv')
order_df = pd.read_csv('fake_orders.csv')

# Compute popularity
item_popularity = order_df['item_id'].value_counts().reset_index()
item_popularity.columns = ['item_id', 'total_orders']
menu_df = menu_df.merge(item_popularity, on='item_id', how='left').fillna({'total_orders': 0})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommendations')
def get_recommendations():
    category = request.args.get('category', default='Snacks')
    top_n = int(request.args.get('top_n', 5))
    subset = menu_df[menu_df['category'].str.lower() == category.lower()]
    top_items = subset.sort_values('total_orders', ascending=False).head(top_n)
    return jsonify(top_items[['item_name', 'price', 'total_orders']].to_dict(orient='records'))

# ✅ NEW: dynamic endpoint to send all categories to frontend
@app.route('/categories')
def get_categories():
    categories = sorted(menu_df['category'].dropna().unique().tolist())
    return jsonify(categories)

if __name__ == '__main__':
    app.run()
