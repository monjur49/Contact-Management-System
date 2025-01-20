from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated database
contacts = []

# Serve the HTML page
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contact Management System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
            }
            .container {
                max-width: 800px;
                margin: 20px auto;
                background: #fff;
                padding: 20px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            h1, h2 {
                text-align: center;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            input, button {
                padding: 10px;
                font-size: 16px;
            }
            button {
                background: #007BFF;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background: #0056b3;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                padding: 10px;
                text-align: left;
                border: 1px solid #ddd;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Contact Management System</h1>
            <form id="contact-form">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>

                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>

                <label for="phone">Phone:</label>
                <input type="tel" id="phone" name="phone" required>

                <button type="submit">Add Contact</button>
            </form>
            <hr>
            <h2>Contacts List</h2>
            <table id="contacts-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- Contacts will be displayed here -->
                </tbody>
            </table>
        </div>
        <script>
            const form = document.getElementById("contact-form");
            const tableBody = document.querySelector("#contacts-table tbody");

            // Fetch and display contacts
            async function fetchContacts() {
                const response = await fetch("/contacts");
                const contacts = await response.json();
                tableBody.innerHTML = "";

                contacts.forEach((contact, index) => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${contact.name}</td>
                        <td>${contact.email}</td>
                        <td>${contact.phone}</td>
                        <td>
                            <button onclick="deleteContact(${index})">Delete</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            }

            // Add a new contact
            form.addEventListener("submit", async (e) => {
                e.preventDefault();
                const formData = new FormData(form);
                const contact = {
                    name: formData.get("name"),
                    email: formData.get("email"),
                    phone: formData.get("phone"),
                };

                await fetch("/contacts", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(contact),
                });

                form.reset();
                fetchContacts();
            });

            // Delete a contact
            async function deleteContact(contactId) {
                await fetch(`/contacts/${contactId}`, {
                    method: "DELETE",
                });
                fetchContacts();
            }

            // Initialize
            fetchContacts();
        </script>
    </body>
    </html>
    '''

# API to manage contacts
@app.route('/contacts', methods=['GET', 'POST'])
def manage_contacts():
    if request.method == 'POST':
        # Add a new contact
        data = request.get_json()
        contacts.append(data)
        return jsonify({'message': 'Contact added successfully!'}), 201
    return jsonify(contacts)

@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    if 0 <= contact_id < len(contacts):
        contacts.pop(contact_id)
        return jsonify({'message': 'Contact deleted successfully!'}), 200
    return jsonify({'error': 'Contact not found!'}), 404

if __name__ == '__main__':
    app.run(debug=True)
