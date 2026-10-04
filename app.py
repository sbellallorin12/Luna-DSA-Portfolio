from flask import Flask, render_template, request
import math

app = Flask(__name__)


# =============================
# LINKED LIST IMPLEMENTATION
# =============================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def delete(self, data):
        current = self.head
        previous = None

        while current:
            if current.data == data:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                return True

            previous = current
            current = current.next

        return False

    def display(self):
        values = []
        current = self.head
        while current:
            values.append(current.data)
            current = current.next
        return values


linked_list = LinkedList()


# =============================
# PAGE ROUTES
# =============================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# =============================
# AREA CALCULATOR
# =============================

@app.route('/area', methods=['GET', 'POST'])
def area():
    circle_area = None
    triangle_area = None
    error = None

    if request.method == 'POST':
        shape = request.form.get('shape')

        try:
            if shape == 'circle':
                radius = float(request.form.get('radius', ''))
                if radius < 0:
                    raise ValueError
                circle_area = math.pi * radius ** 2

            elif shape == 'triangle':
                base = float(request.form.get('base', ''))
                height = float(request.form.get('height', ''))
                if base < 0 or height < 0:
                    raise ValueError
                triangle_area = 0.5 * base * height

        except ValueError:
            error = 'Please enter valid non-negative numbers.'

    return render_template(
        'area.html',
        circle_area=circle_area,
        triangle_area=triangle_area,
        error=error
    )


# =============================
# LINKED LIST UI
# =============================

@app.route('/linkedlist', methods=['GET', 'POST'])
def linkedlist():
    message = None
    message_type = 'success'

    if request.method == 'POST':
        action = request.form.get('action')
        value = request.form.get('value', '').strip()

        if action == 'add':
            if value:
                linked_list.add(value)
                message = f'Node "{value}" was added successfully.'
            else:
                message = 'Please enter a value.'
                message_type = 'error'

        elif action == 'delete':
            if value and linked_list.delete(value):
                message = f'Node "{value}" was deleted successfully.'
            else:
                message = f'Node "{value}" was not found.'
                message_type = 'error'

        elif action == 'clear':
            linked_list.head = None
            message = 'The linked list was cleared.'

    return render_template(
        'linkedlist.html',
        values=linked_list.display(),
        message=message,
        message_type=message_type
    )


if __name__ == '__main__':
    app.run(debug=True)
