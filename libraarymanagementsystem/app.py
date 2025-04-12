from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Raj@123_@45",
    database="lms"
)
cursor = db.cursor(dictionary=True)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email == "admin@library.com" and password == "admin123":
            session["user"] = email
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/users")
def users():
    if "user" not in session:
        return redirect(url_for("login"))
    cursor.execute("SELECT * FROM User")
    users = cursor.fetchall()
    return render_template("users.html", users=users)

@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        cursor.execute("INSERT INTO User (Name, Email, Phone) VALUES (%s, %s, %s)", (name, email, phone))
        db.commit()
        return redirect(url_for("users"))
    return render_template("add_user.html")

@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        cursor.execute("UPDATE User SET Name=%s, Email=%s, Phone=%s WHERE User_ID=%s", (name, email, phone, user_id))
        db.commit()
        return redirect(url_for("users"))
    cursor.execute("SELECT * FROM User WHERE User_ID = %s", (user_id,))
    user = cursor.fetchone()
    return render_template("edit_user.html", user=user)

@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    if "user" not in session:
        return redirect(url_for("login"))
    cursor.execute("DELETE FROM User WHERE User_ID = %s", (user_id,))
    db.commit()
    return redirect(url_for("users"))

@app.route("/librarians")
def librarians():
    if "user" not in session:
        return redirect(url_for("login"))
    cursor.execute("SELECT * FROM Librarian")
    librarians = cursor.fetchall()
    return render_template("librarians.html", librarians=librarians)

@app.route("/add_librarian", methods=["GET", "POST"])
def add_librarian():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        cursor.execute("INSERT INTO Librarian (Name, Email, Phone) VALUES (%s, %s, %s)", (name, email, phone))
        db.commit()
        return redirect(url_for("librarians"))
    return render_template("add_librarian.html")

@app.route("/edit_librarian/<int:librarian_id>", methods=["GET", "POST"])
def edit_librarian(librarian_id):
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        cursor.execute("UPDATE Librarian SET Name=%s, Email=%s, Phone=%s WHERE Librarian_ID=%s", (name, email, phone, librarian_id))
        db.commit()
        return redirect(url_for("librarians"))
    cursor.execute("SELECT * FROM Librarian WHERE Librarian_ID = %s", (librarian_id,))
    librarian = cursor.fetchone()
    return render_template("edit_librarian.html", librarian=librarian)

@app.route("/delete_librarian/<int:librarian_id>")
def delete_librarian(librarian_id):
    if "user" not in session:
        return redirect(url_for("login"))
    cursor.execute("DELETE FROM Librarian WHERE Librarian_ID = %s", (librarian_id,))
    db.commit()
    return redirect(url_for("librarians"))

@app.route("/books")
def books():
    if "user" not in session:
        return redirect(url_for("login"))
    cursor.execute("SELECT * FROM Book")
    books = cursor.fetchall()
    return render_template("books.html", books=books)

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        publisher = request.form["publisher"]
        year = request.form["year"]
        cursor.execute("INSERT INTO Book (Title, Author, Publisher, Year) VALUES (%s, %s, %s, %s)", (title, author, publisher, year))
        db.commit()
        return redirect(url_for("books"))
    return render_template("add_book.html")

@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        publisher = request.form["publisher"]
        year = request.form["year"]
        cursor.execute("UPDATE Book SET Title=%s, Author=%s, Publisher=%s, Year=%s WHERE Book_ID=%s", (title, author, publisher, year, book_id))
        db.commit()
        return redirect(url_for("books"))
    cursor.execute("SELECT * FROM Book WHERE Book_ID = %s", (book_id,))
    book = cursor.fetchone()
    return render_template("edit_book.html", book=book)

@app.route("/delete_book/<int:book_id>")
def delete_book(book_id):
    if "user" not in session:
        return redirect(url_for("login"))
    cursor.execute("DELETE FROM Book WHERE Book_ID = %s", (book_id,))
    db.commit()
    return redirect(url_for("books"))

@app.route("/borrows")
def borrows():
    if "user" not in session:
        return redirect(url_for("login"))
    cursor.execute("""
        SELECT Borrow.Borrow_ID, Borrow.User_ID, Borrow.Book_ID, Borrow.Issue_Date, Borrow.Due_Date, Borrow.Return_Date,
               User.Name AS UserName, Book.Title AS BookTitle
        FROM Borrow
        JOIN User ON Borrow.User_ID = User.User_ID
        JOIN Book ON Borrow.Book_ID = Book.Book_ID
    """)
    borrows = cursor.fetchall()
    return render_template("borrows.html", borrows=borrows)

@app.route("/add_borrow", methods=["GET", "POST"])
def add_borrow():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        user_id = request.form["user_id"]
        book_id = request.form["book_id"]
        issue_date = request.form["issue_date"]
        due_date = request.form["due_date"]
        return_date = request.form["return_date"]
        cursor.execute("INSERT INTO Borrow (User_ID, Book_ID, Issue_Date, Due_Date, Return_Date) VALUES (%s, %s, %s, %s, %s)",
                       (user_id, book_id, issue_date, due_date, return_date))
        db.commit()
        return redirect(url_for("borrows"))
    cursor.execute("SELECT User_ID, Name FROM User")
    users = cursor.fetchall()
    cursor.execute("SELECT Book_ID, Title FROM Book")
    books = cursor.fetchall()
    return render_template("add_borrow.html", users=users, books=books)

@app.route("/delete_borrow/<int:borrow_id>")
def delete_borrow(borrow_id):
    if "user" not in session:
        return redirect(url_for("login"))
    cursor.execute("DELETE FROM Borrow WHERE Borrow_ID = %s", (borrow_id,))
    db.commit()
    return redirect(url_for("borrows"))

@app.route("/fines")
def fines():
    if "user" not in session:
        return redirect(url_for("login"))

    cursor.execute("""
        SELECT Fine.Fine_ID, Fine.Borrow_ID, Fine.Amount, Fine.Status,
               User.Name AS UserName, Book.Title AS BookTitle
        FROM Fine
        JOIN Borrow ON Fine.Borrow_ID = Borrow.Borrow_ID
        JOIN User ON Borrow.User_ID = User.User_ID
        JOIN Book ON Borrow.Book_ID = Book.Book_ID
    """)
    fines = cursor.fetchall()
    return render_template("fines.html", fines=fines)


@app.route("/add_fine", methods=["GET", "POST"])
def add_fine():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        borrow_id = request.form["borrow_id"]
        amount = request.form["amount"]
        status = request.form["status"]

        cursor.execute("INSERT INTO Fine (Borrow_ID, Amount, Status) VALUES (%s, %s, %s)",
                       (borrow_id, amount, status))
        db.commit()
        return redirect(url_for("fines"))

    cursor.execute("""
        SELECT Borrow.Borrow_ID, User.Name AS UserName, Book.Title AS BookTitle
        FROM Borrow
        JOIN User ON Borrow.User_ID = User.User_ID
        JOIN Book ON Borrow.Book_ID = Book.Book_ID
    """)
    borrows = cursor.fetchall()
    return render_template("add_fine.html", borrows=borrows)


@app.route("/edit_fine/<int:fine_id>", methods=["GET", "POST"])
def edit_fine(fine_id):
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        borrow_id = request.form["borrow_id"]
        amount = request.form["amount"]
        status = request.form["status"]

        cursor.execute("UPDATE Fine SET Borrow_ID = %s, Amount = %s, Status = %s WHERE Fine_ID = %s",
                       (borrow_id, amount, status, fine_id))
        db.commit()
        return redirect(url_for("fines"))

    cursor.execute("SELECT * FROM Fine WHERE Fine_ID = %s", (fine_id,))
    fine = cursor.fetchone()

    cursor.execute("""
        SELECT Borrow.Borrow_ID, User.Name AS UserName, Book.Title AS BookTitle
        FROM Borrow
        JOIN User ON Borrow.User_ID = User.User_ID
        JOIN Book ON Borrow.Book_ID = Book.Book_ID
    """)
    borrows = cursor.fetchall()
    return render_template("edit_fine.html", fine=fine, borrows=borrows)


@app.route("/delete_fine/<int:fine_id>")
def delete_fine(fine_id):
    if "user" not in session:
        return redirect(url_for("login"))

    cursor.execute("DELETE FROM Fine WHERE Fine_ID = %s", (fine_id,))
    db.commit()
    return redirect(url_for("fines"))


@app.route("/reservations")
def reservations():
    if "user" not in session:
        return redirect(url_for("login"))
    cursor.execute("""
        SELECT Reservation.Reservation_ID, Reservation.User_ID, Reservation.Book_ID,
               Reservation.Reservation_Date, User.Name AS UserName, Book.Title AS BookTitle
        FROM Reservation
        JOIN User ON Reservation.User_ID = User.User_ID
        JOIN Book ON Reservation.Book_ID = Book.Book_ID
    """)
    reservations = cursor.fetchall()
    return render_template("reservations.html", reservations=reservations)

@app.route("/add_reservation", methods=["GET", "POST"])
def add_reservation():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        user_id = request.form["user_id"]
        book_id = request.form["book_id"]
        reservation_date = request.form["reservation_date"]
        cursor.execute("INSERT INTO Reservation (User_ID, Book_ID, Reservation_Date) VALUES (%s, %s, %s)",
                       (user_id, book_id, reservation_date))
        db.commit()
        return redirect(url_for("reservations"))
    cursor.execute("SELECT User_ID, Name FROM User")
    users = cursor.fetchall()
    cursor.execute("SELECT Book_ID, Title FROM Book")
    books = cursor.fetchall()
    return render_template("add_reservation.html", users=users, books=books)


@app.route("/delete_reservation/<int:reservation_id>")
def delete_reservation(reservation_id):
    if "user" not in session:
        return redirect(url_for("login"))
    cursor.execute("DELETE FROM Reservation WHERE Reservation_ID = %s", (reservation_id,))
    db.commit()
    return redirect(url_for("reservations"))
@app.route("/dashboard")
def dashboard():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Raj@123_@45",
        database="lms"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS count FROM user")
    user_count = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) AS count FROM book")
    book_count = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) AS count FROM borrow")
    issue_count = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) AS count FROM librarian")
    librarian_count = cursor.fetchone()["count"]
    
    cursor.execute("SELECT COUNT(*) AS count FROM reservation")
    reservation_count = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) AS count FROM fine")
    fine_count = cursor.fetchone()["count"]

    conn.close()

    return render_template("dashboard.html", user_count=user_count, book_count=book_count, borrow_count=issue_count,librarian_count=librarian_count,reservation_count=reservation_count,
        fine_count=fine_count)

if __name__ == "__main__":
    app.run(debug=True)



