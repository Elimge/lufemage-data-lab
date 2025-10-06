# scripts/generate_dataset.py

# Libraries imports
import pandas as pd
import numpy as np
from faker import Faker
import datetime
import random

# --- CONFIGURATION ---
NUM_RECORDS = 5000
OUTPUT_PATH = "data/raw_sales_data.csv"

# --- GENERATION LOGIC ---

def generate_sales_data(num_records):
    """
    Generates a pandas DataFrame with simulated sales data.
    Args:
        num_records(int): The number of sales records to generate.
    Returns:
        pd.DataFrame: A DataFrame containing the sales data.
    """

    # Initialize Faker to generate fake data. Configured for Spanish locale.
    fake = Faker("es_ES")

    # --- Creating the bases for the columns ---

    # 1. id_cliente: Simulate a base of recurring customers.  
    # Create 800 unique customer IDs and then sample from that list.  
    # This ensures that some customers have multiple purchases.
    customer_ids = [fake.uuid4() for _ in range(int(num_records * 0.2))]
    chosen_customer_ids = [random.choice(customer_ids) for _ in range(num_records)]

    # 2. fecha_compra: Dates in the last 2 years. 
    end_date = datetime.datetime.now() 
    start_date = end_date - datetime.timedelta(days=730)
    dates = [fake.date_time_between(start_date=start_date, end_date=end_date) for _ in range(num_records)]

    # 3. monto: Use a gamma distribution to make the sales amounts look more realistic.  
    # Most sales will have low amounts, with a few high-value sales.  
    # This approach is much better than using a simple random number.
    shape, scale = 2.0, 150.0 #Distribution params 
    amounts = np.random.gamma(shape, scale, num_records).round(2)

    # 4. categoria_producto: Define a list and assign probabilities.
    product_categories = ["Electrónica" , "Ropa", "Hogar", "Alimentos", "Juguetes", "Libros"]
    category_probabilities = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]
    categories = np.random.choice(product_categories, num_records, p=category_probabilities)

    # 5. ciudad: Colombian cities, also with probabilities to simulate bigger markets 
    cities = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena"]
    city_probabilities = [0.4, 0.25, 0.15, 0.1, 0.1]
    chosen_cities = np.random.choice(cities, num_records, p=city_probabilities)

    # 6. metodo_pago: 
    payment_methods = ["Tarjeta de Crédito", "PSE", "Efectivo", "Billetera digital"]
    payment_probabilities = [0.5, 0.25, 0.1, 0.15]
    chosen_payment_methods = np.random.choice(payment_methods, num_records, p=payment_probabilities)

    # --- Dataframe Assembly --- 

    data = {
        "id_cliente": chosen_customer_ids,
        "fecha_compra": dates, 
        "monto": amounts, 
        "categoria_producto": categories,
        "ciudad": chosen_cities,
        "metodo_pago": chosen_payment_methods
    }

    df = pd.DataFrame(data)

    return df 

    # --- SCRIPT EXECUTION --- 

if __name__ == "__main__":
    print(f"Starting the generation of {NUM_RECORDS} sales records...")

    # Generate the data
    sales_df = generate_sales_data(NUM_RECORDS)

    # Save the DataFrame to a CSV file
    sales_df.to_csv(OUTPUT_PATH, index=False, date_format="%Y-%m-%d %H:%M:%S")

    print(f"Success! Dataset saved to: {OUTPUT_PATH}")

