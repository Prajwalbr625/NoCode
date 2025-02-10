import os
from jinja2 import Environment, FileSystemLoader

# Define project structure
OUTPUT_DIR = "generated_flask_project"
MODULES_DIR = os.path.join(OUTPUT_DIR, "modules")
ROUTES_DIR = os.path.join(OUTPUT_DIR, "routes")

# Create directories if they don't exist
os.makedirs(MODULES_DIR, exist_ok=True)
os.makedirs(ROUTES_DIR, exist_ok=True)

# Load templates
env = Environment(loader=FileSystemLoader("templates"), trim_blocks=True, lstrip_blocks=True)

# Load main templates
base_template = env.get_template("./base_flask.j2")
db_handler_template = env.get_template("modules/db_handler.j2")
utils_template = env.get_template("modules/utils.j2")
steps_generator_template = env.get_template("modules/steps_generator.j2")

# Load route templates
route_templates = {
    "GET": env.get_template("routes/get_route.j2"),
    "POST": env.get_template("routes/post_route.j2"),
    "PUT": env.get_template("routes/put_route.j2"),
    "DELETE": env.get_template("routes/delete_route.j2"),
}

# Example user-defined API routes
user_routes = [
{
    "component_id": 1,
    "route_name": "/employees",
    "method": "POST",
    "function_name": "create_employee",
    "payload": {
        "Department_ID": 1,
        "Employee_ID": 1,
        "Employee_Name": "John Doe",
        "Employee_Salary": 1000
    },
    "steps": [
        {
            "step_id": 1,
            "action": "GET",
            "field": ["Department_ID", "Employee_ID"],
            "from": "payload"
        },
        {
            "step_id": 2,
            "action": "GET",
            "field": "Department_ID",
            "from": "collection",
            "collection_name": "departments",
            "condition": {
                "type": "exists",
                "error_message": "Department not found"
            }
        },
        {
            "step_id": 3,
            "action": "GET",
            "field": "Employee_ID",
            "from": "collection",
            "collection_name": "employees",
            "condition": {
                "type": "not_exists",
                "error_message": "Employee ID already exists"
            }
        },
        {
            "step_id": 4,
            "action": "POST",
            "field": "Employee_ID",
            "data": "payload",
            "to": "collection",
            "collection_name": "employees"
        },
        {
            "step_id": 5,
            "action": "Update",
            "field": "Department_ID",
            "update_value": "Employee_ID",
            "update_field": "Employee_IDS",
            "update_type": "append",
            "to": "collection",
            "collection_name": "departments"
        }
    ]
}
]

# Generate Sequence of steps code
def generate_steps(steps):
    return steps_generator_template.render(steps=steps)

# Generate route code
routes_code = "\n\n".join(
    route_templates[route["method"]].render(**route, generated_sequence=generate_steps(route["steps"])) for route in user_routes
)


# Generate Flask app
final_code = base_template.render(
    database_name="test_db",
    routes=routes_code
)

# Write Flask app file
app_file = os.path.join(OUTPUT_DIR, "generated_flask_app.py")
with open(app_file, "w") as f:
    f.write(final_code)

# Write db_handler.py
db_handler_file = os.path.join(MODULES_DIR, "db_handler.py")
with open(db_handler_file, "w") as f:
    f.write(db_handler_template.render())

# Write utils.py
utils_file = os.path.join(MODULES_DIR, "utils.py")
with open(utils_file, "w") as f:
    f.write(utils_template.render())

print(f"✅ Flask project generated successfully in: {OUTPUT_DIR}")
print(f"📂 Project structure:")
print(f" ├── {OUTPUT_DIR}/")
print(f" │   ├── generated_flask_app.py")
print(f" │   ├── modules/")
print(f" │   │   ├── db_handler.py")
print(f" │   │   ├── utils.py")
print(f" │   ├── routes/ (for future route modularity)")

