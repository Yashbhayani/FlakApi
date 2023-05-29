from flask import Flask, jsonify, make_response, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    request.headers['token']
    data = "hello, this is our first flask website"
    return jsonify({'data': data})

@app.route("/view", methods=["GET"])
def view():
    try:
        token = request.headers['token']
        con = sqlite3.connect("user.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from Employees")
        data = cur.fetchall()
        DATAUSER = []
        for d in data:
            user = UserData(d["id"], d["name"], d["email"], d["mobilenumber"])
            DATAUSER.append(user)
        return make_response({"data": DATAUSER})

    except Exception as e:
        return jsonify({"Error": "Invalid request"})

@app.route("/savedetails", methods=["POST"])
def saveDetails():
    try:
        name = request.json["name"]
        email = request.json["email"]
        mobilenumber = request.json["mobilenumber"]
        with sqlite3.connect("user.db") as con:
            cur = con.cursor()
            cur.execute(
                "INSERT into Employees (name, email, mobilenumber) values (?,?,?)", (name, email, mobilenumber))
            con.commit()
            return make_response({"data": "Employee successfully Added", 'status': 200})
    except Exception as e:
        return jsonify({"Error": "Invalid request"})

@app.route("/edit/<int:id>", methods=["PUT"])
def edit(id):
    try:
        name = request.json["name"]
        email = request.json["email"]
        mobilenumber = request.json["mobilenumber"]
        con = sqlite3.connect("user.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""UPDATE Employees SET name = ?, email = ?, mobilenumber = ? WHERE id = ? """,
                    (name, email, mobilenumber, id))
        con.commit()
        return make_response({"data": "Employee successfully Updated", 'status': 200})
    except Exception as e:
        return jsonify({"Error": "Invalid request"})

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    try:
        con = sqlite3.connect("user.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""DELETE FROM Employees WHERE id = ?""", (id,))
        con.commit()
        return make_response({"data": "Employee successfully Deleted", 'status': 200})
    except Exception as e:
        return jsonify({"Error": "Invalid request"})


def UserData(id, name, email, mobilenumber):
    return {
        'id': id,
        'name': name,
        'email': email,
        'mobilenumber': mobilenumber
    }


if __name__ == "__main__":
    app.run(debug=True)
