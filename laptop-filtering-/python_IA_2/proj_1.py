from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# List to store laptop information
laptops = []

csv_file_path = "laptop_sheet_1.csv"

with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    # Iterate over each row in the CSV file
    for row in reader:
        # Extract relevant information from the row
        brand = row["Brand"]
        model = row["Model"]
        processor = row["Processor"]
        screen_size = row["Screen Size"]
        ram = row['RAM'].replace('GB', '')  # Remove "GB" from RAM
        storage = row['Storage'].replace('GB SSD', '')
        price = row['Price in rupees']

        # Create a dictionary for the current laptop entry
        laptop = {
            "brand": brand,
            "model": model,
            "processor": processor,
            "screen_size": screen_size,
            "ram": ram,
            "storage": storage,
            "price": price
        }

        # Append the laptop dictionary to the list of laptops
        laptops.append(laptop)

# print(laptops)


@app.route('/')
def index():
    return render_template('filter.html')

@app.route('/submit', methods=['POST'])
def submit():
    brand = request.form.get('brand')
    model = request.form.get('model')
    processor = request.form.get('processor')
    screen_size = request.form.get('screen_size')
    ram = request.form.get('ram')

    # Append the entered information to the list
    laptops.append({"brand": brand, "model": model, "processor_speed": processor, "screen_size": screen_size, "ram": ram, "storage":storage})

    # Redirect to the homepage after submitting
    return render_template('index.html', message="Information submitted successfully!")

@app.route('/display')
def display():
    return render_template('display.html', laptops=laptops)

@app.route('/filter', methods=['GET', 'POST'])
def filter_laptops():
    if request.method == 'POST':
        min_ram = request.form.get('minRam')
        min_storage = request.form.get('minStorage')
        brand_name = request.form.get('Brand')
        scr_siz = request.form.get("screen_size")
        max_price = request.form.get("max_price")
        filtered_laptops = [laptop for laptop in laptops if (float(laptop["ram"]) >= float(min_ram) or not int(min_ram)) and (float(laptop["storage"]) >= float(min_storage) or not int(min_storage)) and (laptop["brand"] == brand_name or not brand_name) and (float(laptop["screen_size"]) >= float(scr_siz) or not int(scr_siz)) and (float(laptop["price"]) <= float(max_price) or not int(max_price))]
        return render_template('display.html', laptops=filtered_laptops)
    return render_template('filter.html')

if __name__ == '__main__':
    app.run(debug=True)