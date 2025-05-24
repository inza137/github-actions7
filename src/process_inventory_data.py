# .github/scripts/process_inventory_data.py

import pandas as pd
import os

print(f"--- Python script starting inside the container ---")
print(f"Current working directory: {os.getcwd()}") # Should be GITHUB_WORKSPACE
print(f"User: {os.environ.get('USER', os.getuid())}") # Check user running the script

# --- 1. Create or Load Sample Data ---
print("\nStep 1: Generating sample inventory data...")
data = {
    'product_id': ['P001', 'P002', 'P003', 'P004', 'P005', 'P006'],
    'product_name': ['SuperWidget', 'MegaDevice', 'FlexiGizmo', 'RoboArm', 'DataStreamer', 'AI-Core'],
    'category': ['Widgets', 'Devices', 'Gizmos', 'Robotics', 'Data', 'AI'],
    'unit_price': [19.99, 120.50, 45.00, 899.00, 250.75, 1500.00],
    'stock_quantity': [150, 30, 75, 10, 22, 5]
}
inventory_df = pd.DataFrame(data)
print("Original Inventory DataFrame:")
print(inventory_df.to_string())

# --- 2. Perform Data Transformation ---
print("\nStep 2: Performing transformations...")
# Calculate total stock value for each product
inventory_df['total_stock_value'] = inventory_df['unit_price'] * inventory_df['stock_quantity']

# Categorize products by price range
def categorize_price(price):
    if price < 50:
        return 'Low'
    elif price < 300:
        return 'Medium'
    else:
        return 'High'
inventory_df['price_category'] = inventory_df['unit_price'].apply(categorize_price)

print("\nTransformed Inventory DataFrame:")
print(inventory_df.to_string())

# --- 3. Save Processed Data ---
# Output will be saved in the GITHUB_WORKSPACE, which is mounted into the container
output_directory = "processed_data_output" # Create a subdirectory in the workspace
# Create the directory if it doesn't exist
if not os.path.exists(output_directory):
    print(f"Creating output directory: {output_directory}")
    os.makedirs(output_directory)

output_file_path = os.path.join(output_directory, "transformed_inventory.csv")
inventory_df.to_csv(output_file_path, index=False)
print(f"\nStep 3: Processed data saved to: {output_file_path}")

# --- 4. Verify Output in Workspace ---
print("\nStep 4: Verifying files in the workspace from within the container...")
workspace_path = os.environ.get("GITHUB_WORKSPACE", "/github/workspace")
print(f"Listing contents of GITHUB_WORKSPACE ({workspace_path}):")
# Using os.system for a simple ls, ensure your container has 'ls'
# For a python:slim image, 'ls' is available.
if os.name == 'posix':
    os.system(f"ls -Rla {workspace_path}")
else: # Basic dir for Windows if container was Windows-based
    os.system(f"dir {workspace_path} /s /b")


print(f"\n--- Python script finished successfully inside the container ---")