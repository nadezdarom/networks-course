import json
from flask import Flask, jsonify, request, send_file
from flask_uploads import UploadSet, IMAGES, configure_uploads


app = Flask(__name__)
app.config["UPLOADED_PHOTOS_DEST"] = "images"

icons = UploadSet("photos", IMAGES)
configure_uploads(app, icons)

products = [
    {
        "id": 0,
        "name": "Sphygmomanometer",
        "description": "A device which is used to measure blood pressure",
        "icon": "pic1.png"
    },
]

next_id = 1

@app.route("/products", methods={'GET'})
def get_products():
    return jsonify(products)

@app.route("/product/<int:id>", methods={'GET'})
def get_product_by_id(id: int):
    product = get_product(id)
    if product is None:
        return jsonify({ "error": "Product does not exists" }), 404
    return jsonify(product)

def get_product(id: int):
    return next((p for p in products if p['id'] == id), None)

def check_product(product):
    for key in product.keys():
        if key != "name" and key != "description" and key != "icon":
            return False
    return True

@app.route("/product", methods={'POST'})
def add_new_product():
    global next_id
    product = json.loads(request.data)
    if not check_product(product):
        return jsonify({ "error": "Product is not valid" }), 400
    
    product["id"] = next_id
    next_id += 1

    if "icon" in request.files:
        icon = request.files["icon"]
        filename = icons.save(icon)
        product["icon"] = filename


    products.append(product)

    return jsonify(product), 201

@app.route("/product/<int:id>", methods={'PUT'})
def update_product(id: int):
    product = get_product(id)
    if product is None:
        return jsonify({ "error": "Product does not exists" }), 404
    
    updated_product = json.loads(request.data)
    if not check_product(updated_product):
        return jsonify({ "error": "Product is not valid" }), 400
    
    product.update(updated_product)
    return jsonify(product)

@app.route("/product/<int:id>", methods={'DELETE'})
def delete_product(id: int):
    global products
    product = get_product(id)
    if product is None:
        return jsonify({ "error": "Product does not exists" }), 404
    
    products = [p for p in products if p["id"] != id]
    return jsonify(product), 200


@app.route("/product/<int:id>/image", methods={'GET'})
def get_icon(id: int):
    product = get_product(id)
    if product is None:
        return jsonify({ "error": "Product does not exists" }), 404
    
    file_path = f"images/{product['icon']}"

    return send_file(file_path)


@app.route("/product/<int:id>/image", methods={'POST'})
def post_icon(id: int):
    product = get_product(id)
    if product is None:
        return jsonify({ "error": "Product does not exists" }), 404
    
    if "icon" not in request.files:
        return jsonify({ "error": "No icon" }), 400
    
    icon = request.files["icon"]
    
    filename = icons.save(icon)
    product["icon"] = filename

    return "", 201