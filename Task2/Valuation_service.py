import pandas as pd

def load_data():
    data = pd.read_csv('data.csv')
    currencies = pd.read_csv('currencies.csv')
    matchings = pd.read_csv('matchings.csv')
    return data, currencies, matchings

def create_currency_dict(currencies):
    return currencies.set_index('currency')['ratio'].to_dict()

def convert_price_to_pln(data, currency_dict):
    data['price_in_pln'] = data['price'] * data['currency'].map(currency_dict)
    return data

def calculate_total_price(data):
    data['total_price'] = data['price_in_pln'] * data['quantity']
    return data

def sort_data(data):
    return data.sort_values(['matching_id', 'total_price'], ascending=[True, False])

def process_matching(data_sorted, matchings):
    output = []
    for id in matchings['matching_id']:
        matching_data = data_sorted[data_sorted['matching_id'] == id]
        ignored_products_count = max(0, len(matching_data) - matchings[matchings['matching_id'] == id]['top_priced_count'].values[0])
        matching_data = matching_data.head(matchings[matchings['matching_id'] == id]['top_priced_count'].values[0])
        total_price = matching_data['total_price'].sum() 
        avg_price = total_price / matching_data['quantity'].sum()
        
        output.append({
            'matching_id': id,
            'total_price': total_price,
            'avg_price': avg_price,
            'currency': 'PLN',
            'ignored_products_count': ignored_products_count
        })
    return pd.DataFrame(output)

def save_to_csv(output_df):
    output_df.to_csv('top_products.csv', index=False)

if __name__ == '__main__':

    data, currencies, matchings = load_data()
    data_sorted = sort_data(calculate_total_price(convert_price_to_pln(data, create_currency_dict(currencies))))
    output = process_matching(data_sorted, matchings)
    save_to_csv(output)